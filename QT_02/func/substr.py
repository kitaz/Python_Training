"""startからlenで指定された文字数分のみ切り出す"""
import re

def init_func(param):
    """ paramは各関数に渡す引数。ここで初期処理を行う """
    print(param)

    pattern = re.compile(r'([0-9]+),([0-9]+)')
    for stpos, lennum in pattern.findall(param):
        print(stpos, lennum)

    # 文字列の長さ、位置、などのチェック
    # 3番目の引数とかは？

    func_data = (int(stpos),int(lennum))
    return func_data

def main_func(num, data):
    """ dataは処理対象とする入力データ。func_dataはinit_funcの戻り値 ここで実際の変換処理を行う"""

    print(__name__, "(B) ：", data)
    data = data[(num[0]-1):(num[0]+num[1]-1)]
    print(__name__, "(A) ：", data)

    return data

def main():
    pass

if __name__ == '__main__':
    main()