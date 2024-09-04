import unittest

from shirdal.core.container import Container


class TestContainer(unittest.TestCase):

    def test_register_and_resolve(self):
        container = Container()

        def sample_function():
            return "Hello, World!"

        container.register(sample_function)

        # Test that the function can be resolved
        resolved_function = container.resolve("sample_function")
        self.assertIs(resolved_function, sample_function)  # Check if the resolved function is the same

        # Test that the function returns the expected result
        self.assertEqual(resolved_function(), "Hello, World!")

    def test_register_object(self):
        container = Container()

        class SampleClass:
            def greet(self):
                return "Hello from SampleClass!"

        sample_instance = SampleClass()
        container.register(sample_instance)

        # Test that the instance can be resolved
        resolved_instance = container.resolve("SampleClass")
        self.assertIs(resolved_instance, sample_instance)  # Check if the resolved instance is the same

        # Test that the instance method returns the expected result
        self.assertEqual(resolved_instance.greet(), "Hello from SampleClass!")

    def test_contains(self):
        container = Container()

        def sample_function():
            return "Hello!"

        container.register(sample_function)

        # Test that the container contains the registered function
        self.assertIn("sample_function", container)
        self.assertIn(sample_function, container)

        # Test that the container does not contain an unregistered function
        def another_function():
            return "Goodbye!"

        self.assertNotIn("another_function", container)
        self.assertNotIn(another_function, container)

    def test_resolve_non_existent(self):
        container = Container()

        # Test that resolving a non-existent name raises a KeyError
        with self.assertRaises(KeyError):
            container.resolve("non_existent")


# Run the tests
if __name__ == "__main__":
    unittest.main()
