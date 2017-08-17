"""
countdown-04.py - next edition of countdown program.

This example of using curio comes from the curio tutorial.  Please see the
README.md file for how to access it.

Explanation from tutorial:

However, it’s not necessary to [cancel the task] in the monitor. Change the
parent task to include a timeout and a cancellation request like this:

Notes:
    (start the monitor with:

        python3 -m curio.monitor

        commands:
            ps          list tasks
            where <n>   get stack trace for a task
            cancel <n>  cancel a task

    This edition no longer hangs.
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
    Kid is doing something else besides tying her shoe.

    :return:
    """
    print('Building the Millennium Falcon in Minecraft')
    await curio.sleep(1000)

async def parent():
    """
    Impatient parent allowing the kid only five seconds to tie her shoes.

    Parent cancels kid task when time runs out.

    :return:
    """
    kid_task = await curio.spawn(kid)
    await curio.sleep(5)

    print("Let's go")
    count_task = await curio.spawn(countdown, 10)
    await count_task.join()

    print("We're leaving!")
    """
    Added try/except to capture and act on a second timeout waiting for the 
    kid to finish.
    """
    try:
        await curio.timeout_after(10, kid_task.join)
    except curio.TaskTimeout:
        print('I warned you!')
        await kid_task.cancel()
    print('Leaving')

if __name__ == '__main__':
    curio.run(parent, with_monitor=True)

# EOF
