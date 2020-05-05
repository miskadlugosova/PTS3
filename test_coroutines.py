import unittest
import asyncio
import coroutines
from unittest.mock import MagicMock
from asynctest import patch

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
class TestCompleteNeighbourhood(unittest.TestCase):
    def setUp(self):
        global graph
        graph = {('0', '1'), ('1', '0'), ('1', '2'), ('2', '1')}

    @patch('coroutines.get_neighbours', new_callable=GetNeighboursNotNetwork)
    @patch('coroutines.connect', new_callable=ConnectNotNetwork)
    def test_complete_connects_two_not_connected_neighbours(self, neigh_mock, connect_mock):
        self.assertFalse(('0', '2') in graph)
        loop = asyncio.new_event_loop()
        loop.run_until_complete(coroutines.complete_neighbourhood('1'))
        loop.close()
        self.assertTrue(('0', '2') in graph)


# ciara, idem zlava, cisla portov sa zmensuju
class TestClimbDegree(unittest.TestCase):
    def setUp(self):
        global graph
        graph = {('0', '1'), ('1', '0'), ('1', '2'), ('2', '1'), ('2', '3'), ('3', '2'), ('3', '4'), ('4', '3')}

    @patch('coroutines.get_neighbours', new_callable=GetNeighboursNotNetwork)
    @patch('coroutines.connect', new_callable=ConnectNotNetwork)
    def test_linear_graph_climb_from_edge(self, neigh_mock, connect_mock):
        loop1 = asyncio.new_event_loop()
        result = loop1.run_until_complete(coroutines.climb_degree('4'))
        loop1.close()
        self.assertEqual(result, '1')


# graf z papiera - do vrcholu existuju cesty dlzky 3 aj 4
class TestDistance4(unittest.TestCase):
    def setUp(self):
        global graph
        graph = {('0', '1'), ('1', '0'), ('0', '2'), ('2', '0'), ('0', '3'), ('3', '0'), ('1', '4'), ('4', '1'), ('4', '6'), ('6', '4'), ('2', '5'), ('5', '2'),
                 ('5', '6'), ('6', '5'),
                 ('6', '7'), ('7', '6')}

    @patch('coroutines.get_neighbours', new_callable=GetNeighboursNotNetwork)
    @patch('coroutines.connect', new_callable=ConnectNotNetwork)
    def test_graph_with_different_paths_to_one_node(self, neigh_mock, connect_mock):
        loop1 = asyncio.new_event_loop()
        result = loop1.run_until_complete(coroutines.distance4('0'))
        loop1.close()
        self.assertEqual(result, {'7'})


if __name__ == '__main__':
    unittest.main()
