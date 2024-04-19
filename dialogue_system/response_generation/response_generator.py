#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
応答生成を扱うプログラム
"""


class ResponseGenerator():
    """
    応答生成を扱うクラス
    """
    def get_response(self, system_action):
        """
        応答生成結果を返すメソッド
        """
        _ = system_action
        return {'utt': '', 'end': False}  # 辞書型として返す

    @staticmethod
    def echo(an_object):
        """
        静的解析ツール(lint)対策
        """
        return an_object


class ResponseGeneratorEcho(ResponseGenerator):
    """
    選択した行動内の発話をそのまま応答結果として返すクラス
    """
    def get_response(self, system_action):
        """
        選択した行動内の発話をそのまま応答結果として返すメソッド
        """
        return system_action  # 辞書型として返す
