import unittest
import threading
import krpc.test.schema.Test as TestSchema
from krpc.test.servertestcase import ServerTestCase
import krpc.types

krpc.types.add_search_path('krpc.test.schema')

def worker_thread(tid, conn):
    for i in range(100):
        conn.krpc.get_status()

def worker_thread2(tid, conn, test):
    for i in range(10):
        test.assertEqual('3.14159', conn.test_service.float_to_string(float(3.14159)))
        test.assertEqual('3.14159', conn.test_service.double_to_string(float(3.14159)))
        test.assertEqual('42', conn.test_service.int32_to_string(42))

class TestThreading(ServerTestCase, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestThreading, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestThreading, cls).tearDownClass()

    def setUp(self):
        super(TestThreading, self).setUp()

    def test_thread_safe_connection(self):
        thread0 = threading.Thread(target=worker_thread, args=(0, self.conn))
        thread1 = threading.Thread(target=worker_thread, args=(1, self.conn))
        thread0.start()
        thread1.start()
        thread0.join()
        thread1.join()

    def test_rpc_interleaving(self):
        threads = [threading.Thread(target=worker_thread2, args=(i, self.conn, self)) for i in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

if __name__ == '__main__':
    unittest.main()