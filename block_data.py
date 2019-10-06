import json
import hashlib
import datetime


class Block(object):
  """
    This object forms the actual block of the block chain
    """

  def __str__(self):
    return 'Block <{}::{}>'.format(self.index, self.data)

  def __repr__(self):
    return 'Block <{}::{}>'.format(self.index, self.data)

  def __init__(self, index, previous_hash, data, *args, **kwargs):

    # index of the block
    self.index = index

    # hash of the previous time stamp
    self.previous_hash = previous_hash

    # takes data in string
    self.data = json.dumps(data)

    # hash of the block
    self.curr_hash = self.__get_current_hash__()

  def serialize(self, json_dump=False):
    """
        Function for getting the dict representation
        of a block
        """
    block_repr = {}
    block_repr['index'] = self.index
    block_repr['previous_hash'] = self.previous_hash
    block_repr['data'] = self.data
    block_repr['curr_hash'] = self.curr_hash

    if json_dump:
      block_repr = json.dumps(block_repr)

    return block_repr

  def __get_current_hash__(self):
    """
        Class function for getting hash of the current hash
        """
    hasher = hashlib.sha256()
    hasher.update(self.previous_hash.encode() + self.data.encode())
    return hasher.hexdigest()
