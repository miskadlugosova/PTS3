import asyncio
import aiohttp
import queue
host = "http://localhost:"


async def get_neighbours(node):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(host + str(node)) as resp:
                return list(str(await resp.text()).split(','))
    except:
        return []


async def connect(node1, node2):
    async with aiohttp.ClientSession() as session:
        async with session.get(host + str(node1) + '/new', params={'port': str(node2)}) as resp:
            print(await resp.text())


async def complete_neighbourhood(start):
    list_of_neighbours = await get_neighbours(start)
    tasks = []
    for first in list_of_neighbours:
        for second in list_of_neighbours:
            if first != second:
                task = asyncio.create_task(connect(first, second))
                tasks.append(task)
    await asyncio.gather(*tasks)


async def climb_degree(start):
    list_of_neighbours = await get_neighbours(start)
    my_degree = len(list_of_neighbours)
    degrees_of_neighbours = []

    if my_degree == 0:
        return start

    async def count_degree(node):
        degrees_of_neighbours.append((node, len(await get_neighbours(node))))

    tasks = []
    for node in list_of_neighbours:
        task = asyncio.create_task(count_degree(node))
        tasks.append(task)
    await asyncio.gather(*tasks)

    degrees_of_neighbours = sorted(degrees_of_neighbours, key=lambda tup: (-tup[1], tup[0]))

    if my_degree > degrees_of_neighbours[0][1] or (
            my_degree == degrees_of_neighbours[0][1] and start < degrees_of_neighbours[0][0]):
        return start

    return await climb_degree(degrees_of_neighbours[0][0])


async def distance4(start):
    q = queue.Queue()
    dictionary = {str(start): 0}

    async def visit(node):
        list_of_neighbours = await get_neighbours(node)
        distance = dictionary.get(node)
        for neigh in list_of_neighbours:
            if neigh in dictionary.keys() and dictionary[neigh] <= distance + 1:
                pass
            elif distance < 4:
                q.put(neigh)
                dictionary[neigh] = distance + 1

    q.put(str(start))
    while not q.empty():
        tmp = set()
        while not q.empty():
            tmp.add(q.get())
        tasks = []
        for node in tmp:
            task = asyncio.create_task(visit(node))
            tasks.append(task)
        await asyncio.gather(*tasks)

    answer = set()
    for key in dictionary:
        if dictionary[key] == 4:
            answer.add(key)
    return answer