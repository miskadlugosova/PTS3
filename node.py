import asyncio
from urllib.parse  import urlparse, parse_qs
from http.server  import BaseHTTPRequestHandler
import requests


def get_handler():
    neighbours = set()
    class MyHandler(BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            nonlocal neighbours
            self._set_headers()
            response = 'http://localhost:8000/ or http://localhost:8000/new?port=8080'

            parsed = urlparse(self.path)
            pquery = parse_qs(parsed.query)
            self._root = '..'
            if parsed.path == '/':
                response = ','.join(neighbours)
            if parsed.path == '/new':
                self._name = pquery.get('port', (None,))[0]
                if self._name is not None:
                    neighbours.add(self._name)
                    response = 'Added or exists.'
                else:
                    response = 'Nothing to add.'

            self.wfile.write(bytes(response, "UTF-8"))
    
        def do_HEAD(self):
            self._set_headers()

    return MyHandler


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
    await asyncio.gather(tasks)


async def climb_degree(start):
    list_of_neighbours = get_neighbours(start)
    my_degree = len(list_of_neighbours)
    degrees_of_neighbours = []

    async def count_degree(node):
        degrees_of_neighbours.append((node, get_neighbours(node)))

    tasks = [asyncio.create_task(count_degree(node) for node in list_of_neighbours)]
    await asyncio.gather(tasks)
    degrees_of_neighbours = sorted(degrees_of_neighbours,  key=lambda tup:(-tup[1], tup[0]))

    if my_degree > degrees_of_neighbours[0][1] or (my_degree == degrees_of_neighbours[0][1] and start < degrees_of_neighbours[0][0]):
        return start
    
    return degrees_of_neighbours[0][0]


async def distance4(start):
    pass




