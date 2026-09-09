"""Web Server siêu nhẹ phục vụ Web UI cho Underworld v0 qua Python Standard Library.

Hỗ trợ truy cập từ trình duyệt di động (iOS / iPhone / Safari / Chrome) và máy tính.
"""

import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict
from underworld.composition.world_program import WorldProgram
from underworld.graphics.ui_program import UIProgram
from underworld.interface.administrator import Administrator


class UnderworldWebHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler phục vụ giao diện HTML/CSS/JS và REST Endpoints."""

    world_program: Any = None
    ui_program: Any = None
    admin: Any = None

    def log_message(self, format, *args):
        """Tắt log mặc định của HTTP server để giữ terminal sạch sẽ."""
        pass

    def _send_json(self, data: Dict[str, Any], status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _send_html(self, html_content: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/":
            html = self._render_mobile_web_page()
            self._send_html(html)
        elif path == "/api/state":
            st = self.world_program.get_state()
            payload = self.ui_program.generate_web_presentation(st)
            self._send_json(payload)
        elif path == "/api/step":
            n = int(query.get("n", [1])[0])
            for _ in range(n):
                self.world_program.run_step()
            st = self.world_program.get_state()
            payload = self.ui_program.generate_web_presentation(st)
            self._send_json(payload)
        elif path == "/api/command":
            cmd_type = query.get("type", [""])[0]
            cmd_val = query.get("val", [""])[0]

            if cmd_type == "weather" and cmd_val:
                cmd = self.admin.change_environment("weather", cmd_val)
                self.world_program.world.apply_command(cmd)
                self.world_program.run_step()

            st = self.world_program.get_state()
            payload = self.ui_program.generate_web_presentation(st)
            self._send_json(payload)
        else:
            self._send_json({"error": "Endpoint không tồn tại"}, status=404)

    def _render_mobile_web_page(self) -> str:
        return r"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Underworld v0 — World Graphics Web UI</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-color: #f8fafc;
            --accent-color: #38bdf8;
            --border-color: #334155;
            --btn-bg: #2563eb;
            --btn-hover: #1d4ed8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-color); padding: 12px; font-size: 14px; line-height: 1.5; }
        header { text-align: center; padding: 10px 0 16px 0; border-bottom: 1px solid var(--border-color); margin-bottom: 16px; }
        h1 { font-size: 1.25rem; color: var(--accent-color); margin-bottom: 4px; }
        .subtitle { font-size: 0.8rem; color: #94a3b8; }
        .container { display: flex; flex-direction: column; gap: 12px; max-width: 600px; margin: 0 auto; }
        .module-card { background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 10px; padding: 14px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .module-title { font-size: 0.95rem; font-weight: 600; color: var(--accent-color); margin-bottom: 10px; border-bottom: 1px solid var(--border-color); padding-bottom: 4px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; text-align: center; }
        .stat-box { background-color: #0f172a; padding: 8px; border-radius: 6px; }
        .stat-val { font-size: 1.1rem; font-weight: bold; color: #f1f5f9; }
        .stat-lbl { font-size: 0.75rem; color: #94a3b8; }
        .btn-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 6px; }
        button { background-color: var(--btn-bg); color: white; border: none; padding: 10px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: background 0.2s; }
        button:active { background-color: var(--btn-hover); transform: scale(0.98); }
        table { width: 100%; border-collapse: collapse; font-size: 0.8rem; margin-top: 6px; }
        th, td { padding: 6px; text-align: left; border-bottom: 1px solid var(--border-color); }
        th { color: #94a3b8; font-weight: 600; }
        .log-box { background-color: #020617; color: #38bdf8; font-family: monospace; padding: 10px; border-radius: 6px; font-size: 0.75rem; max-height: 120px; overflow-y: auto; white-space: pre-wrap; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌐 Underworld v0 — Web UI</h1>
            <div class="subtitle">Modules → World → World Program → World Graphics → Web UI</div>
        </header>

        <div id="ui-modules-root">Đang tải giao diện từ World Graphics...</div>
    </div>

    <script>
        async function fetchPresentation() {
            try {
                const res = await fetch('/api/state');
                const data = await res.json();
                renderUI(data);
            } catch (err) {
                console.error("Lỗi tải giao diện:", err);
            }
        }

        async function triggerAction(endpoint) {
            try {
                const res = await fetch(endpoint);
                const data = await res.json();
                renderUI(data);
            } catch (err) {
                console.error("Lỗi thực thi hành động:", err);
            }
        }

        function renderUI(presentation) {
            const root = document.getElementById('ui-modules-root');
            root.innerHTML = '';

            presentation.modules.forEach(mod => {
                const card = document.createElement('div');
                card.className = 'module-card';

                const title = document.createElement('div');
                title.className = 'module-title';
                title.innerText = mod.title;
                card.appendChild(title);

                if (mod.type === 'world_state_summary') {
                    const d = mod.data;
                    card.innerHTML += `
                        <div class="grid-3">
                            <div class="stat-box"><div class="stat-val">${d.tick}</div><div class="stat-lbl">⏱️ Tick</div></div>
                            <div class="stat-box"><div class="stat-val">${d.weather}</div><div class="stat-lbl">🌤️ Thời tiết</div></div>
                            <div class="stat-box"><div class="stat-val">${d.humans_count}</div><div class="stat-lbl">👥 Con người</div></div>
                        </div>
                    `;
                } else if (mod.type === 'control_panel') {
                    const btnGrid = document.createElement('div');
                    btnGrid.className = 'btn-grid';
                    mod.data.actions.forEach(act => {
                        const btn = document.createElement('button');
                        btn.innerText = act.label;
                        btn.onclick = () => triggerAction(act.endpoint);
                        btnGrid.appendChild(btn);
                    });
                    card.appendChild(btnGrid);
                } else if (mod.type === 'entity_table') {
                    let html = `<table><thead><tr><th>ID</th><th>Vị trí</th><th>Năng lượng</th><th>Đói</th><th>Hành động</th></tr></thead><tbody>`;
                    mod.data.entities.forEach(e => {
                        html += `<tr><td><b>${e.id}</b></td><td>(${e.position.join(',')})</td><td>${e.energy}</td><td>${e.hunger}</td><td>${e.last_action}</td></tr>`;
                    });
                    html += `</tbody></table>`;
                    card.innerHTML += html;
                } else if (mod.type === 'event_list') {
                    if (mod.data.events.length === 0) {
                        card.innerHTML += `<div style="color:#94a3b8; font-style:italic; font-size:0.8rem;">Không có sự kiện đặc biệt nào đang diễn ra.</div>`;
                    } else {
                        let html = `<table><thead><tr><th>Loại</th><th>Chi tiết</th></tr></thead><tbody>`;
                        mod.data.events.forEach(evt => {
                            html += `<tr><td>${evt.type}</td><td>${evt.detail}</td></tr>`;
                        });
                        html += `</tbody></table>`;
                        card.innerHTML += html;
                    }
                } else if (mod.type === 'timeline_log') {
                    const logBox = document.createElement('div');
                    logBox.className = 'log-box';
                    logBox.innerText = mod.data.log_lines.join('\n');
                    card.appendChild(logBox);
                }

                root.appendChild(card);
            });
        }

        // Tải giao diện ban đầu
        fetchPresentation();
    </script>
</body>
</html>"""


def start_web_server(
    world_program: WorldProgram,
    ui_program: UIProgram,
    admin: Administrator,
    host: str = "0.0.0.0",
    port: int = 8000
) -> HTTPServer:
    """Khởi tạo và lắng nghe Web Server siêu nhẹ."""
    UnderworldWebHandler.world_program = world_program
    UnderworldWebHandler.ui_program = ui_program
    UnderworldWebHandler.admin = admin

    server = HTTPServer((host, port), UnderworldWebHandler)
    return server
