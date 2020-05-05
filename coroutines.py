import asyncio
import aiohttp
import queue

host = "http://localhost:"

class Requester(object):

    @staticmethod
    async def get_neighbours(node):

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(host + str(node)) as resp:
                    return list(str(await resp.text()).split(','))
        except:
            return []

    @staticmethod
    async def connect(node1, node2):

        async with aiohttp.ClientSession() as session:
            async with session.get(host + str(node1) + '/new', params={'port': str(node2)}) as resp:
                print(await resp.text())


async def complete_neighbourhood(start, requester = Requester):
    list_of_neighbours = await requester.get_neighbours(start)
    for first in list_of_neighbours:
        for second in list_of_neighbours:
            if first != second:
                await requester.connect(first, second)


async def climb_degree(start, requester = Requester):
    list_of_neighbours = await requester.get_neighbours(start)
    my_degree = len(list_of_neighbours)
    degrees_of_neighbours = []

    if my_degree == 0:
        return start

    async def count_degree(node):
        degrees_of_neighbours.append((node, len(await requester.get_neighbours(node))))

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


async def distance4(start, requester = Requester):
    q = queue.Queue()
    dictionary = {str(start): 0}

    async def visit(node):
        list_of_neighbours = await requester.get_neighbours(node)
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
        tasks = [visit(node) for node in tmp]
        await asyncio.gather(*tasks)

    answer = set()
    for key in dictionary:
        if dictionary[key] == 4:
            answer.add(key)
    return answer


async def main():
    print("climbing 8037")
    x = await climb_degree(8037)
    print(x)
    print("calculating distance4")
    z = await distance4(8030)
    print(z)
    print("complete neigh")
    await complete_neighbourhood(8034)
    print("climbing 8034")
    y = await climb_degree(8034)
    print(y)
    print("calculating distance4")
    q = await distance4(8030)
    print(q)
    print("end")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
