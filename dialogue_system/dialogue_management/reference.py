#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
参照データを扱うプログラム
"""


class Reference():
    """
    参照データを扱うクラス
    """
    def __init__(self, random_file, pattern_file):
        """
        コンストラクタ
        """
        self.random_list = self.read_sample_responses(random_file)  # 応答リスト(random_file)を読み込み、random_list属性に設定
        self.pattern_list = self.read_sample_pattern(pattern_file)  # パターン集(pattern_file)を読み込み、pattern_list属性に設定

    def read_sample_pattern(self, sample_file):
        """
        パターン集(sample_file)を読み込むメソッド
        """
        pattern = []                                                   # パターン集を格納するリストを用意
        with open(sample_file, 'r', encoding='utf-8') as a_file:       # 読み込み専用ファイルとしてオープン
            for line in a_file.read().splitlines():                    # 全体を読み込み、改行で分割したリストの各要素について繰り返し
                pat, *phrases = line.split()                           # 各行を空白(タブ含む)で分割した結果を左からpat, phrasesにそれぞれ取得
                if pat == '' or len(phrases) == 0:                     # patが長さ0の文字列、あるいは、phrases(リスト)の要素数が0ならば、次の繰り返しへ
                    continue
                pattern.append((pat, phrases[0]))                      # patとphrases[0]のタプルをpattern(リスト)に追加
        return sorted(pattern, key=lambda x: len(x[0]), reverse=True)  # patternの各要素(タプル)について、タプルの0番目の要素(文字列)の長さの降順にソートした結果を返す

    def read_sample_responses(self, sample_file):
        """
        応答リスト(sample_file)を読み込むメソッド
        """
        with open(sample_file, 'r', encoding='utf-8') as a_file:  # 読み込み専用ファイルとしてオープン
            return a_file.read().splitlines()                     # 全体を読み込み、改行で分割したものをリストとして返す
