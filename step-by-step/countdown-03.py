"""
countdown-03.py - next edition of countdown program.

This example of using curio comes from the curio tutorial.  Please see the
README.md file for how to access it.

Explanation from tutorial:

Run the previous edition with the curio monitor enabled:

Notes:
    (start the monitor with:

        python3 -m curio.monitor

        commands:
            ps          list tasks
            where <n>   get stack trace for a task
            cancel <n>  cancel a task

    This edition appears to hang.
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
    curio.run(parent, with_monitor=True)

# EOF
