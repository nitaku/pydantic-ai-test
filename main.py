from dotenv import load_dotenv
load_dotenv()

import random

from pydantic_ai import Agent

from rich.console import Console


console = Console()

agent = Agent('mistral:devstral-small-latest',
    instructions=(
        "You're a dice game, you should roll a six-sided die and see if the resulting number matches the user's guess."
        "Do not roll the die if the user does not provide a valid guess (i.e. not a number between 1 and 6)."
        "If the user guesses correctly, tell them they're a winner. "
    ),
)

@agent.tool_plain  
def roll_and_check_die(guess: int) -> bool:
    """Roll a six-sided die and return whether the guess matches the result."""
    if guess < 1 or guess > 6:
        raise ValueError('Invalid guess. Please provide a number between 1 and 6.')
    result = random.randint(1, 6)
    win = result == guess
    console.print('[cyan]--- You guessed %s. The die rolled %s. %s ---[/]' % (guess, result, 'You win!' if win else 'You lose.'))
    return win

console.print('[cornflower_blue bold]Welcome to the dice game![/]\n\nGuess a number between 1 and 6, I will roll the die and tell you if you win.\nWrite [bold]exit[/] or [bold]q[/] to quit.')
response = None
while True:
    prompt = console.input('[orange1 bold]>>>[/] ')
    if prompt == 'exit' or prompt == 'q':
        break
    if response is None:
        response = agent.run_sync(prompt)
    else:
        response = agent.run_sync(prompt, message_history=response.all_messages())
    console.print(response.output, style='dark_olive_green3')
