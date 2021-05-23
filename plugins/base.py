#  TODO reflect this class on the database
class AbstractPlugin():
  def __init__(self, system_config):
    self.system_config = system_config
    pass

  def run(self, input_path, run_config):
    pass
  # end def
# end class