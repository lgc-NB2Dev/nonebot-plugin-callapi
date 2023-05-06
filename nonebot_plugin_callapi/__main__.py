import json
from typing import Dict, List

from nonebot import on_shell_command
from nonebot.exception import ParserExit
from nonebot.internal.adapter import Bot
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import ShellCommandArgs
from nonebot.permission import SUPERUSER
from nonebot.rule import ArgumentParser, Namespace

parser = ArgumentParser()
parser.add_argument("api", type=str, help="要调用的 API")
parser.add_argument(
    "params",
    type=str,
    nargs="*",
    help="调用 API 的参数，每个参数的格式为 name=param；或者传入一个 JSON",
)

call_api_matcher = on_shell_command("callapi", permission=SUPERUSER, parser=parser)


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


@call_api_matcher.handle()
async def _(matcher: Matcher, bot: Bot, args: Namespace = ShellCommandArgs()):
    api: str = args.api

    params: List[str] = args.params
    try:
        params_dict = parse_params(params)
    except ValueError as e:
        await matcher.finish(e.args[0])
    except Exception:
        logger.exception("参数解析错误")
        await matcher.finish("参数解析错误，请检查后台输出")

    result = await bot.call_api(api, **params_dict)

    try:
        formatted = json.dumps(result, ensure_ascii=False, indent=2)
    except TypeError:
        formatted = str(result)

    await matcher.finish(formatted)


@call_api_matcher.handle()
async def _(matcher: Matcher, err: ParserExit = ShellCommandArgs()):
    await matcher.finish(err.message)
