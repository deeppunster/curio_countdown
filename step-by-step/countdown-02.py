"""
countdown-02.py - next edition of countdown program.

This example of using curio comes from the curio tutorial.  Please see the
README.md file for how to access it.

Explanation from tutorial:

Let’s add a few more tasks into the mix:

Note: this edition appears to hang.
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


async def kid():
    """
    Kid is doing something else besides tying her shoes.

    :return:
    """
    print('Building the Millennium Falcon in Minecraft')
    await curio.sleep(1000)

async def parent():
    """
    Impatient parent allowing the kid only five seconds to tie her shoes.

    :return:
    """
    kid_task = await curio.spawn(kid)
    await curio.sleep(5)

    print("Let's go")
    count_task = await curio.spawn(countdown, 10)
    await count_task.join()

    print("We're leaving!")
    await kid_task.join()
    print('Leaving')

if __name__ == '__main__':
    curio.run(parent)

# EOF
