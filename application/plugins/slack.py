#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Slack上で動作するbotプログラム
"""

import copy                              # 辞書のコピーをするためにロード
import os                                # ファイル管理のためにロード
from configparser import ConfigParser    # 設定ファイルの読み込みのためにロード
from slackbot.bot import respond_to      # slackbotパッケージのrespond_toデコレータを利用するためにロード
from dialogue_system.agent import Agent  # dialogue_systemパッケージのAgentクラスを利用するためにロード

cfg = {}              # 各種設定値を格納する辞書
bots = {}             # user_idに応じたbotを格納する辞書
initial_flag = False  # 開始記号が入力されたかどうかを示すフラグ
end_flag = False      # 終了状態かどうかを示すフラグ


def read_config():
    """
    設定ファイルを読み込む関数
    """
    cfg = ConfigParser()                                   # 設定ファイルを読み込むConfigParserを生成
    cfg.read(os.path.join(os.getcwd(), 'bot_config.ini'))  # 設定ファイルの読み込み
    return cfg['BOT']                                      # 設定ファイル内の'BOT'セクションを返す


def get_bot(user_id):
    """
    botを格納する辞書(bots)内から、user_idに対応するbotを呼び出す(存在しなければ生成する)関数
    """
    if user_id not in bots:      # user_idがbotsに存在しなければ
        bots[user_id] = Agent()  # Agentを生成し、bots[user_id]に格納する
    return bots[user_id]         # user_idに対応するbotを返す


def get_utterance_and_uid(message):
    """
    Slackのmessageからユーザ発話を取得する関数
    """
    body = message.body                 # slackbotが取得したmessage情報から本体(body)を取得
    # 本体(body)から、メッセージテキスト(text)、タイムスタンプ(ts)、ユーザ(user)をそれぞれ取得
    utterance, ts, user_id = body['text'], body['ts'], body['user']
    _ = ts
    return utterance, user_id           # ユーザの発話とidを返す


@respond_to('^(start)$')  # 開始記号'start'が入力されたらinitial_message関数が呼び出されるようにするデコレータ
def initial_message(message, something):
    """
    開始メッセージを表示する関数
    """
    _ = something
    global cfg, initial_flag                             # global変数のcfg, initial_flagを参照
    cfg = read_config()
    # 開始記号'start'が入力されたので、inital_flagをTrueにセット
    initial_flag = True
    utterance, user_id = get_utterance_and_uid(message)  # ユーザの発話とidを取得
    _ = utterance
    bot = get_bot(user_id)                               # user_idに対応したbotを取得
    init_message = bot.initial_message()                 # 開始メッセージを取得
    message.reply(init_message['utt'])                   # 開始メッセージのテキストを参照し応答
    bot.update_history(
        'start', init_message['utt'], cfg['UserName']
    )                                                    # 発話と応答の履歴を更新


@respond_to('^((?!^start$).+)$')  # 開始記号'start'以外の文字列が入力されたらget_response関数が呼び出されるようにするデコレータ
def get_response(message, something):
    """
    システム応答を取得する関数
    """
    _ = something
    global cfg, end_flag                                              # global変数のcfg, end_flagを参照
    if initial_flag and not end_flag:                                 # 開始記号が入力され、かつ、終了状態になっていなければ以下を実行
        utterance, user_id = get_utterance_and_uid(message)           # ユーザの発話とidを取得
        bot = get_bot(user_id)                                        # user_idに対応したbotを取得
        copy_state = copy.deepcopy(bot.manager.internal_state.state)  # 内部状態を複製
        copy_state["utt"] = utterance                                 # ユーザからの発話をセット
        response = bot.get_response(copy_state)                       # システム応答を取得
        message.reply(response['utt'])                                # システム応答のテキストを参照し応答
        bot.update_history(
            utterance, response['utt'], cfg['UserName']
        )                                                             # 発話と応答の履歴を更新
        if copy_state['turn'] > cfg.getint('NumOfTurn'):              # ターン数が既定値より大きくなったら終了
            bot.write_history()                                       # 対話履歴を書き出し
            message.reply(cfg.get('EndSignal'))                       # 終了記号を送信
            end_flag = True                                           # 終了状態であることをフラグにセット
