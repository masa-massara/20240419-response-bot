#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
エージェントを扱うプログラム
"""

import os                                                                                 # ファイル管理のためにロード
from configparser import ConfigParser                                                     # 設定ファイルの読み込みのためにロード
from dialogue_system.dialogue_management.dialogue_manager import DialogueManager          # 対話管理部を利用するためのロード
from dialogue_system.utterance_analysis.utterance_analyzer import UtteranceAnalyzerEcho   # 発話理解部を利用するためのロード
from dialogue_system.response_generation.response_generator import ResponseGeneratorEcho  # 応答生成部を利用するためのロード


class Agent():
    """
    エージェントを扱うクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """
        self.cfg = self.__read_config()                    # 設定ファイルの読み込み
        self.name = self.cfg['AgentName']                  # エージェントの名前をname属性に設定
        self.manager = DialogueManager(self.cfg)           # 対話管理部をmanager属性に設定
        self.utterance_analyzer = UtteranceAnalyzerEcho()  # 発話理解部をutterance_analyzer属性に設定
        self.response_generator = ResponseGeneratorEcho()  # 応答生成部をresponse_generator属性に設定

    def __read_config(self):
        """
        設定ファイルを読み込むメソッド
        """
        cfg = ConfigParser()                                                                   # 設定ファイルを読み込むConfigParserを生成
        cfg.read(os.path.join(os.getcwd(), os.pardir, 'dialogue_system', 'agent_config.ini'))  # 設定ファイルの読み込み
        return cfg['AGENT']                                                                    # 設定ファイル内の'AGENT'セクションを返す

    def initial_message(self):
        """
        開始メッセージを返すメソッド
        """
        self.manager.start_internal_state(self.cfg['InitialMessage'])   # 内部状態を開始
        system_action = self.manager.select_action()                    # 内部状態に基づき行動選択
        response = self.response_generator.get_response(system_action)  # 選択された行動に基づき応答を生成
        return response                                                 # 開始メッセージを返す

    def get_response(self, state):
        """
        エージェントの応答を取得するメソッド
        """
        analysis_result = self.utterance_analyzer.get_result(state)     # 発話を理解
        self.manager.update_internal_state(analysis_result)             # 内部状態を更新
        system_action = self.manager.select_action()                    # 内部状態に基づき行動選択
        response = self.response_generator.get_response(system_action)  # 選択された行動に基づき応答を生成
        return response                                                 # 生成した応答を返す

    def update_history(self, utterance, response, user):
        """
        対話履歴を更新するメソッド
        """
        self.manager.update_history(utterance, response, user)  # 対話履歴を更新

    def write_history(self):
        """
        対話履歴を書き込むメソッド
        """
        self.manager.write_history()                            # 対話履歴を書き込み
