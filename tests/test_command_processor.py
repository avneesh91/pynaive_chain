import json
import unittest
from unittest.mock import Mock
from unittest import mock
from block_data import Block
from command_processor import CommandProcessor
import websocket as websocket_client


class TestCommandProcessor(unittest.TestCase):
  """
    Class for testing the command_processor functionality
    """
  PING_COMMAND = {'CMD': 'PING'}
  ADD_PEER_COMMAND = {
      'CMD': 'ADD_PEER',
      'peer_id': 'SAMPLE_PEER_ID',
      'peer_host': '0.0.0.0',
      'peer_port': '1234'
  }
  NEW_PEER_JOIN = {
      'CMD': 'NEW_PEER_JOIN',
      'peer_id': 'SAMPLE_PEER_ID',
      'peer_host': '0.0.0.0',
      'peer_port': '1234'
  }
  UPLOAD_DICT  = {
            "CMD": "NEW_JOIN_DATA_UPLOAD",
            "peer_list": [{'peer': 'peer_id_1', 'host': '0.0.0.0', 'port': '1234'},
                          {'peer': 'peer_id_2', 'host': '0.0.0.0', 'port': '1234'},
                          {'peer': 'peer_id_3', 'host': '0.0.0.0', 'port': '1234'}],
            "data_list": [{'index': 0,
                           'previous_hash': 'test_data',
                           'data': '"initial_hash"',
                           'curr_hash': '814a4bf857f49f4542355fe9d6bafc2c59486b62ef731defba1d7ea2fc6a095e'},
                          {'index': 1,
                           'previous_hash': 'test_data1',
                           'data': '"initial_hash1"',
                           'curr_hash': 'b247d67fb2bd7d4ee506416b2d3e89d8630ee8e6a6f1c8fe5a5d41a560cdaac4'}
                          ]
    }



  def setUp(self):
    self.mock_chain_instance = Mock()
    self.mock_chain_instance.add_new_peer.return_value = None
    self.mock_chain_instance.get_peer_id_list.return_value = ['peer_id_1', 'peer_id_2', 'peer_id_3']
    self.mock_chain_instance.block_data.return_value = Block(0, 'test_data', 'initial_hash')
    self.mock_chain_instance.get_block_data.return_value = [Block(0, 'test_data', 'initial_hash'), Block(1, 'test_data1', 'initial_hash1')]
    self.mock_chain_instance.get_peer.return_value = {'host': '0.0.0.0', 'port': '1234'}

    self.mock_websocket_instance = Mock()
    self.mock_websocket_instance.send.return_value = None
    self.mock_websocket_instance.recv.return_value = 'Transmitted_successfully'



  def test__given_command_processor__when_command_processor_invoked_with_ping__then_return_pong_as_message(
      self):

    command_processor = CommandProcessor(self.mock_chain_instance)

    actual_output = command_processor.command_processor(
        TestCommandProcessor.PING_COMMAND)
    expected_output = {'CMD': 'PONG'}

    self.assertEqual(expected_output, actual_output)
    self.assertIsInstance(actual_output, dict)

  def test__given_command_processor__when_command_processor_invoked_with_add_peer__then_invoke_add_peer_on_chain_instance(
      self):
    command_processor = CommandProcessor(self.mock_chain_instance)
    actual_output = command_processor.command_processor(
        TestCommandProcessor.ADD_PEER_COMMAND)
    expected_output = 'ACK'

    self.mock_chain_instance.add_new_peer.assert_called_once_with(
        'SAMPLE_PEER_ID', {
            'host': '0.0.0.0',
            'port': '1234'
        })
    self.assertEqual(expected_output, actual_output)

  @mock.patch('websocket.create_connection')
  def test__given_command_processor__when_command_processor_invoked_with_new_peer_join__then_invoke_add_peer_and_data_upload(
      self, mock_websocket):

    calls_for_get_peer = [mock.call('peer_id_1'), mock.call('peer_id_2'), mock.call('peer_id_3'), mock.call('SAMPLE_PEER_ID')]

    calls_for_send_data_to_peer = [mock.call('peer_id_1'), mock.call('peer_id_2'), mock.call('peer_id_3'), mock.call('SAMPLE_PEER_ID')]

    mock_websocket.return_value = self.mock_websocket_instance

    command_processor = CommandProcessor(self.mock_chain_instance)
    actual_output = command_processor.command_processor(
        TestCommandProcessor.NEW_PEER_JOIN)
    expected_output = 'ACK'

    self.assertEqual(expected_output, actual_output)
    self.mock_chain_instance.add_new_peer.assert_called_once_with(
            'SAMPLE_PEER_ID', {
                'host': '0.0.0.0',
                'port': '1234'
            }
    )
    self.mock_chain_instance.get_peer_id_list.assert_called_once()
    self.mock_chain_instance.get_peer.assert_has_calls(calls_for_get_peer)
    self.mock_chain_instance.get_block_data.assert_called_once()
    self.mock_websocket_instance.send.assert_called_once_with(json.dumps(TestCommandProcessor.UPLOAD_DICT))

  @mock.patch('websocket.create_connection')
  def test__given_command_processor__when_command_processor_invoked_with_new_peer_join_then_raise_websocket_exception__then_remove_added_from_block_chain(
      self, mock_websocket):

    calls_for_get_peer = [mock.call('peer_id_1'), mock.call('peer_id_2'), mock.call('peer_id_3'), mock.call('SAMPLE_PEER_ID')]

    calls_for_send_data_to_peer = [mock.call('peer_id_1'), mock.call('peer_id_2'), mock.call('peer_id_3'), mock.call('SAMPLE_PEER_ID')]

    mock_websocket.return_value = self.mock_websocket_instance
    mock_websocket.side_effect = websocket_client.WebSocketTimeoutException

    command_processor = CommandProcessor(self.mock_chain_instance)
    actual_output = command_processor.command_processor(
        TestCommandProcessor.NEW_PEER_JOIN)
    expected_output = 'ACK'

    self.assertEqual(expected_output, actual_output)
    self.mock_chain_instance.add_new_peer.assert_called_once_with(
            'SAMPLE_PEER_ID', {
                'host': '0.0.0.0',
                'port': '1234'
            }
    )
    self.mock_chain_instance.get_peer_id_list.assert_called_once()
    self.mock_chain_instance.get_peer.assert_has_calls(calls_for_get_peer)
    self.mock_chain_instance.get_block_data.assert_called_once()
    self.mock_chain_instance.remove_peer.assert_called_once_with('SAMPLE_PEER_ID')
