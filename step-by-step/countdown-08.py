"""
countdown-06.py - next edition of countdown program.

This example of using curio comes from the curio tutorial.  Please see the
README.md file for how to access it.

Explanation from tutorial:

All of the synchronization methods also support timeouts. So, if the kid
wanted to be rather annoying, they could use a timeout to repeatedly nag
like this:

Notes:
    (start the monitor with:

        python3 -m curio.monitor

        commands:
            ps          list tasks
            where <n>   get stack trace for a task
            cancel <n>  cancel a task

"""

import curio

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
    Kid changed to nag the parent every second that she must wait.
    """
    while True:
        try:
            print('Can I play?')
            await curio.timeout_after(1, start_evt.wait)
            break
        except curio.TaskTimeout:
            print('Wha!?!')

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
