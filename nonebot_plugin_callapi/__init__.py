from nonebot.plugin import PluginMetadata

from . import __main__ as __main__
from .config import ConfigModel

__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    "CallAPI",
    "使用指令来调用 Bot 的 API",
    "帮助指令：callapi -h",
    ConfigModel,
    {"License": "MIT", "Author": "student_2333"},
)
