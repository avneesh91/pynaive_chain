import unittest
from unittest.mock import Mock
from command_processor import CommandProcessor

class TestCommandProcessor(unittest.TestCase):
    """
    Class for testing the command_processor functionality
    """

    def test__given_command_processor__when_command_processor_invoked_with_ping__then_return_pong_as_message(self):

        mock_chain_instance = Mock()
        command_processor = CommandProcessor(mock_chain_instance)

        actual_output = command_processor.command_processor({'CMD': 'PING'})
        expected_output = {'CMD': 'PONG'}

        self.assertEqual(expected_output, actual_output)
        self.assertIsInstance(actual_output, dict)

