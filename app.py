from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    tickets_items = []
    stats = {"resolved": 0, "escalated": 0, "total": 0, "recovered": 0}
    try:
        if os.path.exists("audit_log.json"):
            with open("audit_log.json", "r") as f:
                audit_data = json.load(f)
                temp_tickets = {}
                for entry in audit_data:
                    tid = entry.get("ticket_id", "Unknown")
                    if tid not in temp_tickets:
                        temp_tickets[tid] = {"logs": [], "priority": "NORMAL", "status": "RESOLVED", "conf": "0", "visibility": "External"}
                    
                    msg = entry.get("data", "").lower()
                    if any(x in msg for x in ["retrying", "recovered", "timeout"]): stats["recovered"] += 1
                    
                    temp_tickets[tid]["logs"].append(entry)
                    if entry.get("type") == "TRIAGE":
                        if "high" in msg: temp_tickets[tid]["priority"] = "HIGH"
                        if "internal" in msg: temp_tickets[tid]["visibility"] = "Internal"
                    if entry.get("type") == "CONFIDENCE":
                        try: temp_tickets[tid]["conf"] = entry.get("data", "").split(": ")[1].replace("%","")
                        except: pass
                    if entry.get("type") == "FINAL_ACTION":
                        stats["resolved"] += 1; stats["total"] += 1
                        temp_tickets[tid]["status"] = "RESOLVED"
                    elif entry.get("type") == "HANDOFF":
                        stats["escalated"] += 1; stats["total"] += 1
                        temp_tickets[tid]["status"] = "ESCALATED"
                
                def sort_key(k):
                    try: return int(k.split('-')[1])
                    except: return 999
                tickets_items = sorted(temp_tickets.items(), key=lambda x: sort_key(x[0]))
    except: pass

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>ShopWave | Mission Control</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <style>
            :root { 
                --bg: #020b12; --card: #0a1622; --border: #1a2e3f;
                --accent: #38bdf8; --success: #10b981; --warn: #f59e0b;
                --text-main: #f3f4f6; --text-muted: #9ca3af;
                --font-main: 'Plus Jakarta Sans', sans-serif; --font-mono: 'JetBrains Mono', monospace;
            }
            
            body, html { height: 100vh; margin:0; background: var(--bg); color: var(--text-main); font-family: var(--font-main); overflow: hidden; }

            .grid-overlay {
                position: fixed; inset: 0; pointer-events: none; z-index: -1;
                background-image: radial-gradient(circle at 2px 2px, rgba(56, 189, 248, 0.05) 1px, transparent 0);
                background-size: 30px 30px;
            }

            .app-container { display: grid; grid-template-columns: 380px 1fr; height: 100vh; }

            .sidebar { 
                background: #020b12; border-right: 1px solid var(--border); 
                padding: 30px; display: flex; flex-direction: column; overflow-y: auto;
            }

            .sys-brand { font-size: 1.1rem; font-weight: 800; display: flex; align-items: center; gap: 10px; margin-bottom: 30px; }
            .sys-brand span { color: var(--accent); }

            .stat-box { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 25px; }
            .stat-p { background: rgba(56, 189, 248, 0.03); border: 1px solid var(--border); padding: 14px; border-radius: 12px; }
            .stat-p-lbl { font-size: 0.55rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; }
            .stat-p-val { font-size: 1rem; font-weight: 700; color: #fff; font-family: var(--font-mono); }

            .diagram-header { font-size: 0.65rem; font-weight: 800; color: var(--accent); margin-bottom: 12px; opacity: 0.7; letter-spacing: 1px; }
            
            /* Professional Architecture Container */
            .diag-wrap { 
                background: white; border-radius: 16px; padding: 15px; 
                margin-bottom: 25px; border: 1px solid var(--accent);
                box-shadow: 0 10px 40px rgba(0,0,0,0.4);
            }
            .mermaid svg { width: 100% !important; height: auto !important; }

            .console-card {
                background: #000; border-radius: 10px; padding: 12px;
                font-family: var(--font-mono); font-size: 0.6rem; color: #4ade80;
                border: 1px solid #22c55e22; line-height: 1.5;
            }

            .feed-area { padding: 40px; overflow-y: auto; height: 100vh; padding-bottom: 200px; }
            
            .ticket-card { 
                background: var(--card); border: 1px solid var(--border); border-radius: 20px;
                margin-bottom: 25px; transition: 0.3s ease-out;
            }
            .ticket-card:hover { border-color: var(--accent); transform: translateY(-3px); }

            .node-head { 
                padding: 22px 30px; border-bottom: 1px solid var(--border); 
                display: flex; justify-content: space-between; align-items: center;
                background: rgba(255,255,255,0.01);
            }

            .audit-body { padding: 10px 30px 25px 30px; }
            .audit-ln { 
                display: grid; grid-template-columns: 130px 1fr; gap: 20px; padding: 10px 0;
                border-bottom: 1px solid rgba(255,255,255,0.02);
            }
            .type-tag { font-family: var(--font-mono); font-size: 0.65rem; font-weight: 700; color: var(--accent); text-transform: uppercase; }
            .data-txt { font-size: 0.85rem; color: #cbd5e1; line-height: 1.6; }

            .conf-pill {
                background: rgba(16, 185, 129, 0.1); color: var(--success);
                font-family: var(--font-mono); font-size: 0.65rem; padding: 4px 12px; border-radius: 50px;
                border: 1px solid rgba(16, 185, 129, 0.2);
            }

            .v-badge { font-size: 0.65rem; font-weight: 800; background: rgba(56, 189, 248, 0.1); color: var(--accent); padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.2); }

            ::-webkit-scrollbar { width: 4px; }
            ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="grid-overlay"></div>
        <div class="app-container">
            <div class="sidebar">
                <div class="sys-brand">
                    <i class="fas fa-microchip"></i>
                    ShopWave <span>Mission Control</span>
                </div>

                <div class="stat-box">
                    <div class="stat-p"><div class="stat-p-lbl">RESOLVED</div><div class="stat-p-val">{{ stats.resolved }}</div></div>
                    <div class="stat-p"><div class="stat-p-lbl">ESCALATED</div><div class="stat-p-val text-warning">{{ stats.escalated }}</div></div>
                </div>

                <div class="diagram-header">SYSTEM ARCHITECTURE Flow</div>
                <div class="diag-wrap">
                    <div class="mermaid">
                        graph TD
                            A([Ticket Ingest]) --> B[Triage Logic]
                            B --> C{Agentic Gate}
                            C --> D[Tool Chain]
                            D --> E[(Audit Hub)]
                            
                            style A fill:#f3f4f6,stroke:#333
                            style E fill:#0ea5e9,color:#fff,stroke-width:2px
                            linkStyle default stroke:#38bdf8,stroke-width:2px,curve:basis
                    </div>
                </div>

                <div class="diagram-header">LIVE_CONSOLE_LOGS</div>
                <div class="console-card">
                    > SYSTEM_STATUS: CONNECTED<br>
                    > CONCURRENCY: ACTIVE (THREAD_20)<br>
                    > RULE_RECOVERY: ENGAGED<br>
                    > DATA_PERSISTENCE: 100%
                </div>
            </div>

            <div class="feed-area">
                <div class="d-flex justify-content-between align-items-center mb-5">
                    <div>
                        <h3 class="fw-bold mb-1">Official Support Audit Log</h3>
                        <p class="text-muted small mb-0">Traceability of autonomous agentic decisions and tool calls.</p>
                    </div>
                    <div class="v-badge">SOC MONITOR ACTIVE</div>
                </div>

                {% for tid, t_data in tickets_items %}
                <div class="ticket-card">
                    <div class="node-head">
                        <div class="d-flex align-items-center gap-3">
                            <span class="fw-bold" style="font-size:1.1rem; color:#fff;">{{ tid }}</span>
                            <span class="v-badge">{{ t_data.visibility }}</span>
                        </div>
                        <div class="d-flex align-items-center gap-3">
                            {% if t_data.conf != "0" %}
                            <div class="conf-pill">CONFIDENCE: {{ t_data.conf }}.0%</div>
                            {% endif %}
                            <span class="fw-bold small" style="color:{{ 'var(--success)' if t_data.status == 'RESOLVED' else 'var(--warn)' }}">
                                {{ t_data.status }}
                            </span>
                        </div>
                    </div>
                    <div class="audit-body">
                        {% for log in t_data.logs %}
                        <div class="audit-ln">
                            <span class="type-tag">{{ log.type }}</span>
                            <span class="data-txt">{{ log.data }}</span>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        <script>
            mermaid.initialize({ startOnLoad: true, theme: 'neutral', fontFamily: 'Plus Jakarta Sans' });
        </script>
    </body>
    </html>
    """
    from jinja2 import Template
    return Template(html_content).render(tickets_items=tickets_items, stats=stats)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
