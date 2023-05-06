import json
import traceback
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Type, Union

from bbcode import Parser as BBCodeParser
from nonebot import on_shell_command, require
from nonebot.exception import ParserExit
from nonebot.internal.adapter import Bot, Event
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import ShellCommandArgs
from nonebot.permission import SUPERUSER
from nonebot.rule import ArgumentParser, Namespace
from PIL import Image
from pil_utils import BuildImage, Text2Image
from pil_utils.fonts import DEFAULT_FALLBACK_FONTS
from pydantic import BaseModel
from pygments import highlight
from pygments.formatters import BBCodeFormatter
from pygments.lexer import Lexer
from pygments.lexers import JsonLexer, PythonTracebackLexer
from pygments.style import Style

try:
    from nonebot.adapters.telegram import Event as TgEvent
    from nonebot.adapters.telegram.message import File as TgFile
except ImportError:
    TgEvent = None

require("nonebot_plugin_saa")
from nonebot_plugin_saa import Image as SAAImage  # noqa: E402
from nonebot_plugin_saa import MessageFactory, extract_target  # noqa: E402

CODE_FONTS = [
    "JetBrains Mono",
    "Cascadia Mono",
    "Segoe UI Mono",
    "Liberation Mono",
    "Menlo",
    "Monaco",
    "Consolas",
    "Roboto Mono",
    "Courier New",
    "Courier",
    "Microsoft YaHei UI",
    *DEFAULT_FALLBACK_FONTS,
]
PADDING = 25

bbcode_parser = BBCodeParser()


@dataclass()
class Codeblock:
    lang: Type[Lexer]
    content: str


def item_to_plain_text(item: Union[str, Codeblock]) -> str:
    parsed: List[
        Tuple[int, Optional[str], Optional[dict], str]
    ] = bbcode_parser.tokenize(item.content if isinstance(item, Codeblock) else item)
    return "".join(
        [
            data
            for b_type, _, _, data in parsed
            if b_type == BBCodeParser.TOKEN_DATA or b_type == BBCodeParser.TOKEN_NEWLINE
        ],
    )


def format_plain_text(items: List[Union[str, Codeblock]]) -> str:
    return "\n".join(item_to_plain_text(it) for it in items)


def item_to_image(item: Union[str, Codeblock]) -> Image.Image:
    item = item or "\n"

    is_codeblock = False
    background_color: Optional[str] = None

    if not isinstance(item, Codeblock):
        formatted = item

    else:
        try:
            formatter = BBCodeFormatter()
            style: Style = formatter.style
            background_color = getattr(style, "background_color", None)

            formatted: str = highlight(item.content, item.lang(), formatter)
            is_codeblock = True

        except:
            formatted = item.content

    text_img = Text2Image.from_bbcode_text(
        formatted,
        fallback_fonts=CODE_FONTS,
    ).to_image()

    if not is_codeblock:
        img = text_img

    else:
        block_size = (text_img.width + PADDING * 2, text_img.height + PADDING * 2)
        block_width, block_height = block_size

        build_img = BuildImage.new("RGBA", block_size, (255, 255, 255, 0))

        if background_color:
            build_img.draw_rounded_rectangle(
                (0, 0, block_width, block_height),
                radius=10,
                fill=background_color,
            )

        build_img.paste(text_img, (PADDING, PADDING), alpha=True)

        img = build_img.image

    return img


def draw_image(items: List[Union[str, Codeblock]]) -> bytes:
    images = [item_to_image(it) for it in items]

    width = max(img.width for img in images)
    height = sum(img.height for img in images)
    bg = BuildImage.new(
        "RGBA",
        (width + PADDING * 2, height + PADDING * 2),
        (255, 255, 255),
    )

    y = PADDING
    for img in images:
        bg.paste(img, (PADDING, y), alpha=True)
        y += img.height

    return bg.convert("RGB").save("png").getvalue()


async def send_return(bot: Bot, event: Event, items: List[Union[str, Codeblock]]):
    try:
        # via saa
        target = extract_target(event)
        image = draw_image(items)
        await MessageFactory(SAAImage(image)).send_to(target, bot=bot)

    except:
        if TgEvent and isinstance(event, TgEvent):
            # telegram
            image = draw_image(items)
            await bot.send(event, TgFile.photo(image))

        else:
            await bot.send(event, format_plain_text(items))


def parse_params(params: List[str]) -> Dict[str, str]:
    if not params:
        return {}

    if len(params) == 1:
        try:
            return json.loads(params[0])
        except json.JSONDecodeError:
            pass

    params_dict = {}

    for param in params:
        if "=" not in param:
            raise ValueError(f"参数 `{param}` 不符合格式 `name=param`")

        name, value = param.split("=", 1)
        params_dict[name] = value

    return params_dict


parser = ArgumentParser()
parser.add_argument("api", type=str, help="要调用的 API")
parser.add_argument(
    "params",
    type=str,
    nargs="*",
    help="调用 API 的参数，每个参数的格式为 name=param；或者传入一个 JSON",
)

call_api_matcher = on_shell_command("callapi", permission=SUPERUSER, parser=parser)


@call_api_matcher.handle()
async def _(
    matcher: Matcher,
    bot: Bot,
    event: Event,
    args: Namespace = ShellCommandArgs(),
):
    api: str = args.api

    params: List[str] = args.params
    try:
        params_dict = parse_params(params)
    except ValueError as e:
        await matcher.finish(e.args[0])
    except Exception:
        logger.exception("参数解析错误")
        await matcher.finish("参数解析错误，请检查后台输出")

    ret_items = [
        f"[b]API:[/b] {api}",
        "",
        "[b]Params:[/b]",
        Codeblock(
            lang=JsonLexer,
            content=json.dumps(params_dict, ensure_ascii=False, indent=2),
        ),
        "",
        "[b]Result:[/b]",
    ]

    try:
        result = await bot.call_api(api, **params_dict)
    except Exception:
        formatted = traceback.format_exc()
        ret_items.append("Call API Failed!")
        ret_items.append(Codeblock(lang=PythonTracebackLexer, content=formatted))

    else:
        if isinstance(result, BaseModel):
            result = result.dict()

        try:
            ret_items.append(
                Codeblock(
                    lang=JsonLexer,
                    content=json.dumps(result, ensure_ascii=False, indent=2),
                ),
            )
        except:
            formatted = str(result)
            ret_items.append(formatted)

    await send_return(bot, event, ret_items)


@call_api_matcher.handle()
async def _(bot: Bot, event: Event, err: ParserExit = ShellCommandArgs()):
    if msg := err.message:
        await send_return(bot, event, [msg])
