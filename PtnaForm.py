from re import L
import tkinter as tk
from typing import overload
from ptna import *
from datetime import datetime
import tkinter.messagebox

"""グローバル変数の定義"""

entry = None  # 入力エリアのオブジェクトを保持
response_area = None        # 応答エリアのオブジェクトを保持
lb = None                        # ログ表示用リストボックスを保持
action = None                  # オプションメニューの状態を保持
ptna = Ptna('ptna')  # Ptnaオブジェクトを保持
on_canvas = None  # Canvasオブジェクトを保持
ptna_imges = []  # イメージを保持
log = []  # インプット文字列を保持


def putlog(str):
    """対話ログをリストボックスに追加する関数
    @str 入力文字列または応答メッセ―ジ"""
    lb.insert(tk.END, str)
    # インプットと応答をリストlogに追加
    log.append(str + '\n')


def prompt():
    """ピティナのプロンプトを作る関数"""
    p = ptna.name
    if(action.get()) == 0:
        p += ':' + ptna.responder.name
    elif (action.get()) == 1:
        p += ':'
    return p + '>'


def changeImg(img):
    """画像をセットする関数"""
    canvas.itemconfig(
        on_canvas,
        image=ptna_imges[img]
    )


def changeLooks():
    m = ptna.emotion.mood
    if -5 <= m <= 5:
        changeImg(0)
    elif -10 <= m < 5:
        changeImg(1)
    elif -15 <= m < -10:
        changeImg(2)
    else:
        changeImg(3)


@overload  # button click event
def talk():
    """対話を行う関数
            ’Ptnaクラスのdialogue()を実行して応答メッセージを取得
            入力文字列をよび応答メッセージをログに出力
    """
    value = entry.get()
    # 入力エリアが来入力の場合
    if not value:
        response_area.configure(text='なに?')
    # 入力されていたら対話オブジェクトを実行
    else:
        # 入力文字列を引数にしてdialogue()の結果を取得
        response = ptna.dialogue(value)
        # 応答メッセージを表示
        response_area.configure(text=response)
        # 入力文字列引数にしてputlog()を呼ぶ
        putlog('>' + value)
        # 応答メッセージを引数にしてputlog()を呼ぶ
        putlog(prompt() + response)
        # 入力エリアをクリア
        entry.delete(0, tk.END)

    changeLooks()


@overload  # enter key event
def talk(event):
    """対話を行う関数
            ’Ptnaクラスのdialogue()を実行して応答メッセージを取得
            入力文字列をよび応答メッセージをログに出力
    """
    value = entry.get()
    # 入力エリアが来入力の場合
    if not value:
        response_area.configure(text='なに?')
    # 入力されていたら対話オブジェクトを実行
    else:
        # 入力文字列を引数にしてdialogue()の結果を取得
        response = ptna.dialogue(value)
        # 応答メッセージを表示
        response_area.configure(text=response)
        # 入力文字列引数にしてputlog()を呼ぶ
        putlog('>' + value)
        # 応答メッセージを引数にしてputlog()を呼ぶ
        putlog(prompt() + response)
        # 入力エリアをクリア
        entry.delete(0, tk.END)

    changeLooks()


def writeLog():
    """ログファイルに辞書を更新したに日時を記録"""
    # ログを作成
    now = 'Ptna System Dialogue Log : ' + \
        datetime.now().strftime('%Y-%m-%d %H:%m:%S' + '\n')
    log.insert(0, now)
    # ログファイルへの書き込む
    with open('dics/log.txt', 'a', encoding='utf_8') as f:
        f.writelines(log)
    # ====================================================
    #  画面を猫画する関数
    # ====================================================


def run():
    # グローバル変数を使用するための記述
    global entry, response_area, lb, action, on_canvas, canvas, ptna_imges

    # メインウィンドウを作成
    root = tk.Tk()
    # ウィントウサイズを定義
    root.geometry('880x560')
    # ウィンドウタイトルを定義
    root.title('Intelligent Agent : ')
    # フォントの用意
    font = ('Helevetica', 14)
    font_log = ('Helevetica', 11)

    def callback():
        """終了時の処理"""
        # メッセージボックスの[OK]ボタンクリック時の処理
        if tkinter.messagebox.askyesno('Quit?', 'ランダム辞書を更新してもいい？'):
            ptna.save()  # 記憶メソッド実行
            writeLog()  # ログを保存
            root.destroy()
        # キャンセルボタンクリック
        else:
            root.destroy()
    root.protocol('WM_DELETE_WINDOW', callback)

    # メニューバーの作成
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    # ファイルメニュー
    filemenu = tk.Menu(menubar)
    menubar.add_cascade(label='ファイル', menu=filemenu)
    filemenu.add_command(label='問じる', command=callback)
    # オプションメニュー
    action = tk.IntVar()
    optionmenu = tk.Menu(menubar)
    menubar.add_cascade(label='オプション', menu=optionmenu)
    optionmenu.add_radiobutton(
        label='Responderを表示',
        variable=action,
        value=0
    )
    optionmenu.add_radiobutton(
        label='Responderを表示しない',
        variable=action,
        value=1
    )

    # キャンバスの作成
    canvas = tk.Canvas(
        root,  # 親要素をメインウィンドウに定義
        width=500,  # 幅
        height=300,  # 高さ
        relief=tk.RIDGE,  # 枠線
        bd=2  # 枠線の幅
    )
    canvas.place(x=370, y=0)  # メインウィンドウ上に表示
    # イメージを用意
    ptna_imges.append(tk.PhotoImage(file="images/talk.gif"))
    ptna_imges.append(tk.PhotoImage(file="images/empty.gif"))
    ptna_imges.append(tk.PhotoImage(file="images/angry.gif"))
    ptna_imges.append(tk.PhotoImage(file="images/happy.gif"))
    on_canvas = canvas.create_image(
        0,
        0,
        image=ptna_imges[0],  # 配置するイメージオブジェクトを指定
        anchor=tk.NW          # 配置の起点となる位置を右上隅に指定
    )

    # 応答エリアを作成
    response_area = tk.Label(
        root,
        width=50,
        height=10,
        bg='yellow',
        font=font,
        relief=tk.RIDGE,
        bd=2
    )
    response_area.place(x=370, y=305)

    # フレームの作成
    frame = tk.Frame(
        root,  # 新要素はメインウィンドウ
        relief=tk.RIDGE,
        borderwidth=4
    )
    # 入力ボックスの作成
    entry = tk.Entry(
        frame,
        width=70,
        font=font
    )
    entry.pack(side=tk.LEFT)  # フレームに右詰めで配置する
    entry.focus_set()  # 入力ボックスにフォーカスを当てる
    # ボタンの作成
    button = tk.Button(
        frame,
        width=15,
        text='話す',
        command=talk  # クリックの時にtalk()関数を呼ぶ
    )
    root.bind("<Return>", talk)
    button.pack(side=tk.LEFT)  # フレームの右詰めで配置
    frame.place(x=30, y=520)

    # リストボックスを作成
    lb = tk.Listbox(
        root,
        width=42,
        height=30,
        font=font_log
    )
    # 縦のスクロールバーを生成
    sb1 = tk.Scrollbar(
        root,
        orient=tk.VERTICAL,  # 縦方向のスクロールバーにする
        command=lb.yview  # スクロール時にListboxのyview()メソッドを呼ぶ
    )
    # 横のスクロールバーを生成
    sb2 = tk.Scrollbar(
        root,
        orient=tk.HORIZONTAL,
        command=lb.xview
    )
    # リストボックスとスクロールバー連動する
    lb.configure(yscrollcommand=sb1.set)
    lb.configure(xscrollcommand=sb2.set)
    # grid()でリストボックス,スクロールバーを画面上に配置
    lb.grid(row=0, column=0)
    sb1.grid(row=0, column=1, sticky=tk.NS)
    sb2.grid(row=1, column=0, sticky=tk.EW)

    # メインループ
    root.mainloop()


# =================================================
# プログラムの起点
# =================================================
if __name__ == '__main__':
    run()
