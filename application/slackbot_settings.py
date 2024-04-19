#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Slack上で動作するbotプログラムのための初期設定
"""

import os  # 環境変数の読み込みのためにロード

API_TOKEN = os.environ.get('SLACK_API_TOKEN', '')  # 環境変数SLACK_API_TOKENからAPI_TOKENの値をセット

default_reply = 'デフォルトの応答テキスト'  # いずれのデコレータにも合致しなかった場合のデフォルトの応答テキスト

# pluginファイル or pluginが存在するディレクトリ
PLUGINS = [
    'plugins',
]
