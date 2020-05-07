import asyncio
import unittest
from unittest.mock import MagicMock
import coroutines
import asynctest
import time
from asynctest import patch

graph = set()


class GetNeighboursNotNetwork(MagicMock):
    async def __call__(self, *args, **kwarg):
        answer = []
        global graph
        for (x, y) in graph:
            if x == args[0]:
                answer.append(y)
        await asyncio.sleep(3)
        return answer


class ConnectNotNetwork(MagicMock):
    async def __call__(self, *args, **kwarg):
        global graph
        graph.add((args[0], args[1]))
        await asyncio.sleep(3)


class TestCompleteNeighbourhoodParallel(asynctest.TestCase):
    def setUp(self):
        global graph
        graph = {('0', '1'), ('1', '0'), ('1', '2'), ('2', '1')}

    @patch('coroutines.get_neighbours', new_callable=GetNeighboursNotNetwork)
    @patch('coroutines.connect', new_callable=ConnectNotNetwork)
    async def test_complete_get_once_connect_task_twice_parallel(self, neigh_mock, connect_mock):
        t0 = time.time()
        await coroutines.complete_neighbourhood('1')
        t1 = time.time()
        self.assertTrue(6 <= (t1 - t0) < 6.05)             #if not parallel, result would be at least 9s, minimum is 6 because i have at least 2 sleeps


class TestClimbDegreeParallel(asynctest.TestCase):
    def setUp(self):
        global graph
        graph = {('0', '1'), ('1', '0'), ('1', '2'), ('2', '1')}

    @patch('coroutines.get_neighbours', new_callable=GetNeighboursNotNetwork)
    @patch('coroutines.connect', new_callable=ConnectNotNetwork)
    async def test_climb_get_once_count_twice_parallel(self, neigh_mock, connect_mock):
        t0 = time.time()
        await coroutines.climb_degree('1')
        t1 = time.time()
        self.assertTrue(6 <= (t1-t0) < 6.05)                         #if not parallel result would be at least 9s, minimum is 6 because i have at least 2 sleeps


class TestDistance4Parallel(asynctest.TestCase):
    def setUp(self):
        global graph
        graph = {('0', '1'), ('1', '0'), ('0', '2'), ('2', '0'), ('0', '3'), ('3', '0')}

    @patch('coroutines.get_neighbours', new_callable=GetNeighboursNotNetwork)
    @patch('coroutines.connect', new_callable=ConnectNotNetwork)
    async def test_distance_get_once_visit_with_get_three_times_parallel(self, neigh_mock, connect_mock):
        t0 = time.time()
        await coroutines.distance4('0')
        t1 = time.time()
        self.assertTrue(6 <= (t1 - t0) < 6.05)                      #if not parallel result would be at least 12s, minimum is 6 because i have at least 2 sleeps


if __name__ == '__main__':
    asynctest.main()
