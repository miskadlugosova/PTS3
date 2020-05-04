import asyncio
import requests


def get_neighbours(node):
    try:
        neighbours = (requests.get(f'http://localhost:{node}').text.split(","))
        return neighbours
    except:
        return []


async def complete_neighbourhood(start):
    list_of_neighbours = get_neighbours(start)

    async def connect(node):
        for neighbour in list_of_neighbours:
            if (neighbour != node):
                requests.get(f'http://localhost:{node}/new?port={neighbour}')

    tasks = [asyncio.create_task(connect(node) for node in list_of_neighbours)]
    await asyncio.gather(*tasks)


async def climb_degree(start):
    list_of_neighbours = get_neighbours(start)
    print("climb_degree")
    print(list_of_neighbours)
    my_degree = len(list_of_neighbours)
    degrees_of_neighbours = []

    async def count_degree(node):
        degrees_of_neighbours.append((node, len(get_neighbours(node))))
        print(node)
        print(len(get_neighbours(node)))

    tasks = [asyncio.create_task(count_degree(node) for node in list_of_neighbours)]
    await asyncio.gather(*tasks)
    degrees_of_neighbours = sorted(degrees_of_neighbours, key=lambda tup: (-tup[1], tup[0]))

    if my_degree > degrees_of_neighbours[0][1] or (
            my_degree == degrees_of_neighbours[0][1] and start < degrees_of_neighbours[0][0]):
        return start

    return degrees_of_neighbours[0][0]


async def distance4(start):
    visited = {}
    answer = {}

    async def visit(node, distance):
        if node in answer and distance < 4:
            answer.discard(node)
            visited.discard(node)
        if node not in visited:
            visited.add(node)
            if (distance == 4):
                answer.add(node)
            else:
                list_of_neighbours = get_neighbours(start)
                tasks = [asyncio.create_task(visit(neigh, distance + 1) for neigh in list_of_neighbours)]
                await asyncio.gather(*tasks)

    await visit(start, 0)
    return answer