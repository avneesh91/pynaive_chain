from block_data import Block


def get_logger(actor):

  def output_log(message):
    print('[INFO]: {}-{}'.format(actor, message))

  return output_log


def get_block(**block_data):
  curr_block = Block(**block_data)
  curr_block.curr_hash = block_data['curr_hash']
  curr_block.data = block_data['data']
  return curr_block
