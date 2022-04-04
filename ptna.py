from responder import *
from dictionary import *
from analyzer import *


class Ptna:
    """ピティナの本体クラス"""

    def __init__(self, name):
        """Ptna オブジェクトの名前をnameに格納
        Responder オブジェクトを生成して responderに格納
        @param name Ptnaオブジェクトの名前"""
        # Dictionaryを生成
        self.dictionary = Dictionary()
        self.name = name
        self.emotion = Emotion(self.dictionary)
        self.res_random = RandomResponder('Random', self.dictionary)
        self.res_what = RepeatResponder('Repeat', self.dictionary)
        self.res_pattern = PatternResponder('Pattern', self.dictionary)
        self.res_template = TemplateResponser('Template', self.dictionary)
        self.res_markov = MarkovResponder('Marcov', self.dictionary)
        # responderの初期値をRepeatResponderにする

    def dialogue(self, input):
        """応答オブジェクトのresponse()を呼び出して
        応答文字列を取得する

        @param input ユーザーによって入力された文字列
        戻り値　応答文字列"""
        # 0が1をランダムに生成
        x = random.randint(1, 100)
        self.emotion.update(input)
        # インプット文字列を解析
        parts = analyze(input)
        # print(parts)
        if x <= 30:
            self.responder = self.res_pattern
        elif 31 <= x <= 50:
            self.responder = self.res_template
        elif 51 <= x <= 70:
            self.responder = self.res_random
        elif 71 <= x <= 90:
            self.responder = self.res_markov
        else:
            self.responder = self.res_what
        #　応答フレーズを生成
        resp = self.responder.response(input, self.emotion.mood, parts)
        self.dictionary.study(input, parts)
        return resp

    def save(self):
        """Dictionaryのsave()を呼ぶ中継メソッド"""
        self.dictionary.save()

    def get_responder_name(self):
        """応答オブジェクトの名前を返す"""
        return self.responder.name

    def get_name(self):
        """Ptnaオブジェクトの名前を返す"""
        return self.name


class Emotion:
    """ピティナの感情モデル"""
    # 機嫌値の上限/加減と回復値を設定
    MOOD_MIN = -15
    MOOD_MAX = 15
    MOOD_RECOVERY = 0.5

    def __init__(self, dictionary):
        """Dictionaryオブジェクトをdictionaryに格納
            機嫌値moodを0で初期化

            @param dictionary Dictionaryオブジェクト"""

        self.dictionary = dictionary
        # 機嫌値を保持するインスタンス変数
        self.mood = 0

    def update(self, input):
        """ユーザーからの入力をパラメーターinputで受け取り
            パターン辞書にマッチさせて機嫌値を変動させる

            @param input ユーザーからの入力"""
        # パターン辞書の各行を繰り返しパターンマッチさせる
        for ptn_item in self.dictionary.pattern:
            if ptn_item.match(input):
                self.adjust_mood(ptn_item.modify)
                break

        # 機嫌を徐々にもとに戻す処理
        if self.mood < 0:
            self.mood += Emotion.MOOD_RECOVERY
        elif self.mood > 0:
            self.mood -= Emotion.MOOD_RECOVERY

    def adjust_mood(self, val):
        """機嫌値を加減させる増減させる
            @param val 機嫌変動値"""
        # 機嫌値moodの値を機嫌変動値によって増減する
        self.mood += int(val)
        # MOOD_MAXとMOOD_MINと比較して、機嫌値が取得る範囲に収める
        if self.mood > Emotion.MOOD_MAX:
            self.mood = Emotion.MOOD_MAX
        elif self.mood < Emotion.MOOD_MIN:
            self.mood = Emotion.MOOD_MIN
