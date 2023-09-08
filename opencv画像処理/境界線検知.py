import os
import numpy as np
import cv2
import pandas as pd
from operator import itemgetter

"""=======================
Open CV パス 日本語対応
https://qiita.com/SKYS/items/cbde3775e2143cad7455
======================="""


def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


"""=========================================
水平線の検知
========================================="""


def get_vertical_line(image_path):
    # https://way2se.ringtrees.com/py_cv2-003/
    bgr_img = imread(image_path)
    img = bgr_img[:, :, 0]
    height, width = img.shape
    minlength = width * 0.4
    gap = 0
    judge_img = cv2.bitwise_not(img)
    # 検出しやすくするために二値化
    # th, judge_img = cv2.threshold(judge_img, 128, 255, cv2.THRESH_BINARY)
    th, judge_img = cv2.threshold(judge_img, 210, 255, cv2.THRESH_BINARY)
    imwrite('out-proccess.jpg', judge_img)
    # 平行な横線のみを取得
    lines = cv2.HoughLinesP(judge_img, rho=1, theta=np.pi/360, threshold=100,
                            minLineLength=minlength, maxLineGap=gap)
    line_list = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # 傾きが threshold_slope px以内の線を横線と判断
        threshold_slope = 1
        if abs(y1 - y2) < threshold_slope:
            whiteline = 3
            lineadd_img = cv2.line(
                bgr_img, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 0, 255), whiteline)
            x1 = line[0][0]
            y1 = line[0][1]
            x2 = line[0][2]
            y2 = line[0][3]
            line = (x1, y1, x2, y2)
            line_list.append(line)
    # y座標をキーとして並び変え
    line_list.sort(key=itemgetter(1, 0, 2, 3))
    # !!! 合計の長さでy座標の位置を決定 --ここから

    #-- ここまで
    line_list = pd.DataFrame(line_list)
    print('line_list_pd')
    print(line_list)
    imwrite('out.jpg', lineadd_img)


"""=======================================
メイン
========================================"""

if __name__ == '__main__':
    # main
    test2image = './テスト画像/test-2.jpg'
    get_vertical_line(test2image)
