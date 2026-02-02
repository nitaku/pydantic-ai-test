# TODO validate user input in a tool
# TODO perform the match in the roll_die tool
# TODO maintain context

from dotenv import load_dotenv
load_dotenv()

import random

from pydantic_ai import Agent

from rich.console import Console


console = Console()

agent = Agent('mistral:devstral-small-latest',
    instructions=(
        "You're a dice game, you should roll a six-sided die and see if the number "
        "you get back matches the user's guess. Do not roll the die if the user does not provide a valid guess (i.e. not a number between 1 and 6)."
        "If the user guesses correctly, tell them they're a winner. "
    ),
)

@agent.tool_plain  
def roll_die() -> str:
    """Roll a six-sided die and return the result."""
    result = random.randint(1, 6)
    console.print('[cyan]--- The die rolled %s ---[/]' % result)
    return str(result)

console.print('[cornflower_blue bold]Welcome to the dice game![/]\n\nGuess a number between 1 and 6, I will roll the die and tell you if you win.\nWrite [bold]exit[/] or [bold]q[/] to quit.')
while True:
    prompt = console.input('[orange1 bold]>>>[/] ')
    if prompt == 'exit' or prompt == 'q':
        break
    response = agent.run_sync(prompt)
    console.print(response.output, style='dark_olive_green3')
