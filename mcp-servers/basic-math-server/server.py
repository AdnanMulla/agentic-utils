import math
import logging
import wrapt
from fastmcp import FastMCP

# ---------------------------------------
# 🔹 Configure logging
# ---------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ],
)

logger = logging.getLogger("NumericTools")


# ---------------------------------------
# 🔹 Decorator that preserves function signature
# ---------------------------------------
def log_tool(func):
    """Decorator to log input/output without breaking FastMCP signature."""

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        logger.info(f"[CALL] Tool: {wrapped.__name__}")
        logger.info(f"[INPUT] args={args}, kwargs={kwargs}")

        try:
            result = wrapped(*args, **kwargs)
            logger.info(f"[OUTPUT] {result}")
            return result
        except Exception as e:
            logger.exception(f"[ERROR] Error in tool {wrapped.__name__}: {e}")
            raise

    return wrapper(func)


mcp = FastMCP("BasicMathServer")

# Tools


@mcp.tool()
@log_tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@mcp.tool()
@log_tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@mcp.tool()
@log_tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
@log_tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


@mcp.tool()
@log_tool
def power(a: float, b: float) -> float:
    """Raise a to the power of b (a^b)."""
    return a ** b


@mcp.tool()
@log_tool
def average(numbers: list[float]) -> float:
    """Return the average of a list of numbers."""
    if not numbers:
        raise ValueError("List cannot be empty.")
    return sum(numbers) / len(numbers)


if __name__ == "__main__":
    # Run HTTP transport on localhost, port 8000, path /mcp
    print("STARTING server...")
    mcp.run(transport="http", host="127.0.0.1", port=8000, path="/mcp")
