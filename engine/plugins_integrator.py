import sys
sys.path.append('./')
import argparse
from api import PluginsModel

parser = argparse.ArgumentParser()
parser.add_argument("--name", help="Plugin name")
parser.add_argument("--executable_path", help="Path of plugin run file")

args = parser.parse_args()

new_plugin = PluginsModel()
new_plugin.name = args.name
new_plugin.executable_path = args.executable_path
new_plugin.is_enabled = True
new_plugin.system_configuration = {
    "keyframes_enabled": True,
    "keyframes_threshold": 0.5
}
new_plugin.plugin_configuration = {
    "plugin_name": args.name
}

new_plugin.save()
