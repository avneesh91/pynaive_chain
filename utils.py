def get_logger(actor):

  def output_log(message):
    print('[INFO]: {}-{}'.format(actor, message))

  return output_log
