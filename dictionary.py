import re
import random


class Dictionary:
    def __init__(self):
        self.random = []
        #   ランダム辞書ファイルオープン
        rflie = open('dics/random.txt', 'r', encoding='utf_8')
        #   各行を要素としてリストに格納
        r_lines = rflie.readlines()
        rflie.close()

        #   末尾の改行と空白文字を取り除いて
        #   インスタンス変数(リスト)に格納
        self.random = []
        for line in r_lines:
            str = line.rstrip('\n')
            if(str != ''):
                self.random.append(str)

        #   パターン辞書オープン
        pfile = open('dics/pattern.txt', 'r', encoding='utf_8')
        # 各行を要素としてリストに格納
        p_lines = pfile.readlines()
        pfile.close()

        #   末尾の改行と空白文字取り除いて
        #   インスタンス変数(リスト)に格納
        self.new_lines = []
        for line in p_lines:
            str = line.rstrip('\n')
            if(str != ''):
                self.new_lines.append(line)

        #   辞書型のインスタンス変数を用意
        self.pattern = {}
        #   1行をタブで切り分けて辞書オブジェクトに格納
        #   pattern キー　正規表現のパターン
        #　phrases キー　応答列
        for line in self.new_lines:
            ptn, prs = line.split('\t')
            self.pattern.append(ParseItem(ptn, prs))


class ParseItem:
    SEPARATOR = '^((-?\d+)##)?(.*)$'

    def __init__(self, pattern, phrases):
        """@param pattern パターン
           @param phrases 応答列
        """
        # 辞書のパターンの部分にSEPARATORをパターンマッチさせる
        m = re.findall(ParseItem.SEPARATOR, pattern)
        # インスタンス変数modifyに0を代入
        self.modify = 0
        # マッチ結果の整数の部分が空いでなければ値を再代入
        if m[0][1]:
            print(m)
            self.modify = int(m[0][1])
        #   インスタンス変数patternにマッチ結果のパターン部分を代入
        self.pattern = m[0][2]
        self.phrases = []  # 応答列を保持するインスタンス変数
        self.dic = {}  # インスタンス変数
        #  引数で渡された応答列を'|'で分割し
        #  個々の要素に対してSEPARATORをパターンマッチさせる
        #  self.phrases['need' = 応答列の整数部分, 'phrases'=応答列の文字列部分]
        for phrase in phrases.split('|'):
            # 応答列に対してパターンマッチを行う
            m = re.findall(ParseItem.SEPARATOR, phrase)
            # 'need'キーの値を整数部分m[0][1]にする
            # ’phrase'キーの値を応答文字列m[0][2]にする
            self.dic['need'] = 0
            if m[0][1]:
                self.dic['need'] = int(m[0][1])
            self.dic['phrase'] = int(m[0][2])
            # 作成した辞書をphrasesリストに追加
            self.phrases.append(self.dic.copy())

    def match(self, str):
        """self.pattern(各行ごとの正規表現)を
        インプット文字列にパターンマッチ"""
        return re.search(self.pattern, str)

    def choice(self, mood):
        """@param mood 現在の機嫌値"""

        choices = []
        # self.phrasesが保持するリストの要素(辞書)を反複処理する
        for p in self.phrases:
            # self.phrasesの'need'キーの数値と
            # パラメーターmoodをsuitable()に渡す
            # 結果がtrueであればchoicesリストに'phrase'キーの応答列を追加
            if(self.suitable(p['need'], mood)):
                choices.append(p['phrases'])
            # choices リストが空であればNoneを返す
            if(len(choices) == 0):
                return None
                # choicesリストが空でなければランダムに応答文字列を選択して返す
            return random.choice(choices)

    def suitable(self, need, mood):
        """インスタンス変数phrases(リスト)の要素('need''phrasesの辞書)
            @param need 必要機嫌値
            @param mood 現在の機嫌値"""
        # 必要機嫌値が0であればTrueを返す
        if(need == 0):
            return True
        # 必要機嫌値がプラスの場合は機嫌値が必要機嫌値をこえているか判定
        elif(need > 0):
            return mood > need
        else:
            return mood < need