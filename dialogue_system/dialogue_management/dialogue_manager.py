#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
対話管理を扱うプログラム
"""

import copy                                                                   # 辞書のコピーをするためにロード
import os                                                                     # ファイル管理のためにロード
import numpy as np                                                            # 確率分布に従った取得のためにロード
from dialogue_system.dialogue_management.internal_state import InternalState  # 内部状態のクラス(InternalState)を利用するためにロード
from dialogue_system.dialogue_management.reference import Reference           # 参照データ用のクラス(Reference)を利用するためにロード
from dialogue_system.dialogue_management.responder import PatternResponder    # 各種応答生成器((.+)Responder)を利用するためにロード
from dialogue_system.dialogue_management.responder import RandomResponder     # 各種応答生成器((.+)Responder)を利用するためにロード
from dialogue_system.dialogue_management.responder import WhatResponder       # 各種応答生成器((.+)Responder)を利用するためにロード

from dialogue_system.dialogue_management.responder import SearchResponder       # 各種応答生成器((.+)Responder)を利用するためにロード


class DialogueManager():
    """
    対話管理を扱うクラス
    """
    def __init__(self, cfg):
        """
        コンストラクタ
        """
        self.cfg = cfg                                                                          # 設定情報をcfg属性にセット
        self.name = self.cfg['AgentName']                                                       # エージェントの名前をname属性に設定
        self.internal_state = InternalState()                                                   # 内部状態を扱うインスタンス
        self.history = []                                                                       # 対話履歴を記録するリストをhistory属性に設定
        self.history_filename = os.path.join(self.cfg['RefFilePath'], self.cfg['HistoryFile'])  # 対話履歴を記録するファイル名をhistory_filename属性に設定
        # 参照データを扱うインスタンス(応答リストrandom.txt、パターン集pattern.txtを読み込み済みのインスタンス)を生成し、reference属性に設定
        self.reference = Reference(
            random_file=os.path.join(self.cfg['RefFilePath'], self.cfg['RandomFile']),
            pattern_file=os.path.join(self.cfg['RefFilePath'], self.cfg['PatternFile']),
        )
        # 応答を返すインスタンスを格納するための辞書
        self.responder = {
            'pattern': PatternResponder('pattern', self.reference.pattern_list),                # パターンに応じた応答を返すPatternResponderを生成し、responder属性に追加
            'random': RandomResponder('random', self.reference.random_list),                    # 応答リストからランダムに応答を返すRandomResponderを生成し、responder属性に追加
            'what': WhatResponder('what', None),                                                # 聞き返しの応答を返すWhatResponderを生成し、responder属性に追加




            'search': SearchResponder('what',
None),                                                
            # 検索を表す、responder属性に追加
        }

    def __select_responder(self):
        """
        responderをある確率に応じて選択するメソッド
        """
        # 応答を返すインスタンスのリストから、pで指定された確率分布で(ここではself.responderの各要素が、[0.8, 0.1, 0.1]の確率として)一つの要素を選択
        return np.random.choice(
            [self.responder['pattern'], self.responder['random'], self.responder['what']],
            p=[0.8, 0.1, 0.1],
        )

    def start_internal_state(self, init_message):
        """
        内部状態を初期化するメソッド
        """
        self.internal_state.init_turn()                  # ターン数を初期化
        self.internal_state.state['utt'] = init_message  # 開始メッセージをセット

    def update_internal_state(self, analysis_result):
        """
        内部状態を更新するメソッド
        """
        self.internal_state.update(analysis_result)  # 発話理解結果(analysis_result)に基づき内部状態を更新
        self.internal_state.increment_turn()         # ターン数をインクリメント

    def select_action(self):
        """
        システム行動を選択するメソッド
        """
        system_action = copy.deepcopy(self.internal_state.state)  # 内部状態をシステム行動にコピー
        state = copy.deepcopy(self.internal_state.state)          # 内部状態をコピー
        if state['turn'] > 1:                                     # ターン数が2以上なら(開始メッセージでなければ)
            responder = self.__select_responder()                 # responderをある確率に応じて選択する
            response = responder.get_response(state['utt'])       # 内部状態の'utt'に基づき、responderから応答を取得する
            if not response:                                      # 応答が偽なら(空文字列であれば)
                responder = self.responder['random']              # responderをRandomResponderに設定する
                response = responder.get_response(state['utt'])   # 内部状態の'utt'に基づき、responderから応答を取得する
            system_action['utt'] = response                       # システム行動に応答をセットする
        return system_action                                      # システム行動を返す

    def update_history(self, utterance, response, user='USER'):
        """
        対話履歴を更新するメソッド
        """
        self.history.append((            # 対話履歴(self.history)に、発話と応答のタプルを追加
            f'{user}: {utterance}',      # ユーザ名と発話の文字列
            f'{self.name}: {response}',  # エージェント名と応答の文字列
        ))

    def write_history(self):
        """
        対話履歴を書き出すメソッド
        """
        with open(self.history_filename, 'w', encoding='utf-8') as a_file:                 # 書き出し専用ファイルとしてオープン
            a_file.write(''.join(map(lambda x: x[0] + '\n' + x[1] + '\n', self.history)))  # 対話履歴の各要素(タプル)の0番目と1番目の要素に改行をつけて連結した文字列のリストについて、各要素を連結したものを書き出す
