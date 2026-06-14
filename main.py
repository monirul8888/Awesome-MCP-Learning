from fastmcp import FastMCP
import random

mcp = FastMCP("Demo Server")

@mcp.tool
def roll_dice(n_dice: int = 1)-> list[int]:

    """ Roll n_dice 6-sided and return the results"""

    return [random.randint(1,6) for _ in range(n_dice)]



@mcp.tool
def add_numbers(a: float , b: float)->float:

    """ Add Two Numbers"""
    return a+b

if __name__== "__main__":
    mcp.run()



