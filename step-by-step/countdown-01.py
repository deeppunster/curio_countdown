"""
countdown-01.py - first edition of countdown program.

This example of using curio comes from the curio tutorial.  Please see the
README.md file for how to access it.

Explanation from tutorial:

Here is a simple curio hello world program–a task that prints a simple
countdown as you wait for your kid to put their shoes on:
"""

import curio

async def countdown(n: int):
    """
    Simple countdown program using the curio.sleep timer.

    :param n: Seconds to count down before quitting.
    :return:
    """
    while n > 0:
        print('T-minus', n)
        await curio.sleep(1)
        n -= 1

if __name__ == '__main__':
    curio.run(countdown, 10)

# EOF
