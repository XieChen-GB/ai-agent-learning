from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="demo-server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """两数相加"""
    return a + b

# 如果这个文件是被直接运行的（而不是被别的文件 import 进去当工具用），就执行 mcp.run()
if __name__ == "__main__":
    mcp.run()