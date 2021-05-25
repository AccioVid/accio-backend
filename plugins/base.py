#  TODO reflect this class on the database
class AbstractPlugin():
  def __init__(self, plugin_config):
    self.plugin_config = plugin_config
    pass

  def run(self, input_path):
    pass
  # end def
# end class