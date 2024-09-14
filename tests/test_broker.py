import unittest
from enum import Enum, auto

# Assuming the classes are imported from the module where they are defined
from shirdal import Broker, BrokerManager, BrokerType
from shirdal.core import TaskExecutor, TaskManager, ListQueue, Container
from shirdal.net import ServerTaskManager, ClientTaskManager


class TestBroker(unittest.TestCase):
    def setUp(self):
        # Create real instances of the dependencies
        self.container = Container()
        self.task_manager = TaskManager(ListQueue())
        self.task_executor = TaskExecutor(self.task_manager, self.container)
        self.broker = Broker(self.task_manager, self.task_executor)

    def test_broker_start(self):
        self.broker.start()
        # Check if the task executor and task manager are started
        self.assertTrue(self.task_executor.is_running)
        self.assertTrue(self.task_manager.is_running)

    def test_broker_stop(self):
        self.broker.start()  # Start first to ensure stop has an effect
        self.broker.stop()
        # Check if the task executor and task manager are stopped
        self.assertFalse(self.task_executor.is_running)
        self.assertFalse(self.task_manager.is_running)

    def test_broker_publish(self):
        topic = "test_topic"
        message = "test_message"
        self.broker.publish(topic, message)
        # Check if the message was published (this would depend on your TaskManager implementation)
        self.assertIn((topic, message), self.task_manager.messages)

    def test_broker_subscribe(self):
        topic = "test_topic"
        received_messages = []

        def callback(message):
            received_messages.append(message)

        self.broker.subscribe(topic, callback)
        self.broker.publish(topic, "test_message")
        # Check if the callback was called with the correct message
        self.assertIn("test_message", received_messages)

    def test_broker_create_local(self):
        broker = Broker.create(BrokerType.LOCAL)
        self.assertIsInstance(broker, Broker)
        self.assertIsInstance(broker.task_manager, TaskManager)
        self.assertIsInstance(broker.task_executor, TaskExecutor)

    def test_broker_create_server(self):
        broker = Broker.create(BrokerType.SERVER, port=1234)
        self.assertIsInstance(broker, Broker)
        self.assertIsInstance(broker.task_manager, ServerTaskManager)
        self.assertIsInstance(broker.task_executor, TaskExecutor)

    def test_broker_create_client(self):
        broker = Broker.create(BrokerType.CLIENT, host='localhost', port=1234)
        self.assertIsInstance(broker, Broker)
        self.assertIsInstance(broker.task_manager, ClientTaskManager)

    def test_broker_create_invalid_type(self):
        with self.assertRaises(ValueError):
            Broker.create(Enum('InvalidType', 'INVALID'))


class TestBrokerManager(unittest.TestCase):
    def setUp(self):
        self.broker_manager = BrokerManager()

    def test_create_broker(self):
        broker = self.broker_manager.create_broker('test_broker', BrokerType.LOCAL)
        self.assertIsInstance(broker, Broker)
        self.assertIn('test_broker', self.broker_manager.brokers)

    def test_get_broker(self):
        broker = self.broker_manager.create_broker('test_broker', BrokerType.LOCAL)
        retrieved_broker = self.broker_manager.get_broker('test_broker')
        self.assertEqual(broker, retrieved_broker)

    def test_start_all(self):
        broker = self.broker_manager.create_broker('test_broker', BrokerType.LOCAL)
        self.broker_manager.start_all()
        self.assertTrue(broker.task_executor.is_running)
        self.assertTrue(broker.task_manager.is_running)

    def test_stop_all(self):
        broker = self.broker_manager.create_broker('test_broker', BrokerType.LOCAL)
        self.broker_manager.start_all()  # Start first to ensure stop has an effect
        self.broker_manager.stop_all()
        self.assertFalse(broker.task_executor.is_running)
        self.assertFalse(broker.task_manager.is_running)

    def test_publish(self):
        broker = self.broker_manager.create_broker('test_broker', BrokerType.LOCAL)
        topic = "test_topic"
        message = "test_message"
        self.broker_manager.publish('test_broker', topic, message)
        # Check if the message was published to the correct broker
        self.assertIn((topic, message), broker.task_manager.messages)

    def test_publish_broker_not_found(self):
        with self.assertRaises(ValueError):
            self.broker_manager.publish('non_existent_broker', 'test_topic', 'test_message')

    def test_subscribe(self):
        broker = self.broker_manager.create_broker('test_broker', BrokerType.LOCAL)
        topic = "test_topic"
        received_messages = []

        def callback(message):
            received_messages.append(message)

        self.broker_manager.subscribe('test_broker', topic, callback)
        self.broker_manager.publish('test_broker', topic, "test_message")
        # Check if the callback was called with the correct message
        self.assertIn("test_message", received_messages)

    def test_subscribe_broker_not_found(self):
        with self.assertRaises(ValueError):
            self.broker_manager.subscribe('non_existent_broker', 'test_topic', lambda x: None)


if __name__ == '__main__':
    unittest.main()
