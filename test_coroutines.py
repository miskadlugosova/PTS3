import unittest
import coroutines
import asynctest
from asynctest.mock import MagicMock

graph = set()

class GetNeighboursNotNetwork(MagicMock):
    async def __call__(self, *args, **kwarg):
        answer = []
        global graph
        for (x,y) in graph:
            if x == args[0]:
                answer.append(y)
        return answer


class ConnectNotNetwork(MagicMock):
    async def __call__(self, *args, **kwarg):
        global graph
        graph.add((args[0], args[1]))


# opytam sa na susedov vrcholu x, zavolam complete na jeho suseda, opytam sa na susedov vrcholu x
class TestCompleteNeighbourhood(asynctest.TestCase):
    def setUp(self):
        global graph
        graph = {('0', '1'), ('1', '0'), ('1', '2'), ('2', '1')}

    @asynctest.patch('coroutines.get_neighbours', new_callable=GetNeighboursNotNetwork)
    @asynctest.patch('coroutines.connect', new_callable=ConnectNotNetwork)
    async def test_complete_connects_two_not_connected_neighbours(self, neigh_mock, connect_mock):
        self.assertFalse(('0', '2') in graph)
        await coroutines.complete_neighbourhood('1')
        self.assertTrue(('0', '2') in graph)
        self.assertTrue(('2','0') in graph)


# ciara, idem zlava, cisla portov sa zmensuju
class TestClimbDegree(asynctest.TestCase):
    def setUp(self):
        global graph
        graph = {('0', '1'), ('1', '0'), ('1', '2'), ('2', '1'), ('2', '3'), ('3', '2'), ('3', '4'), ('4', '3')}

    @asynctest.patch('coroutines.get_neighbours', new_callable=GetNeighboursNotNetwork)
    @asynctest.patch('coroutines.connect', new_callable=ConnectNotNetwork)
    async def test_linear_graph_climb_from_edge(self, neigh_mock, connect_mock):
        self.assertEqual(await coroutines.climb_degree('4'), '1')


# graf z papiera - do vrcholu existuju cesty dlzky 3 aj 4
class TestDistance4(asynctest.TestCase):
    def setUp(self):
        global graph
        graph = {('0', '1'), ('1', '0'), ('0', '2'), ('2', '0'), ('0', '3'), ('3', '0'), ('1', '4'), ('4', '1'), ('4', '6'), ('6', '4'), ('2', '5'), ('5', '2'),
                 ('5', '6'), ('6', '5'),
                 ('6', '7'), ('7', '6')}

    @asynctest.patch('coroutines.get_neighbours', new_callable=GetNeighboursNotNetwork)
    @asynctest.patch('coroutines.connect', new_callable=ConnectNotNetwork)
    async def test_graph_with_different_paths_to_one_node(self, neigh_mock, connect_mock):
        self.assertEqual(await coroutines.distance4('0'), {'7'})


if __name__ == '__main__':
    unittest.main()
