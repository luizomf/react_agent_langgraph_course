from langchain.tools import BaseTool, tool


@tool
def multiply(a: float, b: float) -> float:
    """Multiply a * b and returns the result

    Args:
        a: float multiplicand
        b: float multiplier

    Returns:
        the resulting float of the equation a * b
    """
    return a * b


TOOLS: list[BaseTool] = [multiply]
TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}
