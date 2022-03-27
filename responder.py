import random
import re


class Responder:
    """応答クラス"""

    def __init__(self, name, dictionary):
        """Responderオブジェクトの名前をnameに格納
            @param name Responderオブジェクトの名前
            @param dictionary Dictionary オブジェクト"""
        self.name = name
        self.dictionary = dictionary

    def response(self, input, mood):
        """オーバーライトを前提したresponse()メソッド"""
        """戻り値空の文字列
            @param inout 入力された文字列"""
        return ''

    def get_name(self):
        """応答オブジェクトの名前を返す"""
        return self.name


class RepeatResponder(Responder):
    """ オウム返しのためのサブクラス"""

    def response(self, input, mood):
        """応答文字列を作って返す
        @param input 入力された文字列"""
        return '{}ってなに？'.format(input)


class RandomResponder(Responder):
    """ランダムな応答のためのサブクラス"""

    def __init__(self, name, dictionary):
        """Responder オブジェクトの名前を引数として
        スーパークラスの__init__()を呼び出す
        ランダムに抽出するメッセージを格納したリストを作成

        @param name Responderオブジェクトの名前
        """
        super().__init__(name, dictionary)

        self.responses = []
        rFile = open('dics/random.txt', 'r', encoding='utf_8')
        rlines = rFile.readlines()
        for str in rlines:
            str = str.rstrip('\n')
            if(str != 0):
                self.responses.append(str)
        rFile.close()

    def response(self, input, mood):
        """応答文字列を作って返す

            @param input 入力された文字列
            戻り値　リストからランダムに抽出した文字列"""
        return (random.choice(self.responses))


class PatternResponder(Responder):
    """パターンに反応するためのサブクラス"""

    def response(self, input, mood):
        """パターンにマッチした場合に応答文字列を作って返す
            @param input 入力された文字列
            @param mood 機嫌値"""
        self.resp = None
        for ptn_item in self.dictionary.pattern:
            # match()でインポットした文字列にパターンマッチを行う
            m = ptn_item.match(input)
            # マッチした場合は機嫌値moodを引数にしてchoice()を実行
            # 戻り値の応答文字列、またはNoneを取得
            if(m):
                self.resp = ptn_item.choice(mood)
            # choice()の戻り値がNoneでない場合は
            # 応答文字列の中の%match%をインポットされた文字列中の
            # マッチした文字列に置き換える
            if self.resp != None:
                return re.sub('%match', m.group(), self.resp)
        return random.choice(self.dictionary.random)
