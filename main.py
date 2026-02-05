from dotenv import load_dotenv
load_dotenv()

import random

from pydantic_ai import Agent, ModelRetry
from pydantic_ai.exceptions import UnexpectedModelBehavior

from rich.console import Console

from calculator import calc


console = Console()

agent = Agent('mistral:devstral-medium-latest',
    instructions=(
        "You're a dice game, you should roll a six-sided die and obtain whether the user's guess matches the result as well as the roll."
        "Do not roll the die if the user does not provide a valid guess (i.e. not a number between 1 and 6)."
        "If the user provides a simple mathematical expression (using +-*/ and brackets alone), evaluate it and use it as the guess."
        "If the user guesses correctly, tell them they're a winner. "
    ),
)

@agent.tool_plain(retries=3)
def roll_and_check_die(guess: int) -> (bool, int):
    """Roll a six-sided die and return whether the guess (a number between 1 and 6) matches the result, as well as the roll result."""
    if guess < 1 or guess > 6:
        console.print('[red]--- DIE tool: Invalid guess. Please provide a number between 1 and 6. ---[/]')
        raise ModelRetry('Invalid guess. Please provide a number between 1 and 6.')
    result = random.randint(1, 6)
    win = result == guess
    console.print('[cyan]--- DIE tool: You guessed %s. The die rolled %s. %s ---[/]' % (guess, result, 'You win!' if win else 'You lose.'))
    return (win, result)

@agent.tool_plain(retries=3)
def calculate(expression: str) -> str:
    """Evaluate a simple mathematical expression (using "+-*/" and brackets alone) and return the result as a string."""
    try:
        result = calc(expression)
    except Exception as e:
        console.print('[red]--- CALC tool: Error calculating %s ---[/]' % expression)
        raise ModelRetry('Error calculating %s: %s - Only simple mathematical expressions (using "+-*/" and brackets alone) are supported.' % (expression, e))
    console.print('[magenta]--- CALC tool: The result of %s is %s ---[/]' % (expression, result))
    return str(result)

console.print('[cornflower_blue bold]Welcome to the dice game![/]\n\nGuess a number between 1 and 6, I will roll the die and tell you if you win.\nWrite [bold]exit[/] or [bold]q[/] to quit.')
response = None
while True:
    prompt = console.input('[orange1 bold]>>>[/] ')
    if prompt == 'exit' or prompt == 'q':
        break
    
    try:
        if response is None:
            response = agent.run_sync(prompt)
        else:
            response = agent.run_sync(prompt, message_history=response.all_messages())
        
        console.print(response.output, style='dark_olive_green3')
    except UnexpectedModelBehavior as e:
        console.print('[red] Unexpected model behavior. Please try again with a different prompt. Error: %s[/]' % e.message)