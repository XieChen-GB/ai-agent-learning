# 练习：写一个会议录音 MCP Server

from mcp.server.fastmcp import FastMCP  # claude MCP Server 框架                          # 文件系统操作
from pathlib import Path                # 现代的路径处理工具，比字符串拼路径更安全
from datetime import datetime           # 把时间戳转成人类可读的日期格式

# ── 配置 ──────────────────────────────────────────────────────────────
# 常量 RECORDINGS_DIR = 音频文件存储路径
# __file__ 是当前脚本自身的路径
# .parent 取父目录，即 stage3/
# / "recordings" 拼接子目录名（Path 重载了 / 运算符，专门用于路径拼接）
RECORDINGS_DIR = Path(__file__).parent/"recordings"

# 常量 AUDIO_EXTENSIONS = 处理文件的格式
AUDIO_EXTENSIONS = {".mp3", ".mp4", ".m4a", ".wav", ".ogg", ".aac"}

# ── 初始化 MCP Server ──────────────────────────────────────────────────
# 创建FastMCP的实例
mcp = FastMCP(name="meeting-recordings") 

# ── Tool 1：列出所有录音 ───────────────────────────────────────────────

@mcp.tool()
def list_recordings() -> str:
    """列出会议录音文件夹内的所有录音文件，按时间倒序排列"""

    # 检查文件夹是否存在, 不存在则返回
    if not RECORDINGS_DIR.exists():
        return f"录音文件夹不存在：{RECORDINGS_DIR}\n请先创建该文件夹"

    # 将文件夹下所有音频文件路径信息(Path的对象)放入files
    files = [
        f for f in RECORDINGS_DIR.iterdir() if f.is_file() 
        and  f.suffix.lower() in AUDIO_EXTENSIONS
    ]
    # iterdir() 遍历目录下所有条目
    # iterdir() 属于 pathlib 的 Path 对象，返回文件夹里每一项（文件和子文件夹）的路径对象。
    # 返回例子： ecordings/meeting.mp3
    # f.is_file() 是文件返回Ture

    # f.suffix   ".mp3"  ← 包含点号 
    # f.name    "meeting.mp3" 
    # f.stem    "meeting" ← 去掉扩展名的文件名



    if not files:   #files为空时False
        return "录音文件夹存在，但没有找到任何录音文件。"
    
    #按修改时间排序files
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True) 
    # stat() 是 Path 对象的方法，返回文件的元数据，常用的属性有：
        # st_size           size                文件大小（字节）
        # st_mtime          modification time   最后修改时间
        # st_ctime          change time         Mac/Linux：元数据修改时间 / Windows：创建时间
        # st_atime          access time         最后访问时间(打开看了一眼） 
    
    lines = [f"找到{len(files)}个录音文件（按时间倒序）:\n"]
    
    for f in files:
        stat = f.stat()        # 获取文件的元信息对象
        size_mb = stat.st_size/(1024*1024)  # st_size 是字节数 换算成MB
        mtime = datetime.fromtimestamp(stat.st_mtime)
        # st_mtime 返回的是类似 1748736000.0 这样的数字，人看不懂。
        # fromtimestamp() 就是把这串数字翻译成 2026-06-01 10:00:00 这样的可读格式。
        mtime_str = mtime.strftime("%Y-%m-%d %H:%M") # strftime: 格式化成"2025-04-10 14:30"
        # %Y    四位年  2026
        # %m    两位月  06
        # %d    两位日  24
        # %H    时    （24小时制）14
        # %M    分      30
        # %S     秒      05
        lines.append(f"  • {f.name} [{size_mb:.1f} MB] {mtime_str}")

    return "\n".join(lines)  # 作用是用指定的连接符(这里是\n)把列表里的元素拼成一个字符串


# ── Tool 2：查看单个文件详情 ───────────────────────────────────────────
@mcp.tool()
def get_recording_info(filename : str) -> str:
    """获取指定录音文件的详细信息。 filename 只需传文件名，不需要完整路径"""

# 安全检查：防止路径穿越攻击（如 filename="../../../etc/passwd"）
# resolve() 把路径里的 . 以及 . 展开成真实的绝对路径    
# 例子： /Users/xiechen/recordings/../Documents → /Users/xiechen/Documents
#       /Users/xiechen/recordings/./meeting.mp3 → /Users/xiechen/recordings/meeting.mp3
# 然后检查展开后的路径是否还在 RECORDINGS_DIR 目录下

    filepath = RECORDINGS_DIR/filename  # 拼接完整路径 Path类重载了/运算符

    try:
        resolved = filepath.resolve()
        if not str(resolved).startswith(str(RECORDINGS_DIR.resolve()) + "/"):
            return "错误：不允许访问录音文件夹以外的文件。"
    except Exception:
        return f"路径解析失败：{filename}"
    
    if not filepath.exists():
        return f"文件不存在：{filename}"
    
    if not filepath.is_file():
        return f"{filename}不是文件"

    stat = filepath.stat()
    size_mb = stat.st_size/(1024*1024)  # 文件大小
    ctime_str = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
    mtime_str = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

    return (
        f"文件名：{filepath.name}\n"
        f"格式：{filepath.suffix.upper()}\n"
        f"文件大小：{size_mb:.2f}MB\n"
        f"创建时间：{ctime_str}\n"
        f"最后修改：{mtime_str}\n"
        f"完整路径：{filepath}"
    )


# ── Tool 3：按关键字搜索 ───────────────────────────────────────────────
@mcp.tool()
def search_recordings(keyword:str) -> str:
    """在录音文件名中搜索包含指定关键字的文件。搜索不区分大小写。"""

    # 检查文件夹是否存在, 不存在则返回
    if not RECORDINGS_DIR.exists():
        return f"文件夹不存在：{RECORDINGS_DIR}"
    
    # keyword.lower() 和 f.name.lower() 都转小写，实现大小写不敏感的搜索
    # 将匹配到的文件名放入列表
    matched = [
        file
        for file in RECORDINGS_DIR.iterdir()
        if file.is_file()
        and file.suffix.lower() in AUDIO_EXTENSIONS
        and keyword.lower() in file.name.lower()
    ]

    if not matched: # 列表为空
        return f"没有找到文件名包含{keyword}的录音。\n"
    
    lines = [f"找到{len(matched)}个匹配的录音:\n"]
    for  f in matched:
        stat = f.stat()
        mtime_str = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d")
        lines.append(f" • {f.name}  {mtime_str}")

    return "\n".join(lines)

# ── 入口 ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()               # 启动 MCP Server，等待 Claude Desktop 连接