# AI Agent 学习项目

## 项目简介
个人 AI Agent 学习项目，按阶段（week/stage）组织，涵盖 RAG、LangChain、LangSmith、MCP 协议等主题。

## 目录结构
- `week1~6/` — Python 基础阶段（语法、数据结构、函数模块、文件/JSON/异常、OOP、异步）
- `fastapi-basics/` — FastAPI 基础练习（GET/POST、Pydantic、Ollama 集成）
- `stage2/` — AI 入门基础：Prompt Engineering、Function Calling、状态管理、Gemini API 首次调用
- `stage3/` — 核心技能：RAG/ChromaDB、LangSmith 追踪、MCP Server、Agent 调试与评估
- `stage4/` — 当前阶段，进阶实战：多 Agent 系统（LangGraph）、Claude Haiku API
- `学习计划.md` — 完整学习路线参考（各阶段目标与练习）

## 技术栈
- Python 3.x
- Ollama（本地模型，qwen2.5）/ Google Gemini API（免费层）
- ChromaDB（本地向量数据库，RAG）
- LangChain / LangSmith（追踪调试）/ LangGraph
- MCP 协议（mcp[cli]，自定义 MCP Server）
- FastAPI

## 约定
- 代码注释和回复均使用中文
- 每个 stage 下有独立的 `venv` 虚拟环境
- 各 stage 下的 `.env`（API Key 等密钥）不提交，已在根 `.gitignore` 中忽略

