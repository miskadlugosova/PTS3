import asyncio
import aiohttp
import requests


async def get_neighbours(node, host="http://localhost:"):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(host + str(node)) as resp:
                return list(str(await resp.text()).split(','))
    except:
        return []


async def complete_neighbourhood(start, host="http://localhost:"):
    list_of_neighbours = await get_neighbours(start)

    async def connect(node):
        for neighbour in list_of_neighbours:
            if (neighbour != node):
                requests.get(f'{host}{node}/new?port={neighbour}')

    tasks = [connect(node) for node in list_of_neighbours]
    await asyncio.gather(*tasks)


async def climb_degree(start):
    list_of_neighbours = await get_neighbours(start)
    my_degree = len(list_of_neighbours)
    degrees_of_neighbours = []

    async def count_degree(node):
        degrees_of_neighbours.append((node, len(await get_neighbours(node))))

    tasks = [count_degree(node) for node in list_of_neighbours]
    await asyncio.gather(*tasks)


    degrees_of_neighbours = sorted(degrees_of_neighbours, key=lambda tup: (-tup[1], tup[0]))
    if my_degree > degrees_of_neighbours[0][1] or (
            my_degree == degrees_of_neighbours[0][1] and start < degrees_of_neighbours[0][0]):
        return start

    return await climb_degree(degrees_of_neighbours[0][0])


async def distance4(start):
    queue = []
    dictionary = {start : 0}

    async def visit(node):
        list_of_neighbours = await get_neighbours(node)
        distance = dictionary.get(node)
        for neigh in list_of_neighbours:
            if dictionary[neigh] <= distance+1:
                list_of_neighbours.discard(neigh)
            else:
                queue.append(neigh)
                dictionary[neigh] = dictionary+1

    queue.append(start)
    while not queue.empty():
        tmp = set()
        while not queue.empty():
            tmp.add(queue.pop(0))
        tasks = [visit(node) for node in set]
        await asyncio.gather(*tasks)


    answer = set()
    for key in dictionary:
        if dictionary[key] == 4:
            answer.add(key)
    return answer



async def main():
    x = await climb_degree(8034)
    print(x)
    await complete_neighbourhood(8031)
    y = await climb_degree(8034)
    print(y)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
