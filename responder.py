from analyzer import *
import random
from markov import *
import re
from itertools import chain


class Responder:
    """応答クラス"""

    def __init__(self, name, dictionary):
        """Responderオブジェクトの名前をnameに格納
            @param name Responderオブジェクトの名前
            @param dictionary Dictionary オブジェクト"""
        self.name = name
        self.dictionary = dictionary

    def response(self, input, mood, parts):
        """オーバーライトを前提したresponse()メソッド"""
        """戻り値空の文字列
            @param inout 入力された文字列
            @param mood 機嫌値
            @param parts 形態素解析結果のリスト
            戻り値　空の文字列"""
        return ''

    def get_name(self):
        """応答オブジェクトの名前を返す"""
        return self.name


class RepeatResponder(Responder):
    """ オウム返しのためのサブクラス"""

    def response(self, input, mood, parts):
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

    def response(self, input, mood, parts):
        """応答文字列を作って返す

            @param input 入力された文字列
            戻り値　リストからランダムに抽出した文字列"""
        return (random.choice(self.responses))


class PatternResponder(Responder):
    """パターンに反応するためのサブクラス"""

    def response(self, input, mood, parts):
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


class TemplateResponser(Responder):
    """テンプレートに反応するためのサブクラス"""

    def response(self, input, mood, parts):
        """テンプレートを使用して応答フレーズを生成する
            @param inout 入力された文字列
            @param mood 機嫌値
            @param parts 形態素解析結果のリスト
        """
        # input文字列の名詞の部分のみを格納するリスト
        keyword = []
        # テンプレート本体を格納する変数
        template = ''
        # 解析結果partsの「文字列」➡word, 「品詞情報」➡partsに順次格納
        for word, part in parts:
            # 名詞であるかをチェックしてkeywordsリストに格納
            if(keyword_check(part)):
                keyword.append(word)
            # keywordsリストに格納された名詞の数を取得
            count = len(keyword)
            # keywordsリストに一つ以上の名詞が存在し、
            # 名詞の数に対応するテンプレートが存在するかをチェック
            if (count > 0) and (str(count) in self.dictionary.template):
                # テンプレートリストから名詞の数に対応するテンプレートを
                # ランダムに抽出
                template = random.choice(self.dictionary.template[str(count)])
                # テンプレートの空欄(%noun%)に
                # keywordsに格納されている名詞を埋め込む
                for word in keyword:
                    template = template.replace('%noun%', word, 1)
                return template
            return random.choice(self.dictionary.random)


class MarkovResponder(Responder):
    """マルコフ連鎖を利用して応答を生成するためのサブクラス"""

    def response(self, input, mood, parts):
        m = []
        # 解析結果の形態素と品詞に対して反複処理
        for word, part in parts:
            # インプット文字列に名詞があればそれを含むマルコフ連鎖文を検索
            if keyword_check(part):
                # マルコフ連鎖で生成した文章を一つずつ処理
                for sentence in self.dictionary.sentences:
                    # 形態素の文字列がマルコフ連鎖の文章に含まれているか検索
                    # 最後を'.*?'にすると検索文字列だけにもマッチするので
                    # +'.*'として検索文字列だけにマッチしないようにする
                    find = '.*' + word + ' .*'
                    # マルコフ連鎖文にマッチさせる
                    tmp = re.findall(find, sentence)
                    if tmp:
                        # マッチする文章があればリストmに追加
                        m.append(tmp)
        # findall()はリストを返してくるので多重リストをフラットにする
        m = list(chain.from_iterable(m))

        # 集合に変換して重複した文章を取り除く
        check = set(m)
        # 再度、リストに戻す
        m = list(check)

        if m:
            # インプット文字列の名詞にマッチしたマルコフ連鎖文からランダムに選択
            return(random.choice(m))

        return random.choice(self.dictionary.random)
