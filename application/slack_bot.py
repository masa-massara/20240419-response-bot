#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Slack上で動作するbotプログラム
"""

import sys                    # 正常終了のためにロード
from slackbot.bot import Bot  # slackbotパッケージのBotクラスを使うためのロード


def main():
    """
    メイン（main）プログラムです。
    常に0を応答します。
    """
    bot = Bot()  # Botを生成
    bot.run()    # Botを実行
    return 0


if __name__ == "__main__":  # 本モジュールが主プログラムのときのみif以下を実行するためのif文
    sys.exit(main())
