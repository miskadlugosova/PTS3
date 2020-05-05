import threading
import time
import asynctest
from initialize_nodes import do_stuff
from coroutines import climb_degree, complete_neighbourhood, distance4


class TestSystem(asynctest.TestCase):
    def setUp(self):
        HOST = "localhost"
        graph_base = 8030
        graph = {(0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2), (3, 4), (4, 3), (4, 5), (5, 4)}
        graph = {(graph_base + x, graph_base + y) for x, y in graph}
        nodes = {x for y in graph for x in y}
        self.condition_ready = threading.Condition()
        self.condition_done = threading.Condition()
        self.server = threading.Thread(target=do_stuff, args=(
            HOST, nodes, graph, self.condition_ready, self.condition_done,))

    # climb node, calculate distance from beginning in linear, complete graph, climb from the same node, calculate distance from beginning again
    async def test_system_coroutines_together(self):
        self.server.start()
        with self.condition_ready:
            self.condition_ready.wait()
        time.sleep(1)
        self.assertEqual(await climb_degree('8034'), '8031')
        self.assertEqual(await distance4('8030'), {'8034'})
        await complete_neighbourhood('8034')
        self.assertEqual(await climb_degree('8034'), '8033')
        self.assertEqual(await distance4('8030'), {'8034', '8035'})
        with self.condition_done:
            self.condition_done.notify()
        self.server.join()


if __name__ == '__main__':
    asynctest.main()
