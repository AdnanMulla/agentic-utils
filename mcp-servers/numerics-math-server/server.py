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


# ---------------------------------------
# 🔹 Initialize MCP server
# ---------------------------------------
mcp = FastMCP("NumericToolsServer")


# ---------------------------------------
# 🔹 Define tools
# ---------------------------------------
@mcp.tool()
@log_tool
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


@mcp.tool()
@log_tool
def prime_factors(n: int) -> list[int]:
    """Return the list of prime factors of a number."""
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    if n > 2:
        factors.append(n)
    return factors


@mcp.tool()
@log_tool
def gcd(a: int, b: int) -> int:
    """Compute the greatest common divisor."""
    return math.gcd(a, b)


@mcp.tool()
@log_tool
def lcm(a: int, b: int) -> int:
    """Compute the least common multiple."""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)


@mcp.tool()
@log_tool
def next_prime(n: int) -> int:
    """Return the next prime number greater than n."""
    def is_p(x):
        if x <= 1:
            return False
        if x <= 3:
            return True
        if x % 2 == 0 or x % 3 == 0:
            return False
        i = 5
        while i * i <= x:
            if x % i == 0 or x % (i + 2) == 0:
                return False
            i += 6
        return True

    candidate = n + 1
    while not is_p(candidate):
        candidate += 1
    return candidate


@mcp.tool()
@log_tool
def is_perfect_number(n: int) -> bool:
    """Check if n is a perfect number (sum of divisors equals n)."""
    if n < 2:
        return False
    divisors_sum = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divisors_sum += i
            if i != n // i:
                divisors_sum += n // i
    return divisors_sum == n


# ---------------------------------------
# 🔹 Start MCP server
# ---------------------------------------
if __name__ == "__main__":
    print("🚀 Starting MCP-Numerics server on http://127.0.0.1:8001/mcp ...")
    mcp.run(transport="http", host="127.0.0.1", port=8001, path="/mcp")
