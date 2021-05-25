"""
- query one unprocessed video
- multiple plugins
    - query enabled from db
    - load from executable_path
    - extract keyframes
        - consider threshold
    - 
- update video to be processed (not scalable)
"""

import sys
sys.path.append('./')
from api import VideosModel, PluginsModel

class EngineManager:
    def __init__(self):
        pass

    def _import(self, name):
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def run(self):
        videos = VideosModel.query.filter_by(processed=False)
        plugins_records = PluginsModel.query.filter_by(is_enabled=True)
        plugins = [self._import(p.executable_path)(p.plugin_configuration) for p in plugins_records]
        

obj = EngineManager()
obj.run()
# klass = obj._import('plugins.yolo_object_detection.yolo.YoloPlugin')
# import ipdb; ipdb.set_trace()
# plugins[1].plugin_configuration = {"confidence" : 0.5, "threshold" : 0.3}
# plugins[0].plugin_configuration = {'encodings_path': 'plugins/facedetection/the_office.pkl'}