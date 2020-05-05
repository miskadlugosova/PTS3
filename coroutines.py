import asyncio
import aiohttp
import requests
import queue


async def get_neighbours(node, host="http://localhost:"):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(host + str(node)) as resp:
                return list(str(await resp.text()).split(','))
    except:
        return []


async def complete_neighbourhood(start, host="http://localhost:"):
    list_of_neighbours = await get_neighbours(start)
    print("list of neig in complete")
    print(list_of_neighbours)

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
    print("list of neigh in climbing")
    print(list_of_neighbours)

    if my_degree == 0:
        return start

    async def count_degree(node):
        degrees_of_neighbours.append((node, len(await get_neighbours(node))))

    tasks = [count_degree(node) for node in list_of_neighbours]
    await asyncio.gather(*tasks)

    degrees_of_neighbours = sorted(degrees_of_neighbours, key=lambda tup: (-tup[1], tup[0]))
    print("sorted degrees")
    print(degrees_of_neighbours)
    if my_degree > degrees_of_neighbours[0][1] or (
            my_degree == degrees_of_neighbours[0][1] and start < degrees_of_neighbours[0][0]):
        return start

    return await climb_degree(degrees_of_neighbours[0][0])


async def distance4(start):
    q = queue.Queue()
    dictionary = {str(start) : 0}

    async def visit(node):
        list_of_neighbours = await get_neighbours(node)
        distance = dictionary.get(node)
        print("printing list in visit")
        print(list_of_neighbours)
        for neigh in list_of_neighbours:
            print("deciding for")
            print(neigh)
            if neigh in dictionary.keys() and dictionary[neigh] <= distance+1:
                list_of_neighbours.remove(neigh)
            elif distance < 4:
                print("puttin in queue")
                q.put(neigh)
                dictionary[neigh] = distance+1

    q.put(str(start))
    while not q.empty():
        print("printing dictionary")
        print(dictionary)
        print("printing set")
        tmp = set()
        while not q.empty():
            tmp.add(q.get())
        print(tmp)
        tasks = [visit(node) for node in tmp]
        await asyncio.gather(*tasks)

    print("after finding")
    print(dictionary)

    answer = set()
    for key in dictionary:
        if dictionary[key] == 4:
            answer.add(key)
    return answer



async def main():
    #print("climbing 8037")
    #x = await climb_degree(8037)
    #print(x)
    print("calculating distance4")
    z = await distance4(8030)
    print(z)
    print("complete neigh")
    await complete_neighbourhood(8034)
    #print("climbing 8034")
    #y = await climb_degree(8034)
    #print(y)
    print("calculating distance4")
    q = await distance4(8030)
    print(q)
    print("end")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
