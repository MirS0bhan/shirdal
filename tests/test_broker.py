import unittest

from shirdal.core.broker import TaskManager, TaskExecutor

import time


class TestTaskManagerAndExecutor(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager()
        self.task_executor = TaskExecutor(self.task_manager)
        self.executed_tasks = []

    def task_factory(self, task_id):
        def task():
            self.executed_tasks.append(task_id)

        return task

    def test_task_execution(self):
        # Add tasks
        self.task_manager.add_task(self.task_factory(1))
        self.task_manager.add_task(self.task_factory(2))
        self.task_manager.add_task(self.task_factory(3))

        # Allow some time for tasks to be executed
        time.sleep(1)

        # Check that all tasks have been executed
        self.assertEqual(self.executed_tasks, [1, 2, 3])

    def test_task_addition_after_delay(self):
        # Add initial task
        self.task_manager.add_task(self.task_factory(1))

        # Allow some time for the first task to be executed
        time.sleep(0.5)

        # Add another task after delay
        self.task_manager.add_task(self.task_factory(2))

        # Allow some time for all tasks to be executed
        time.sleep(1)

        # Check that all tasks have been executed in order
        self.assertEqual(self.executed_tasks, [1, 2])

    def test_no_tasks_executed_when_none_added(self):
        # Allow some time to verify that no tasks are executed
        time.sleep(1)

        # Check that no tasks have been executed
        self.assertEqual(self.executed_tasks, [])


if __name__ == '__main__':
    unittest.main()
