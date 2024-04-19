#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
応答を扱うプログラム
"""

import random  # ランダムな取得のためにロード
import re      # 正規表現操作のためにロード


class Responder():
    """
    応答を扱うクラス
    """
    def __init__(self, name, reference):
        """
        コンストラクタ
        """
        self.name = name            # 応答クラスの名前を設定
        self.reference = reference  # 参照データを設定

    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        _ = utterance
        return ''

    @staticmethod
    def echo(an_object):
        """
        静的解析ツール(lint)対策
        """
        return an_object


class PatternResponder(Responder):
    """
    パターンに応じて応答を返す応答を扱うクラス
    """
    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        for item in self.reference:                       # 参照データ(self.reference)の各要素itemについて繰り返し
            match = re.search(item[0], utterance)         # 各要素の0番目の内容(item[0], すなわちパターン)が発話に含まれているかどうかを順に検索
            if match:                                     # もし最初の検索結果が存在すれば
                return random.choice(item[1].split('|'))  # その要素の1番目の内容(item[1], すなわちパターンに応じた応答集)を'|'で分割しリストとしたものから、ランダムに要素を一つ選択し、返す
        return ''                                         # もし全要素について検索に該当する結果がなければ、空文字列を返す


class RandomResponder(Responder):
    """
    応答リストからランダムに応答を返す応答を扱うクラス
    """
    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        _ = utterance
        return random.choice(self.reference)  # randomモジュールのchoice関数で応答リスト(self.reference)からランダムに応答を取得し、返す


class WhatResponder(Responder):
    """
    聞き返ししかしない応答を扱うクラス
    """
    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        return utterance + 'って何？'  # 聞き返しの応答を返す

class SearchResponder(Responder):
    """
    検索を扱うクラス
    """
    def get_response(self, utterance):
        """
        応答を返すメソッド
        """
        return random.choice(self.reference)  # 検索
