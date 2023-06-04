from nonebot.plugin import PluginMetadata

from .__main__ import HELP_TEXT
from .config import ConfigModel

__version__ = "0.1.2"
__plugin_meta__ = PluginMetadata(
    name="CallAPI",
    description="使用指令来调用 Bot 的 API",
    usage=HELP_TEXT,
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-callapi",
    type="application",
    config=ConfigModel,
    supported_adapters=None,
    extra={"License": "MIT", "Author": "student_2333"},
)
