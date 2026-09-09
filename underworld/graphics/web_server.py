"""Web Server siêu nhẹ phục vụ Web UI cho Underworld v0 qua Python Standard Library.

Hỗ trợ truy cập từ trình duyệt di động (iOS / iPhone / Safari / Chrome) và máy tính.
Cài đặt tuân thủ tuyệt đối ranh giới Presentation Layer:
  - KHÔNG biến đổi (mutate) World trực tiếp.
  - Mọi tương tác điều khiển đều gửi lệnh `AdministratorCommand` tới Administrator.
  - Hỗ trợ Background Thread tự động tick nhịp 1 giây khi bật Auto-Run có Thread Lock đồng bộ.
  - In log hoạt động thế giới thời gian thực ra Console/Terminal song song với Web UI.
"""

import json
import time
import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Dict
from underworld.composition.world_program import WorldProgram
from underworld.graphics.ui_program import UIProgram
from underworld.interface.administrator import Administrator


class UnderworldWebHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler phục vụ giao diện HTML/CSS/JS hiện đại và REST Endpoints."""

    world_program: Any = None
    ui_program: Any = None
    admin: Any = None
    auto_run_active: bool = False
    _auto_thread: Any = None
    _step_lock = threading.Lock()

    def log_message(self, format, *args):
        """Tắt log mặc định của HTTP server để giữ terminal sạch sẽ."""
        pass

    @classmethod
    def _start_auto_run_thread(cls):
        """Khởi chạy Background Thread tự động tick mỗi 1 giây có Thread Lock đồng bộ."""
        if cls._auto_thread is not None and cls._auto_thread.is_alive():
            return

        def auto_ticker():
            while True:
                if cls.auto_run_active and cls.world_program and cls.admin:
                    with cls._step_lock:
                        cls.world_program.run_step(administrator=cls.admin)
                        st = cls.world_program.get_state()
                    tick = st.get("time_step", 0)
                    env = st.get("environment", {})
                    weather = env.get("weather", "N/A")
                    humans_cnt = len(st.get("human_states", st.get("humans", {})))
                    print(f" [NHỊP TỰ VẬN HÀNH 1S] Auto-Tick -> [Tick {tick}] Thời tiết: {weather} | Con người: {humans_cnt} cá thể")
                time.sleep(1.0)

        cls._auto_thread = threading.Thread(target=auto_ticker, daemon=True)
        cls._auto_thread.start()

    def _log_console_activity(self, action_desc: str, state: Dict[str, Any]):
        """In log hoạt động thời gian thực của thế giới ra Terminal/Console."""
        tick = state.get("time_step", 0)
        env = state.get("environment", {})
        weather = env.get("weather", "N/A")
        humans_cnt = len(state.get("human_states", state.get("humans", {})))
        events = state.get("events", [])

        print(f" [WEB UI LOG] {action_desc} -> [Tick {tick}] Thời tiết: {weather} | Con người: {humans_cnt} cá thể | Sự kiện bước này: {len(events)}")
        if events:
            for evt in events:
                print(f"               ⚡ Event: {evt.get('type')} - {evt.get('chi_tiết')}")

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
            with self.__class__._step_lock:
                st = self.world_program.get_state()
            payload = self.ui_program.generate_web_presentation(st)
            payload["auto_run"] = self.__class__.auto_run_active
            self._send_json(payload)
        elif path == "/api/auto_toggle":
            with self.__class__._step_lock:
                self.__class__.auto_run_active = not self.__class__.auto_run_active
                st = self.world_program.get_state()
            status_str = "BẬT" if self.__class__.auto_run_active else "TẮT"
            self._log_console_activity(f"Quản trị viên {status_str} chế độ Tự vận hành 1s", st)
            payload = self.ui_program.generate_web_presentation(st)
            payload["auto_run"] = self.__class__.auto_run_active
            self._send_json(payload)
        elif path == "/api/step":
            n = int(query.get("n", [1])[0])
            with self.__class__._step_lock:
                for _ in range(n):
                    self.world_program.run_step(administrator=self.admin)
                st = self.world_program.get_state()
            self._log_console_activity(f"Thực hiện chạy {n} tick(s)", st)
            payload = self.ui_program.generate_web_presentation(st)
            payload["auto_run"] = self.__class__.auto_run_active
            self._send_json(payload)
        elif path == "/api/command":
            cmd_type = query.get("type", [""])[0]
            cmd_val = query.get("val", [""])[0]

            with self.__class__._step_lock:
                if cmd_type == "weather" and cmd_val:
                    self.admin.change_environment("weather", cmd_val)
                    self.world_program.run_step(administrator=self.admin)
                    action_msg = f"Quản trị viên đổi thời tiết thành '{cmd_val}'"
                elif cmd_type == "create_human":
                    self.admin.create_human()
                    self.world_program.run_step(administrator=self.admin)
                    action_msg = "Quản trị viên tạo con người mới"
                elif cmd_type == "disaster" and cmd_val:
                    self.admin.trigger_disaster(cmd_val)
                    self.world_program.run_step(administrator=self.admin)
                    action_msg = f"Quản trị viên kích hoạt thiên tai '{cmd_val}'"
                else:
                    self.world_program.run_step(administrator=self.admin)
                    action_msg = "Chạy 1 tick mô phỏng"

                st = self.world_program.get_state()

            self._log_console_activity(action_msg, st)
            payload = self.ui_program.generate_web_presentation(st)
            payload["auto_run"] = self.__class__.auto_run_active
            self._send_json(payload)
        else:
            self._send_json({"error": "Endpoint không tồn tại"}, status=404)

    def _render_mobile_web_page(self) -> str:
        return """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Underworld v0 — Modern World Graphics Web UI</title>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: #151d30;
            --card-border: #23304c;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --primary: #38bdf8;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --accent-purple: #a855f7;
            --btn-bg: #1e293b;
            --btn-border: #334155;
            --btn-hover: #334155;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); padding: 12px; font-size: 14px; line-height: 1.5; }

        header {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 12px 16px;
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }
        h1 { font-size: 1.25rem; font-weight: 700; color: var(--primary); letter-spacing: -0.02em; margin-bottom: 2px; }
        .subtitle { font-size: 0.78rem; color: var(--text-sub); }
        .live-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.72rem;
            font-weight: 600;
            margin-top: 6px;
            text-transform: uppercase;
        }
        .badge-pulse { width: 8px; height: 8px; border-radius: 50%; background-color: var(--accent-green); animation: pulse 1.5s infinite; }
        .live-badge.off .badge-pulse { background-color: var(--text-sub); animation: none; }
        .live-badge.on { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); border: 1px solid rgba(16, 185, 129, 0.3); }
        .live-badge.off { background: rgba(148, 163, 184, 0.1); color: var(--text-sub); border: 1px solid rgba(148, 163, 184, 0.2); }
        @keyframes pulse { 0% { opacity: 0.3; transform: scale(0.9); } 50% { opacity: 1; transform: scale(1.15); } 100% { opacity: 0.3; transform: scale(0.9); } }

        .container { display: flex; flex-direction: column; gap: 12px; max-width: 650px; margin: 0 auto; }

        .module-card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 14px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .module-title {
            font-size: 0.92rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 6px;
        }

        /* World State Grid */
        .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
        .stat-box { background: #0c121e; border: 1px solid var(--card-border); padding: 10px; border-radius: 8px; text-align: center; }
        .stat-val { font-size: 1.15rem; font-weight: 800; color: #ffffff; }
        .stat-lbl { font-size: 0.72rem; color: var(--text-sub); margin-top: 2px; }

        /* Control Panel Buttons */
        .btn-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
        button {
            background-color: var(--btn-bg);
            color: var(--text-main);
            border: 1px solid var(--btn-border);
            padding: 10px 8px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        button:hover { background-color: var(--btn-hover); border-color: var(--primary); }
        button:active { transform: scale(0.97); }
        button.active-mode { background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: white; border: none; box-shadow: 0 0 10px rgba(16, 185, 129, 0.4); }

        /* Entity Cards / Table */
        .entity-card { background: #0c121e; border: 1px solid var(--card-border); border-radius: 8px; padding: 10px; margin-bottom: 8px; }
        .entity-card:last-child { margin-bottom: 0; }
        .entity-header { display: flex; justify-content: space-between; font-weight: 700; color: #f1f5f9; font-size: 0.85rem; margin-bottom: 6px; }
        .progress-bar { width: 100%; height: 6px; background-color: #1e293b; border-radius: 3px; overflow: hidden; margin-top: 3px; }
        .progress-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease; }
        .fill-energy { background-color: var(--primary); }
        .fill-hunger { background-color: var(--accent-amber); }
        .entity-status { font-size: 0.75rem; color: var(--text-sub); margin-top: 6px; }

        /* Event Tag Styles */
        .event-item { padding: 6px 8px; border-radius: 6px; background-color: #0c121e; border: 1px solid var(--card-border); margin-bottom: 6px; font-size: 0.78rem; }
        .event-type-tag { font-weight: 700; padding: 2px 6px; border-radius: 4px; font-size: 0.7rem; margin-right: 6px; display: inline-block; }
        .tag-disaster { background-color: rgba(239, 68, 68, 0.2); color: var(--accent-red); border: 1px solid rgba(239, 68, 68, 0.4); }
        .tag-admin { background-color: rgba(168, 85, 247, 0.2); color: var(--accent-purple); border: 1px solid rgba(168, 85, 247, 0.4); }
        .tag-auto { background-color: rgba(56, 189, 248, 0.2); color: var(--primary); border: 1px solid rgba(56, 189, 248, 0.4); }

        .log-box { background-color: #030712; color: #38bdf8; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; padding: 10px; border-radius: 8px; font-size: 0.75rem; max-height: 140px; overflow-y: auto; white-space: pre-wrap; border: 1px solid var(--card-border); }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌐 Underworld v0 — Web UI</h1>
            <div class="subtitle">Thế Giới Tự Vận Hành Nhịp 1s | iOS & Mobile Responsive</div>
            <div id="status-badge" class="live-badge off">
                <span class="badge-pulse"></span>
                <span id="badge-text">Auto 1s: TẠM DỪNG</span>
            </div>
        </header>

        <div id="ui-modules-root">Đang tải giao diện từ World Graphics...</div>
    </div>

    <script>
        let isAutoRun = false;

        async function fetchPresentation() {
            try {
                const res = await fetch('/api/state');
                const data = await res.json();
                isAutoRun = data.auto_run || false;
                updateBadge();
                renderUI(data);
            } catch (err) {
                console.error("Lỗi tải giao diện:", err);
            }
        }

        async function triggerAction(endpoint) {
            try {
                const res = await fetch(endpoint);
                const data = await res.json();
                isAutoRun = data.auto_run || false;
                updateBadge();
                renderUI(data);
            } catch (err) {
                console.error("Lỗi thực thi hành động:", err);
            }
        }

        function updateBadge() {
            const badge = document.getElementById('status-badge');
            const badgeText = document.getElementById('badge-text');
            if (isAutoRun) {
                badge.className = 'live-badge on';
                badgeText.innerText = 'Auto 1s: ĐANG CHẠY';
            } else {
                badge.className = 'live-badge off';
                badgeText.innerText = 'Auto 1s: TẠM DỪNG';
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
                        <div class="stat-grid">
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
                        if (act.id === 'auto_2s' && isAutoRun) {
                            btn.innerText = '⏸️ Tắt Auto 1s';
                            btn.classList.add('active-mode');
                        }
                        btn.onclick = () => triggerAction(act.endpoint);
                        btnGrid.appendChild(btn);
                    });
                    card.appendChild(btnGrid);
                } else if (mod.type === 'entity_table') {
                    mod.data.entities.forEach(e => {
                        const eCard = document.createElement('div');
                        eCard.className = 'entity-card';
                        eCard.innerHTML = `
                            <div class="entity-header">
                                <span>👤 ${e.id}</span>
                                <span>📍 Vị trí: (${e.position.join(', ')})</span>
                            </div>
                            <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:2px;">Năng lượng: ${e.energy}%</div>
                            <div class="progress-bar"><div class="progress-fill fill-energy" style="width: ${Math.min(100, Math.max(0, e.energy))}%;"></div></div>
                            <div style="font-size:0.75rem; color:#94a3b8; margin-top:4px; margin-bottom:2px;">Mức đói: ${e.hunger}%</div>
                            <div class="progress-bar"><div class="progress-fill fill-hunger" style="width: ${Math.min(100, Math.max(0, e.hunger))}%;"></div></div>
                            <div class="entity-status">💬 Hành động: <b>${e.last_action}</b></div>
                        `;
                        card.appendChild(eCard);
                    });
                } else if (mod.type === 'event_list') {
                    if (mod.data.events.length === 0) {
                        card.innerHTML += `<div style="color:#94a3b8; font-style:italic; font-size:0.8rem;">Không có sự kiện đặc biệt nào đang diễn ra.</div>`;
                    } else {
                        mod.data.events.forEach(evt => {
                            let tagClass = 'tag-auto';
                            if (evt.type === 'SU_KIEN_THIEN_TAI') tagClass = 'tag-disaster';
                            else if (evt.type === 'SU_KIEN_QUAN_TRI') tagClass = 'tag-admin';

                            const item = document.createElement('div');
                            item.className = 'event-item';
                            item.innerHTML = `<span class="event-type-tag ${tagClass}">${evt.type}</span>${evt.detail}`;
                            card.appendChild(item);
                        });
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

        // Tự động poll làm mới trạng thái mỗi 1 giây
        setInterval(fetchPresentation, 1000);
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
    """Khởi tạo và lắng hệ Web Server siêu nhẹ."""
    UnderworldWebHandler.world_program = world_program
    UnderworldWebHandler.ui_program = ui_program
    UnderworldWebHandler.admin = admin
    UnderworldWebHandler._start_auto_run_thread()

    server = HTTPServer((host, port), UnderworldWebHandler)
    return server
