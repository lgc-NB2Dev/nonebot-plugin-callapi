from nonebot.plugin import PluginMetadata, require

require("nonebot_plugin_alconna")

from .__main__ import HELP_TEXT  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.3.0"
__plugin_meta__ = PluginMetadata(
    name="CallAPI",
    description="使用指令来调用 Bot 的 API",
    usage=HELP_TEXT,
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-callapi",
    type="application",
    config=ConfigModel,
    supported_adapters=None,
    extra={"License": "MIT", "Author": "LgCookie"},
)
