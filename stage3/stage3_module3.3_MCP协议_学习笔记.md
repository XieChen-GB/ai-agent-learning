# Stage 3 Module 3.3：MCP 协议 学习笔记

## 一、MCP 是什么，为什么需要它

AI 应用要连各种外部工具（文件系统、数据库、邮件……），以前每一对"AI 应用 × 工具"都要单独写对接代码，M 个应用 × N 个工具 = M×N 套代码，重复劳动、互不兼容。

MCP（Model Context Protocol）是 Anthropic 2024 年 11 月发布的开放协议，把 M×N 变成 M+N：
- 工具开发者只写一次 MCP Server
- AI 应用只实现一次 MCP Client
- 两边按统一协议握手，就能互相调用

类比：USB 接口让各种设备都能连电脑，MCP 让各种工具都能连 AI 应用。

---

## 二、三个角色：Host / Client / Server

不是简单的两方关系，是三层：

| 角色 | 是什么 | 举例 |
|------|--------|------|
| **Host** | AI 应用本体，管理对话、调用 LLM、决定何时用工具 | Claude Desktop、Claude Code |
| **Client** | 活在 Host 内部的组件，跟某一个 Server 维持 1:1 连接 | Host 连了 3 个 Server → 内部有 3 个 Client |
| **Server** | 独立的程序，对外暴露能力（读文件、查数据库……） | filesystem server、自己写的 server |

---

## 三、通信基础：JSON-RPC 2.0

MCP 底层用 JSON-RPC 2.0——用 JSON 格式发送函数调用请求的轻量协议，不是 MCP 自创的。

一次工具调用本质上就是这样一条 JSON：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "read_meeting_folder",
    "arguments": {"path": "/Users/xiechen/meetings"}
  }
}
```

- `method`：协议方法名（这里是"调用工具"）
- `params`：参数
- `id`：匹配请求和响应用的（异步场景下可能同时有多个请求，靠 id 对应）

**写代码时不用手写这些 JSON**，SDK 会封装，但理解这一层，出问题时知道去哪排查。

---

## 四、Server 暴露的三种能力（Primitives）

| 能力 | 是什么 | 判断依据 |
|------|--------|----------|
| **Tool** | 可执行的动作，模型主动决定要不要调用 | 需要模型来判断"用不用" |
| **Resource** | 只读数据，直接当背景资料给模型，不需要模型决策 | 不需要模型判断，直接喂给它 |
| **Prompt** | 预写好的提示词模板，用户选用 | 填参数就能生成的模板 |

**实际例子：**
- "主动判断要不要去读取会议录音" → Tool
- "把已有的会议纪要全文直接作为背景资料" → Resource

---

## 五、Transport：连接方式

| 方式 | 场景 | 说明 |
|------|------|------|
| **stdio** | Server 在本地 | 通过进程的标准输入输出通信，没网络没端口，快 |
| **Streamable HTTP** | Server 在远程 | 通过 HTTP 连接，支持流式响应 |

本地开发用 stdio，云端部署用 Streamable HTTP。

---

## 六、版本现状

- 当前稳定规范版本：**2025-11-25**（我们学的这一版）
- 协议已捐赠给 Linux Foundation 旗下 Agentic AI Foundation
- 下一版（2026-07-28）的 RC 已放出，但正式版要 7 月 28 日才发布
- Python SDK 固定版本：`mcp[cli]==1.28.0`（v2 还在 alpha，避免被升级）

---

## 七、MCP Server 生态：不用都自己写

现成的 Server 有三类来源：

| 来源 | 说明 | 数量 |
|------|------|------|
| **官方参考服务器** | Anthropic 维护，Filesystem、Git、Memory 等 | 7 个活跃 |
| **厂商维护** | GitHub、Slack、Stripe 等官方出的 | 约 50 个 |
| **社区贡献** | MCP Registry、PulseMCP、Smithery 上搜到的 | 几千个，质量参差不齐 |

**关键教训：**
- 官方 Postgres Server（`@modelcontextprotocol/server-postgres`）已被废弃、有 SQL 注入漏洞，不要用
- 被移到 `servers-archived` 仓库的都是废弃的，网上很多教程还在指着这些教人装
- 社区 Server 用之前要自己读代码或看清楚它声明了哪些权限
- 推荐替代：Supabase 官方版、`crystaldba/postgres-mcp`、pgEdge 企业版

**自己写 Server 的真正场景：** 不是重新发明"读文件"这种轮子，而是在通用能力之上叠加自己专有的业务逻辑，或暴露别人没有的私有数据源。

---

## 八、Python SDK：FastMCP

FastMCP 不是协议，是一个 Python 工具（类），帮你把普通函数自动包装成符合 MCP 协议格式的 Tool。类比：MCP 是交通规则，FastMCP 是教练。

写法和 FastAPI 几乎一样：

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo-server")     # 相当于 FastAPI 的 app = FastAPI()

@mcp.tool()                      # 相当于 @app.get(...)
def add(a: int, b: int) -> int:
    """两数相加"""               # 这行会被发给 AI 模型，模型靠它判断工具用途
    return a + b

if __name__ == "__main__":
    mcp.run()                    # 启动 Server，开始监听请求
```

**三个决定 Tool 能不能被模型正确调用的东西：**
1. 函数名
2. 参数类型注解（`a: int`）
3. docstring（`"""两数相加"""`）——会被原样发给模型

---

## 九、环境搭建与工具

### 安装的东西

| 工具 | 命令 | 作用 |
|------|------|------|
| MCP Python SDK | `pip install "mcp[cli]==1.28.0"` | 协议核心 + 命令行工具（dev/run/install） |
| uv | `brew install uv` | 新一代 Python 包管理工具，`mcp dev` 依赖它启动 Server |

### venv、pip、uv 的关系

- **venv**：Python 自带，作用是建一个隔离的环境（盖房间）
- **pip**：往环境里装包（往房间搬东西）
- **uv**：把 venv 建环境 + pip 装包合并成一个工具，速度快几十倍

现在两套并存：stage3 日常开发继续用 pip + venv，`mcp dev` 这种场景让 uv 自己管。

---

## 十、实操验证流程

### 第一步：Inspector 测试（验证 Server 本身没问题）

```bash
mcp dev 04_mcp_server_demo.py
```

- `mcp`：命令行程序本体
- `dev`：子命令，启动 Inspector 调试界面
- `04_mcp_server_demo.py`：要测试的 Server 文件

Inspector 是个网页，在浏览器里手动输入参数、点按钮调用 Tool、看结果。不需要 Claude Desktop 参与。目的：把"Server 本身对不对"和"Claude Desktop 接入对不对"两个问题分开排查。

**注意：** 点 Connect 那一刻 Server 才真正启动，不是命令一跑就启动了。

### 第二步：接入 Claude Desktop

```bash
mcp install 04_mcp_server_demo.py
```

这条命令往 Claude Desktop 的配置文件里加一条记录，告诉 Claude Desktop 去哪找这个 Server、用什么命令启动。配置文件固定路径：

```
/Users/xiechen/Library/Application Support/Claude/claude_desktop_config.json
```

Anthropic 定死的路径，`mcp install` 提前知道这个位置。

安装后必须**完全退出 Claude Desktop 再重新打开**，配置文件只在启动时读一次。

### 第三步：Claude Desktop 里实测

在新对话里对 Claude 说"帮我用 add 工具算一下 7 加 8"，Claude 调用了 demo-server 的 add 工具，返回 15。✅

### 卸载

官方没有 `mcp uninstall` 命令。删除方式：手动编辑配置文件，把对应的 Server 那块 JSON 删掉，重启 Claude Desktop。

---

## 十一、下一步

开新会话，写真正的练习：读取本地会议录音文件夹的 MCP Server。
