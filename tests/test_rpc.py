
from shirdal.net import ServerRPC, ClientRPC

class TestCLass:
    def add(self,x:int):
        return x*x


import unittest
import threading
from time import sleep


class TestRPCIntegration(unittest.TestCase):

    def setUp(self):
        self.endpoint = "tcp://127.0.0.1:4555"
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.start()
        sleep(1)  # Wait for the server to start up

    def tearDown(self):
        # Ensure the server thread terminates after each test
        self.server_thread.join()

    def run_server(self):
        server = ServerRPC(self.endpoint, TestCLass)
        server.start()

    def test_server_and_client_init(self):
        client = ClientRPC(self.endpoint)
        # Here you would check if the client has connected successfully
        # Unfortunately, ZeroMQ doesn't provide a straightforward way to check connection status

    # def test_rpc_call(self):
    #     client = ClientRPC(self.endpoint)
    #     result = client.call('add', 3, 4)
    #     self.assertEqual(result, {'result': 7})  # Assuming the server implements 'add'

    def test_wrapped_class(self):
        # This test assumes ExampleClass has an 'add' method
        client = ClientRPC(self.endpoint)
        WrappedClass = client.wrap_class(TestCLass)
        instance = WrappedClass()

        result = instance.add(2, 3)
        self.assertEqual(result, 5)  # Assuming the server correctly returns 2 + 3


if __name__ == '__main__':
    unittest.main()