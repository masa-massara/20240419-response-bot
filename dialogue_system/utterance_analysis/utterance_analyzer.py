#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
発話理解を扱うプログラム
"""


class UtteranceAnalyzer():
    """
    発話理解を扱うクラス
    """
    def get_result(self, state):
        """
        理解結果を返すメソッド
        """
        _ = state
        return {'utt': ''}  # 辞書型として返す

    @staticmethod
    def echo(an_object):
        """
        静的解析ツール(lint)対策
        """
        return an_object


class UtteranceAnalyzerEcho(UtteranceAnalyzer):
    """
    入力を理解結果としてそのまま返すクラス。疑問文、否定文、命令文を判定し、疑問文にはポイントを加算する。
    """
    def get_result(self, state):
        """
        理解結果を返すメソッド
        """

        # 文章の内容と、各種文の判定結果とポイントを初期化
        sentence_meaning = {"文章": state['utt'], "疑問": 0, "否定": 0, "命令": 0}

        # 疑問文を判定するフレーズ
        question_phrases = ["ですか", "なぜ", "どうして", "いつ", "どこ", "誰が", "何を", "どれ", "どのように", "どんな", "本当に", "どうやって", "何故", "何時", "どのくらい", "何で", "どうしたの", "どうなの", "それで", "何が", "いくつ", "何回", "どうぞ", "誰の", "どのくらいの期間", "どれくらい遠い", "どんな風に", "何故なら", "どんな理由で", "どういう意味", "?"]

        # 否定文を判定するフレーズ
        negation_phrases = negation_phrases = ["ない", "ず", "ではない", "じゃない", "しない", "できない", "無い", "なかった", "ぬ", "ません","かけていない", "必要がない", "でない", "見つからない", "存在しない", "必要ではない", "否定的な", "認められない","許されない", "受け入れられない", "否定的", "認めない", "違う","違い", "無関係", "反対", "つながらない","なしで", "断る", "拒否する", "拒む"]


        # 命令文を判定するフレーズ
        command_phrases = ["してください", "しろ", "せよ", "ください", "なさい", "お願いします", "ご確認ください",]

        # 疑問文の判定とポイント加算
        for phrase in question_phrases:
            if phrase in state['utt']:
                sentence_meaning["疑問"] += 1  # 疑問文であればポイントを1加算

        # 否定文の判定
        for phrase in negation_phrases:
            if phrase in state['utt']:
                sentence_meaning["否定"] +=1
                break

        # 命令文の判定
        for phrase in command_phrases:
            if phrase in state['utt']:
                sentence_meaning["命令"] +=1
                break
        
        print(sentence_meaning)

        # return sentence_meaning  # 辞書型として返す

        return {'utt': state['utt']}  # 辞書型として返す
