"""
Tutorial 1 from https://curio.readthedocs.io/en/latest/tutorial.html.
"""

import curio
import signal

# define a signal that forced the kids to wait for permission to start
start_evt = curio.Event()


async def fib(nbr):
    """
    Compute Fibonacci numbers (brute force)
    :param nbr: Fibonacci number to compute
    :return: desired Fibonacci number
    """
    if nbr <= 2:
        return 1
    else:
        fib_task1 = await curio.spawn(fib, nbr - 1)
        fib_nbr1 = await fib_task1.join()
        fib_task2 = await curio.spawn(fib, nbr - 2)
        fib_nbr2 = await fib_task2.join()
        fib_nbr = int(fib_nbr1) + int(fib_nbr2)
        return fib_nbr

async def fibrunner(nbr):
    """
    Run recursive fib until final number derived.

    :param nbr:
    :return:
    """
    print(f'fibrunner started with {nbr}')
    fib_task = await curio.spawn(fib, nbr)
    result = await fib_task.join()

    print(f'Fibrunner finished with {result}')
    return

async def countdown(ctr):
    """
    Simple countdown timer.

    :param ctr: number of seconds to wait
    :return:
    """
    while ctr > 0:
        print(f'T minus {ctr}')
        await curio.sleep(1)
        ctr -= 1


async def friend(name):
    """
    Friend definition of others the kid knows.

    :param name: name of friend
    :return:
    """
    print(f'Hi, my name is {name}')
    print('Playing Minecraft')
    try:
        await curio.sleep(1000)
    except curio.CancelledError:
        print(f"{name} - I'm going home")
        raise


async def kid():
    """
    Kid task.

    :return:
    """
    task_id = 0

    print('Can I play?')
    await start_evt.wait()

    print('Building the Millennium Falcon in Minecraft')

    async with curio.TaskGroup() as friends:
        await friends.spawn(friend, 'Max')
        await friends.spawn(friend, 'Lillian')
        await friends.spawn(friend, 'Thomas')
        try:
            total = 0
            for nbr in range(50):
                await curio.sleep(1)
                task_id = await curio.aside(fibrunner, nbr)
                print(f'Started task {task_id}')
                await task_id.join()

        except curio.CancelledError:
            print('Fine. Saving my work.')
            # await task_id.cancel()
            print(f'Task {task_id} has been cancelled')
            raise


async def parent():
    """
    Parent's agenda.

    :return:
    """

    # catch termination signal to stop playing and leave
    goodbye = curio.SignalEvent(signal.SIGINT, signal.SIGTERM)

    kid_task = await curio.spawn(kid)
    await curio.sleep(5)

    print('Yes, go play.')
    await start_evt.set()

    await goodbye.wait()
    # del goodbye        # trash the signal event to get immediate exit

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
