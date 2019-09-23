import json
import unittest
from .block_data import Block

class TestBlock(unittest.TestCase):
    """
    Class for testing the Block class
    """

    def setUp(self):
        self.Blockdata = Block(0, "random_testing_data", "initial_hash")

    def test__give_block_data__when_str_invoked__then_return_block_representation(self):
        actual_output = self.Blockdata.__str__()
        expected_output = 'Block <0::"initial_hash">'
        self.assertEqual(actual_output, expected_output)

    def test__given_block_data__when_repr_invoked__then_return_block_representation(self):
        actual_output = self.Blockdata.__repr__()
        expected_output = 'Block <0::"initial_hash">'
        self.assertEqual(actual_output, expected_output)

    def test__given_block_data__when_serialize_invoked_with_json_dumps_as_false__then_return_serialized_dict(self):
        actual_output = self.Blockdata.serialize()

        expected_output = {
            "index": 0,
            "previous_hash": "random_testing_data",
            "data": '"initial_hash"',
            "curr_hash": "88458136d3fc2260cc310fa41880c8d7a550c9949807d112a9ff0aed1f258d60"
        }

        self.assertEqual(actual_output, expected_output)
        self.assertIsInstance(actual_output, dict)

    def test__given_block_data__when_serialize_invoked_with_json_dumps_as_true__then_return_serialized_string(self):
        actual_output = self.Blockdata.serialize(json_dump=True)

        expected_output = json.dumps({
            "index": 0,
            "previous_hash": "random_testing_data",
            "data": '"initial_hash"',
            "curr_hash": "88458136d3fc2260cc310fa41880c8d7a550c9949807d112a9ff0aed1f258d60"
        })

        self.assertEqual(actual_output, expected_output)
        self.assertIsInstance(actual_output, str)

