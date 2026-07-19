# mcp_server.py
# Run this file directly: python mcp_server.py
# The server communicates over stdio (standard input/output)

from mcp.server.fastmcp import FastMCP

# ── 1. Create the MCP server instance ───────────────────────────────────────
# FastMCP is the high-level, decorator-based API (recommended for most cases)
mcp = FastMCP(
    name="demo-server",        # Unique server name
    instructions=(             # Optional: tells the LLM how to use this server
        "A demo MCP server with math utilities and string helpers. "
        "Use add/multiply for arithmetic and word_count/reverse_text for strings."
    ),
)


# ── 2. Define tools using @mcp.tool() decorator ──────────────────────────────
# Each tool becomes callable by the LLM via the MCP client.
# Type hints + docstrings are used to generate the tool schema automatically.

@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b. Raises an error if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    return base ** exponent


@mcp.tool()
def word_count(text: str) -> dict:
    """Count words, characters, and sentences in the given text."""
    words = text.split()
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return {
        "word_count": len(words),
        "char_count": len(text),
        "sentence_count": len(sentences),
    }


@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse the characters in the given text."""
    return text[::-1]


@mcp.tool()
def is_palindrome(text: str) -> bool:
    """Check whether the given text is a palindrome (ignoring case/spaces)."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


# ── 3. Optionally expose static data as Resources ────────────────────────────
# Resources let the LLM read data without calling a function.

@mcp.resource("info://server-version")
def get_version() -> str:
    """Returns the current version of this MCP server."""
    return "1.0.0"


# ── 4. Run the server ─────────────────────────────────────────────────────────
# transport="stdio" means: read JSON-RPC messages from stdin, write to stdout.
# This is the standard transport for local MCP servers.
if __name__ == "__main__":
    mcp.run(transport="stdio")
