from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import shutil
import socket
from datetime import datetime, timezone, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "prompts" / "catalog.json"
ACTIVE_DIR = ROOT / "prompts" / "active"
TRASH_DIR = ROOT / "prompts" / "trash"
DASHBOARD_DIR = Path(__file__).resolve().parent
TZ = timezone(timedelta(hours=8))

STAGE_PREFIX = {
    "think": "THINK",
    "title": "TITLE",
    "write": "WRITE",
    "rewrite": "REWRITE",
    "review": "REVIEW",
    "general": "GENERAL",
}

STAGE_LABEL = {
    "think": "想深",
    "title": "标题",
    "write": "写稿",
    "rewrite": "改稿",
    "review": "审稿",
    "general": "通用",
}


def now_iso() -> str:
    return datetime.now(TZ).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:48] or "prompt"


def ensure_dirs() -> None:
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    TRASH_DIR.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> dict:
    if not path.exists():
        return {"version": 1, "updated_at": now_iso(), "items": []}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    data["updated_at"] = now_iso()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def safe_relative_path(value: str) -> Path:
    candidate = (ROOT / value).resolve()
    if ROOT not in candidate.parents and candidate != ROOT:
        raise ValueError("path escapes workspace")
    return candidate


def extract_prompt(markdown: str) -> str:
    match = re.search(
        r"##\s*可复制提示词\s*```(?:text)?\s*(.*?)\s*```",
        markdown,
        flags=re.S,
    )
    if match:
        return match.group(1).strip()
    match = re.search(r"```(?:text)?\s*(.*?)\s*```", markdown, flags=re.S)
    if match:
        return match.group(1).strip()
    return markdown.strip()


def extract_notes(markdown: str) -> str:
    match = re.search(r"##\s*(?:使用备注|二次追问|AI 味黑名单|备注)\s*(.*)", markdown, flags=re.S)
    return match.group(1).strip() if match else ""


def variables_from_prompt(prompt: str) -> list[str]:
    values = sorted(set(re.findall(r"【[^】]+】", prompt)))
    return values


def render_markdown(item: dict, prompt: str, notes: str = "") -> str:
    variables = variables_from_prompt(prompt)
    variable_lines = "\n".join(f"- `{v}`" for v in variables) or "- 暂无固定变量"
    tags = " / ".join(item.get("tags", [])) or "未分类"
    notes = notes.strip() or "这里写这个提示词的使用技巧、限制和二次追问方式。"
    return f"""# {item["id"]}: {item["title"]}

平台：{item.get("platform", "通用")}

阶段：{STAGE_LABEL.get(item.get("stage", "general"), item.get("stage", "general"))}

作用：{item.get("purpose", "")}

适合场景：{item.get("scenario", "")}

标签：{tags}

旧编号：{item.get("legacy_id") or "无"}

最后更新：{item.get("updated_at", now_iso())}

## 可修改变量

{variable_lines}

## 可复制提示词

```text
{prompt.strip()}
```

## 使用备注

{notes}
"""


def load_catalog() -> dict:
    ensure_dirs()
    catalog = read_json(CATALOG_PATH)
    catalog.setdefault("items", [])
    return catalog


def save_catalog(catalog: dict) -> None:
    write_json(CATALOG_PATH, catalog)


def find_item(catalog: dict, prompt_id: str) -> dict | None:
    prompt_id = prompt_id.upper()
    for item in catalog.get("items", []):
        if item.get("id", "").upper() == prompt_id or item.get("legacy_id", "").upper() == prompt_id:
            return item
    return None


def prompt_payload(item: dict, include_content: bool = True) -> dict:
    payload = dict(item)
    content = ""
    notes = ""
    file_value = item.get("file")
    if file_value:
        path = safe_relative_path(file_value)
        if path.exists():
            markdown = path.read_text(encoding="utf-8", errors="replace")
            content = extract_prompt(markdown)
            notes = extract_notes(markdown)
    payload["content"] = content if include_content else ""
    payload["preview"] = re.sub(r"\s+", " ", content).strip()[:260]
    payload["notes"] = notes
    payload["variables"] = variables_from_prompt(content)
    return payload


def next_id(catalog: dict, stage: str) -> str:
    prefix = STAGE_PREFIX.get(stage, "GENERAL")
    max_num = 0
    for item in catalog.get("items", []):
        match = re.match(rf"^{re.escape(prefix)}-(\d+)$", item.get("id", ""))
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"{prefix}-{max_num + 1:03d}"


def unique_file_path(prompt_id: str, title: str, status: str = "active") -> Path:
    folder = ACTIVE_DIR if status == "active" else TRASH_DIR
    base = f"{prompt_id}-{slugify(title)}.md"
    path = folder / base
    counter = 2
    while path.exists():
        path = folder / f"{prompt_id}-{slugify(title)}-{counter}.md"
        counter += 1
    return path


class PromptHandler(BaseHTTPRequestHandler):
    server_version = "PromptDashboard/1.0"

    def log_message(self, fmt: str, *args) -> None:
        return

    def send_json(self, data: dict | list, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message: str, status: HTTPStatus = HTTPStatus.BAD_REQUEST) -> None:
        self.send_json({"ok": False, "error": message}, status)

    def read_body_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length == 0:
            return {}
        body = self.rfile.read(length).decode("utf-8")
        return json.loads(body or "{}")

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self.send_json({"ok": True, "root": str(ROOT), "time": now_iso()})
            return
        if parsed.path == "/api/open":
            self.handle_open(parsed)
            return
        if parsed.path == "/api/prompts":
            self.handle_list(parsed)
            return
        if parsed.path.startswith("/api/prompts/"):
            prompt_id = unquote(parsed.path.rsplit("/", 1)[-1])
            self.handle_get_prompt(prompt_id)
            return
        self.serve_static(parsed.path)

    def handle_open(self, parsed) -> None:
        query = parse_qs(parsed.query)
        target_value = query.get("path", [""])[0]
        if not target_value:
            self.send_error_json("path is required")
            return
        try:
            target = safe_relative_path(target_value)
        except ValueError:
            self.send_error_json("path escapes workspace", HTTPStatus.FORBIDDEN)
            return
        if not target.exists():
            self.send_error_json("path not found", HTTPStatus.NOT_FOUND)
            return
        os.startfile(str(target))
        self.send_json({"ok": True, "path": str(target)})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/prompts":
            self.handle_create()
            return
        match = re.match(r"^/api/prompts/([^/]+)/(trash|restore)$", parsed.path)
        if match:
            prompt_id, action = unquote(match.group(1)), match.group(2)
            if action == "trash":
                self.handle_trash(prompt_id)
            else:
                self.handle_restore(prompt_id)
            return
        self.send_error_json("unknown endpoint", HTTPStatus.NOT_FOUND)

    def do_PUT(self) -> None:
        parsed = urlparse(self.path)
        match = re.match(r"^/api/prompts/([^/]+)$", parsed.path)
        if match:
            self.handle_update(unquote(match.group(1)))
            return
        self.send_error_json("unknown endpoint", HTTPStatus.NOT_FOUND)

    def do_DELETE(self) -> None:
        parsed = urlparse(self.path)
        match = re.match(r"^/api/prompts/([^/]+)$", parsed.path)
        if match:
            self.handle_delete(unquote(match.group(1)))
            return
        self.send_error_json("unknown endpoint", HTTPStatus.NOT_FOUND)

    def handle_list(self, parsed) -> None:
        query = parse_qs(parsed.query)
        status = query.get("status", ["active"])[0]
        catalog = load_catalog()
        items = []
        for item in catalog.get("items", []):
            if status != "all" and item.get("status", "active") != status:
                continue
            items.append(prompt_payload(item, include_content=True))
        self.send_json({"ok": True, "items": items})

    def handle_get_prompt(self, prompt_id: str) -> None:
        catalog = load_catalog()
        item = find_item(catalog, prompt_id)
        if not item:
            self.send_error_json("prompt not found", HTTPStatus.NOT_FOUND)
            return
        self.send_json({"ok": True, "item": prompt_payload(item, include_content=True)})

    def handle_create(self) -> None:
        data = self.read_body_json()
        title = (data.get("title") or "").strip()
        content = (data.get("content") or "").strip()
        if not title or not content:
            self.send_error_json("title and content are required")
            return
        catalog = load_catalog()
        stage = (data.get("stage") or "general").strip()
        prompt_id = next_id(catalog, stage)
        item = {
            "id": prompt_id,
            "legacy_id": None,
            "status": "active",
            "stage": stage,
            "platform": (data.get("platform") or "通用").strip(),
            "title": title,
            "purpose": (data.get("purpose") or "").strip(),
            "scenario": (data.get("scenario") or "").strip(),
            "tags": data.get("tags") if isinstance(data.get("tags"), list) else [],
            "file": "",
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        path = unique_file_path(prompt_id, title, "active")
        item["file"] = str(path.relative_to(ROOT)).replace("\\", "/")
        path.write_text(render_markdown(item, content, data.get("notes", "")), encoding="utf-8")
        catalog["items"].append(item)
        save_catalog(catalog)
        self.send_json({"ok": True, "item": prompt_payload(item)}, HTTPStatus.CREATED)

    def handle_update(self, prompt_id: str) -> None:
        data = self.read_body_json()
        catalog = load_catalog()
        item = find_item(catalog, prompt_id)
        if not item:
            self.send_error_json("prompt not found", HTTPStatus.NOT_FOUND)
            return
        for field in ["stage", "platform", "title", "purpose", "scenario"]:
            if field in data:
                item[field] = (data.get(field) or "").strip()
        if "tags" in data and isinstance(data["tags"], list):
            item["tags"] = data["tags"]
        item["updated_at"] = now_iso()
        content = (data.get("content") or "").strip()
        notes = (data.get("notes") or "").strip()
        if item.get("file"):
            path = safe_relative_path(item["file"])
        else:
            path = unique_file_path(item["id"], item.get("title", "prompt"), item.get("status", "active"))
            item["file"] = str(path.relative_to(ROOT)).replace("\\", "/")
        path.parent.mkdir(parents=True, exist_ok=True)
        if not content and path.exists():
            content = extract_prompt(path.read_text(encoding="utf-8", errors="replace"))
        path.write_text(render_markdown(item, content, notes), encoding="utf-8")
        save_catalog(catalog)
        self.send_json({"ok": True, "item": prompt_payload(item)})

    def handle_trash(self, prompt_id: str) -> None:
        catalog = load_catalog()
        item = find_item(catalog, prompt_id)
        if not item:
            self.send_error_json("prompt not found", HTTPStatus.NOT_FOUND)
            return
        if item.get("status") == "trash":
            self.send_json({"ok": True, "item": prompt_payload(item)})
            return
        old_path = safe_relative_path(item["file"])
        new_path = TRASH_DIR / old_path.name
        if old_path.exists():
            if new_path.exists():
                new_path = unique_file_path(item["id"], item.get("title", "prompt"), "trash")
            shutil.move(str(old_path), str(new_path))
            item["file"] = str(new_path.relative_to(ROOT)).replace("\\", "/")
        item["status"] = "trash"
        item["deleted_at"] = now_iso()
        item["updated_at"] = now_iso()
        save_catalog(catalog)
        self.send_json({"ok": True, "item": prompt_payload(item)})

    def handle_restore(self, prompt_id: str) -> None:
        catalog = load_catalog()
        item = find_item(catalog, prompt_id)
        if not item:
            self.send_error_json("prompt not found", HTTPStatus.NOT_FOUND)
            return
        old_path = safe_relative_path(item["file"])
        new_path = ACTIVE_DIR / old_path.name
        if old_path.exists():
            if new_path.exists():
                new_path = unique_file_path(item["id"], item.get("title", "prompt"), "active")
            shutil.move(str(old_path), str(new_path))
            item["file"] = str(new_path.relative_to(ROOT)).replace("\\", "/")
        item["status"] = "active"
        item.pop("deleted_at", None)
        item["updated_at"] = now_iso()
        save_catalog(catalog)
        self.send_json({"ok": True, "item": prompt_payload(item)})

    def handle_delete(self, prompt_id: str) -> None:
        catalog = load_catalog()
        item = find_item(catalog, prompt_id)
        if not item:
            self.send_error_json("prompt not found", HTTPStatus.NOT_FOUND)
            return
        if item.get("status") != "trash":
            self.send_error_json("move prompt to trash before permanent delete")
            return
        path = safe_relative_path(item["file"])
        if path.exists():
            path.unlink()
        catalog["items"] = [i for i in catalog.get("items", []) if i is not item]
        save_catalog(catalog)
        self.send_json({"ok": True})

    def serve_static(self, request_path: str) -> None:
        request_path = unquote(request_path.split("?", 1)[0])
        if request_path in ("", "/"):
            path = DASHBOARD_DIR / "index.html"
        elif request_path.startswith("/content-dashboard/"):
            path = (ROOT / request_path.lstrip("/")).resolve()
            content_root = ROOT / "content-dashboard"
            if content_root not in path.parents and path != content_root:
                self.send_error(HTTPStatus.FORBIDDEN)
                return
        elif request_path.startswith("/prompts/") or request_path in {
            "/PROMPT_WORKBENCH.md",
            "/CONTENT_WORKBENCH.md",
            "/candidates.md",
            "/rubric_notes.md",
            "/script_patterns.md",
            "/audience.md",
            "/STATUS.md",
        }:
            path = (ROOT / request_path.lstrip("/")).resolve()
            if ROOT not in path.parents and path != ROOT:
                self.send_error(HTTPStatus.FORBIDDEN)
                return
        else:
            path = (DASHBOARD_DIR / request_path.lstrip("/")).resolve()
            if DASHBOARD_DIR not in path.parents and path != DASHBOARD_DIR:
                self.send_error(HTTPStatus.FORBIDDEN)
                return
        if not path.exists() or path.is_dir():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex((host, port)) != 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    ensure_dirs()
    if not CATALOG_PATH.exists():
        write_json(CATALOG_PATH, {"version": 1, "updated_at": now_iso(), "items": []})
    if not port_available(args.host, args.port):
        print(f"Prompt dashboard already appears to be running on http://{args.host}:{args.port}")
        return
    server = ThreadingHTTPServer((args.host, args.port), PromptHandler)
    print(f"Prompt dashboard running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
