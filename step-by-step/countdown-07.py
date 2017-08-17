"""
countdown-06.py - next edition of countdown program.

This example of using curio comes from the curio tutorial.  Please see the
README.md file for how to access it.

Explanation from tutorial:

Although threads are not used to implement curio, you still might have to
worry about task synchronization issues (e.g., if more than one task is
working with mutable state). For this purpose, curio provides **Event**,
**Lock**, **Semaphore**, and **Condition** objects. For example,
let’s introduce an event that makes the child wait for the parent’s
permission to start playing:

Notes:
    (start the monitor with:

        python3 -m curio.monitor

        commands:
            ps          list tasks
            where <n>   get stack trace for a task
            cancel <n>  cancel a task

"""

import curio

"""
Added event as a signal for when the kid can start.
"""
start_evt = curio.Event()

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


async def friend(name: str):
    """
    A named friend is playing Minecraft with the original kid.

    :param name:
    :return:
    """
    print('Hi, my name is', name)
    print('Playing Minecraft')
    try:
        await curio.sleep(1000)
    except curio.CancelledError:
        print(name, 'going home')
        raise


async def kid():
    """
    Kid is doing something else besides tying her shoes and invites some
    friends to play with her.  She also has to wait until signalled before
    starting.

    :return:
    """
    """
    Kid now has to wait for the signal (via the event) to start.
    """
    print('Can I play?')
    await start_evt.wait()

    print('Building the Millennium Falcon in Minecraft')

    async with curio.TaskGroup() as f:
        await f.spawn(friend, 'Max')
        await f.spawn(friend, 'Lillian')
        await f.spawn(friend, 'Thomas')
        try:
            await curio.sleep(1000)
        except curio.CancelledError:
            print('Fine. Saving my work.')
            raise

async def parent():
    """
    Impatient parent allowing the kid only five seconds to tie her shoes
    and makes kid wait five seconds before starting.

    :return:
    """
    kid_task = await curio.spawn(kid)
    await curio.sleep(5)

    """
    Make the kid wait five seconds before signalling the start event.
    """
    print('Yes, go play')
    await start_evt.set()
    await curio.sleep(5)

    print("Let's go")
    count_task = await curio.spawn(countdown, 10)
    await count_task.join()

    print("We're leaving!")
    try:
        await curio.timeout_after(10, kid_task.join)
    except curio.TaskTimeout:
        print('I warned you!')
        await kid_task.cancel()
    print('Leaving')

if __name__ == '__main__':
    curio.run(parent, with_monitor=True)

# EOF
