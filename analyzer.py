from janome.tokenizer import Tokenizer  # janome.tokenizerをインポート
import re


def analyze(text):
    """形態素解析を行う

        @param text 解析対象の文章
        戻り値　見出しと品詞のペアを格納した多重リスト"""
    t = Tokenizer()  # Tokenizer オブジェクトを生成
    tokens = t.tokenize(text)  # 形態素解析を実行
    result = []  # 解析結果の見出しと品詞を格納するリスト

    # リストからTokensオブジェクトを一つずつ取り出す
    for token in tokens:
        result.append([token.surface, token.part_of_speech])
    return result


def keyword_check(part):
    """品詞が名刺であるか調べる

        @param part 形態素解析の品詞の部分
        戻り値　名詞であればTrue,そうでなければFalse"""
    return re.match('名詞,(一般|固有名詞|サ変接続|形容動詞語幹)', part)


def parse(text):
    """形態素解析によって形態素を取り出す

        @param text マルコフ辞書のもとになるテキスト
        戻り値　形態素のリスト
        """
    t = Tokenizer()  # Tokenizerのオブジェクトを生成
    tokens = t.tokenize(text)  # 形態素分析を実行
    result = []  # 形態素を格納するリスト
    for token in tokens:
        result.append(token.surface)
    return result
