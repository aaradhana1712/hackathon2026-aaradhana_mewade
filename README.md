# 🚀 ShopWave Autonomous Support Agent
**Agentic AI Hackathon 2026 - Official Submission**

### 🚀 LIVE DEMO: [https://hackathon2026-aaradhana-mewade.vercel.app]
### 📹 RECORDED WALKTHROUGH: [Watch Demo Video](https://drive.google.com/file/d/1wJvV5eqKEMrB0E4w08PU2TnrOUyIgDfL/view?usp=sharing)

---

## 🏛️ Project Overview
This project presents a production-grade, autonomous support resolution agent for **ShopWave**. Built on a robust **LangGraph** foundation, the agent is designed to handle hundreds of support tickets simultaneously while maintaining 100% transparency through a professional audit governance hub.

## 🌐 Live Dashboard
- **URL:** [http://127.0.0.1:8002](http://127.0.0.1:8002) (Local Deployment)
- **Status:** Production-Ready | Audit Logs Active

## 🧠 Agent Architecture
Our agent follows a strictly governed **governance-first** loop:
1. **Ingest:** Tickets are ingested from `tickets.json`.
2. **Triage:** Classifies urgency, category, and **visibility** (Internal/External).
3. **Chain Rule:** Executes a mandatory 3-step tool chain (`get_customer` -> `get_order` -> `search_policies`).
4. **Reasoning:** AI evaluates the context with a dynamic **Confidence Score**.
5. **Outcome:** Either resolves autonomously or generates an **Official Handoff Template** for humans.

## 🛠️ Key Technical Features (The 4 Rules)
- **🔗 Chain:** Guaranteed 3+ tool calls per resolution.
- **⚡ Concurrency:** Integrated `asyncio.Semaphore` for parallel processing of 20+ tickets.
- **🛡️ Recover:** Self-healing logic for tool timeouts and malformed data.
- **🔍 Explain:** 100% transparent audit logs for every sub-decision.

## 🏃 Setup & Run
1. Install dependencies: `pip install -r requirements.txt`
2. Set API Key in `.env`: `GOOGLE_API_KEY=your_key`
3. Run Agent Execution: `python main.py`
4. Launch Monitoring Dashboard: `python app.py`

## 🐳 Docker Deployment (Bonus Points)
```bash
docker build -t shopwave-agent .
docker run -p 8002:8002 shopwave-agent
```

## 📝 Challenges Faced (For Hackathon Form)
1. **Concurrency Control:** Balancing high-speed parallel processing with API rate limits was solved using asynchronous semaphores.
2. **Graceful Recovery:** Implementing a fail-safe mechanism for tool timeouts.
3. **Visibility Audit:** Integrating internal/external visibility classification.

---
**Developed with ❤️ by Aaradhana Mewade for the Agentic AI Hackathon 2026.**
