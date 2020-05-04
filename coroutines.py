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
    visited = set()
    answer = set()
    list_of_neighbours = await get_neighbours(start)

    async def visit(node, distance):
        if node in answer and distance < 4:
            answer.discard(node)
            visited.discard(node)
        if node not in visited:
            visited.add(node)
            if (distance == 4):
                answer.add(node)
            else:
                list_of_neighbours = await get_neighbours(node)

    tasks = [visit(neigh, 1) for neigh in list_of_neighbours]
    await asyncio.gather(*tasks)
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
