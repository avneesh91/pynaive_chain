import unittest
from unittest.mock import Mock
from command_processor import CommandProcessor

class TestCommandProcessor(unittest.TestCase):
    """
    Class for testing the command_processor functionality
    """
    PING_COMMAND = {'CMD': 'PING'}
    ADD_PEER_COMMAND = {'CMD': 'ADD_PEER', 'peer_id': 'SAMPLE_PEER_ID', 'peer_host': '0.0.0.0', 'peer_port': '1234'}

    def test__given_command_processor__when_command_processor_invoked_with_ping__then_return_pong_as_message(self):

        mock_chain_instance = Mock()
        command_processor = CommandProcessor(mock_chain_instance)

        actual_output = command_processor.command_processor(TestCommandProcessor.PING_COMMAND)
        expected_output = {'CMD': 'PONG'}

        self.assertEqual(expected_output, actual_output)
        self.assertIsInstance(actual_output, dict)

    def test__given_command_processor__when_command_processor_invoked_with_add_peer__then_invoke_add_peer_on_chain_instance(self):

        mock_chain_instance = Mock()
        mock_chain_instance.add_new_peer.return_value = None

        command_processor = CommandProcessor(mock_chain_instance)
        actual_output = command_processor.command_processor(TestCommandProcessor.ADD_PEER_COMMAND)

        mock_chain_instance.add_new_peer.assert_called_once_with('SAMPLE_PEER_ID', {'host': '0.0.0.0', 'port': '1234'})
