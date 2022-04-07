from asyncio.windows_events import NULL
import re
import random
from analyzer import *


class Marcov:

    def make(self):
        # ログファイルを読み込む
        filename = './dics/log.txt'
        with open(filename, "r", encoding='utf_8') as f:
            text = f.read()
        # プロンプトの文字列を取り除く
        if text == '':
            return NULL
        text = re.sub('>', '', text)
        text = re.sub(
            'ptna:Repeat|ptna:Random|ptna:Pattern|ptna:Template|ptna:Marcov', '', text)
        # タイムスタンプの部分を取り除く
        text = re.sub('Ptna System Dialogue Log :.*\n', '', text)
        # 空白行が含まれていると\n\nが続くので\nを一つにする
        text = re.sub('\n\n', '\n', text)
        # ログファイルの文章を形態素に分解してリストにする

        wordlist = parse(text)
        # markov辞書を生成
        markov = {}
        p1 = ' '
        p2 = ' '
        p3 = ' '
        for word in wordlist:
            # p1,p2,p3のすべてに値が格納されているか
            if p1 and p2 and p3:
                # markovに(p1,p2,p3)キーが存在するか
                if (p1, p2, p3) not in markov:
                    markov[(p1, p2, p3)] = []
                # キーのリストにサフィックスを追加(重複あり)
                markov[(p1, p2, p3)].append(word)
            # 三つのプレフィックスの値を置き換える
            p1, p2, p3 = p2, p3, word

        # マルコフ辞書から文章を作り出す
        count = 0
        sentence = ' '
        # markovのキーをランダムに抽出し、プレピックス1~3に代入
        p1, p2, p3 = random.choice(list(markov.keys()))
        while count < len(wordlist):
            # キーが存在するかチェック
            if (p1, p2, p3) in markov:
                # 文章にする単語を取得
                tmp = random.choice(markov[(p1, p2, p3)])
                # 取得した単語をsentenceに追加
                sentence += tmp
            # 三つのプレフィックスの値を置き換える
            p1, p2, p3 = p2, p3, tmp
            count += 1

        # 開き括弧を削除
        sentence = re.sub('「', '', sentence)
        # 閉じ括弧を削除
        sentence = re.sub('」', '', sentence)

        # 生成した文章を戻り値として返す
        return sentence
