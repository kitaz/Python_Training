"""日時データを指定の書式に変換する"""
import re
import datetime

def check_date(inyear, inmonth, inday):
    """西暦年、月、日の組み合わせの正当性をチェックする"""
    try:
        checkdatestr = "%04d/%02d/%02d"%(inyear, inmonth, inday)
#        resultdatestr = datetime.datetime.strptime(checkdatestr, "%Y/%m/%d")
        datetime.datetime.strptime(checkdatestr, "%Y/%m/%d")
        return True
    except ValueError:
        return False


def convert_wareki(inyear, inmonth, inday):
    """引数の西暦年、月、日から元号、和暦年を返す"""
    tmp = (inyear * 10000) + (inmonth * 100) + inday
    if tmp >= 19890108:
        wareki = "平成"
        wyear = inyear - 1989 +1
    elif tmp >= 19261225:
        wareki = "昭和"
        wyear = inyear - 1926 +1
    elif tmp >= 19120730:
        wareki = "大正"
        wyear = inyear - 1912 +1
    elif tmp >= 18680908:
        wareki = "明治"
        wyear = inyear - 1868 +1
    else:
        raise ValueError("システム対象外の日付が入力されています")

    return wareki, wyear


def convert_seireki(wareki, wayear):
    """引数の元号と和暦年から西暦年を返す"""
    if wareki == "平成":
        year = wayear + 1989 - 1
    elif wareki == "昭和":
        year = wayear + 1926 - 1
    elif wareki == "大正":
        year = wayear + 1912 - 1
    elif wareki == "明治":
        year = wayear + 1868 - 1
    else:
        raise ValueError("不正な元号が入力されています")

    return year


def init_func(param):
    """ paramは各関数に渡す引数。ここで初期処理を行う """
    if param == "":
        raise SyntaxError("引数がありません")

    return param


def main_func(func_data, data):
    """ dataは処理対象とする入力データ。func_dataはinit_funcの戻り値 ここで実際の変換処理を行う"""

#    print(__name__, "(B) ：", data)
    valymd = [0, 0, 0]
    valhms = [0, 0, 0]
    wayear = 0
    wareki = ""

    ptnymds = re.compile(r'([0-9]+)[/-]([0-9]+)[/-]([0-9]+)')
    ptnymdw = re.compile(r'(明治|大正|昭和|平成)([0-9]+)年([0-9]+)月([0-9]+)日')
    ptnhms = re.compile(r'([0-9]+):([0-9]+):([0-9]+)')
    ymds = ptnymds.findall(data)
    ymdw = ptnymdw.findall(data)
    hms = ptnhms.findall(data)

    # 年月日の取得
    if ymds != []:
        valymd[0] = int(ymds[0][0])
        valymd[1] = int(ymds[0][1])
        valymd[2] = int(ymds[0][2])

        # 和暦を取得
        tmp = convert_wareki(valymd[0], valymd[1], valymd[2])
        wareki = tmp[0]
        wayear = tmp[1]

    if ymdw != []:
        wareki = ymdw[0][0]
        wayear = int(ymdw[0][1])
        valymd[1] = int(ymdw[0][2])
        valymd[2] = int(ymdw[0][3])

        # 西暦を取得
        valymd[0] = convert_seireki(wareki, wayear)

    # 年月日の入力がある場合
    if ymds != [] or ymdw != []:
        # 西暦1900年未満は対象外
        if valymd[0] < 1900:
            raise ValueError("システムの対象範囲外の年が入力されています")

        # 西暦年月日が有効か確認
        if not check_date(valymd[0], valymd[1], valymd[2]):
            raise ValueError("無効な日付が入力されています")

    #　時刻の取得
    if hms != []:
        valhms[0] = int(hms[0][0])
        valhms[1] = int(hms[0][1])
        valhms[2] = int(hms[0][2])

        # 時刻が有効か確認
        if valhms[0] < 0 or valhms[0] >= 24:
            raise ValueError("無効な時刻(時)が入力されています")
        if valhms[1] < 0 or valhms[1] >= 60:
            raise ValueError("無効な時刻(分)が入力されています")
        if valhms[2] < 0 or valhms[2] >= 60:
            raise ValueError("無効な時刻(秒)が入力されています")

    # func_dataで指定された書式に変換
    outdata = func_data
    outdata = re.sub('YYYY', str(valymd[0]), outdata)
    outdata = re.sub('EE', str(wareki), outdata)
    outdata = re.sub('YY', str(wayear), outdata)
    outdata = re.sub('MM', str(valymd[1]).zfill(2), outdata)
    outdata = re.sub('mm', str(valymd[1]), outdata)
    outdata = re.sub('DD', str(valymd[2]).zfill(2), outdata)
    outdata = re.sub('dd', str(valymd[2]), outdata)
    outdata = re.sub('HH', str(valhms[0]).zfill(2), outdata)
    outdata = re.sub('MI', str(valhms[1]).zfill(2), outdata)
    outdata = re.sub('SS', str(valhms[2]).zfill(2), outdata)

#    print(__name__, "(A) ：", outdata)

    return outdata

def main():
    """main"""

if __name__ == '__main__':
    main()
