# -*- coding:utf-8 -*-
import os
import copy
import time
import sys
import random
import pygame
from pygame.locals import *

SCREEN_SET = Rect(0, 0, 800, 700)

###################################
#
# 　ここからメイン
#
###################################
def main():
    # 変数の初期化
    x1_pt = 50
    y1_pt = 450
    #0:up  1:right 2:down 3:left
    direction = 0       #最初は上向き　UP
    score = 0
    list1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
             [1, 0, 1, 0, 1, 0, 0, 0, 1, 1],
             [1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
             [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 1, 1, 1, 1],
             [1, 0, 1, 0, 1, 1, 1, 1, 3, 1],
             [1, 2, 1, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    pygame.init()  # Pygameの初期化
    screen = pygame.display.set_mode((800, 700))  # 画面サイズを指定して画面を生成
    pygame.display.set_caption("GAME")  # タイトルバーに表示する文字
    screen.fill((0, 0, 0))  # 画面を黒色に塗りつぶし
    list0 = copy.deepcopy(list1)  # ディープコピー
    screen.fill((0, 0, 0))  # ウィンドウの背景色
    face_img = pygame.image.load("./img/mas_face.jpg")
    put_img(screen, face_img, 400, 100)  # 画面に顔を置く

    # 初期の猫の色を決める
    cat_color = 5

    # ココからメインのループ
    while (1):
        print(x1_pt)
        print(y1_pt)
        print(direction)
        put_frame(screen, list0)  # 画面に枠を置く
        time.sleep(0.05)  # 速度調整のsleep
        x2_pt, y2_pt = 0, 0

        #自動移動処理
        x2_pt, y2_pt,direction = think_proc(x1_pt, y1_pt,direction, list0)
        
        # ゴールしたかチェック
        if (list0[int(y2_pt / 50)][int(x2_pt / 50)]) == 3:
            print('GOAL')
            time.sleep(5)  # 速度調整のsleep
            pygame.quit()  # Pygameの終了(画面閉じられる)
            sys.exit()

        # 前位置ブロックの削除
        list0 = set_block_list(int(x1_pt / 50), int(y1_pt / 50), 0, list0)
        y1_pt = y2_pt  #予定y位置に移動
        x1_pt = x2_pt  #予定x位置に移動
        # 移動ブロックの当たり判定MAP固定
        list0 = set_block_list(int(x1_pt / 50), int(y1_pt / 50), cat_color, list0)
        # 画面に枠を置く
        put_frame(screen, list0)

        # 移動ブロック（猫）を画面に置く
        put_drop_cat(screen, x1_pt, y1_pt,direction)

        pygame.display.update()  # スクリーンの一部分のみを更新します。この命令はソフトウェア側での表示処理に最適化されています。

        put_score(screen, score)  # スコアの表示


## スコアの表示
def put_score(screen, score):
    font = pygame.font.Font(None, 40)  # フォントの設定(55px)
    put_img(screen, get_block_img(0), 400, 50)  # スコア表示部分に黒ブロックを置いて消す
    put_img(screen, get_block_img(0), 450, 50)  # スコア表示部分に黒ブロックを置いて消す
    put_img(screen, get_block_img(0), 500, 50)  # スコア表示部分に黒ブロックを置いて消す
    screen.blit(font.render(str(score), True, (255, 255, 0)), [400, 50])  # 文字列の表示位置


## ブロックの削除対象チェックと削除
def chek_delete_cat(x, y, list0: list, score):
    if y > 6:
        # 底から2段目以下ならば3個並んでいないので即返る
        return list0, score
    elif y < 2:
        # 天から2段目以上ならば3個並んでいないので即返る
        return list0, score
    cat0 = list0[y][x]
    cat1 = list0[y + 1][x]
    cat2 = list0[y + 2][x]
    if (cat0 == cat1) and (cat1 == cat2):
        # 3個並んでる
        list0[y][x] = 0
        list0[y + 1][x] = 0
        list0[y + 2][x] = 0
        score = score + 3
    return list0, score


## ブロックの当たり判定　※簡易なので下しか見ていない。本来は横も見る
def chek_collision(x, y, list0: list) -> int:
    block = list0[y][x]
    if block == 1:
        return True
    else:
        return False

## 着地したブロックを変数に書き込む
def set_block_list(x, y, cat_col, list0: list) -> list:
    list0[y][x] = cat_col
    return list0


#自動動作させる
def think_proc(x1_pt: int, y1_pt: int, direction:int , list0:list) -> object:
    #direction = 0
    #          0:up    1:right 2:down 3:left
    xy_add = [[0, -1], [1, 0], [0, 1],[-1, 0]]
    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:  # 閉じるボタンが押されたら終了
            pygame.quit()  # Pygameの終了(画面閉じられる)
            sys.exit()

    #迷路解法として右手法を使用する
    #右手の当たりチェック
    xadd,yadd=xy_add[((direction+1)&3)]
    x_now = (x1_pt / 50) + xadd
    y_now = (y1_pt / 50) + yadd
    r_collision: bool = chek_collision(int(x_now), int(y_now), list0)
    #前方の当たりチェック
    xadd,yadd=xy_add[direction]
    x_now = (x1_pt / 50) + xadd
    y_now = (y1_pt / 50) + yadd
    f_collision: bool = chek_collision(int(x_now), int(y_now), list0)
    if r_collision and (not f_collision):
        # 右に壁があり、前方に壁がない場合、一歩前進
        x1_pt = x_now*50
        y1_pt = y_now*50
    elif ((not f_collision) and (not r_collision)) or  ( f_collision and (not r_collision)) :
        # 前方に壁がなく、右に壁がない場合は、右を向き一歩進む
        # 前方に壁が有り、右に壁がない場合は、右を向き一歩進む
        direction = ((direction + 1) & 3)
        xadd,yadd=xy_add[direction]
        x_now = (x1_pt / 50) + xadd
        y_now = (y1_pt / 50) + yadd
        x1_pt = x_now*50
        y1_pt = y_now*50
    elif f_collision and r_collision:
        # 右に壁があり、前方に壁がある場合は、左を向く
        direction = ((direction +1) & 3)
        direction = ((direction +1) & 3)
        direction = ((direction +1) & 3)

    return x1_pt, y1_pt,direction

## キー入力など、イベント処理
##　矢印キーでブロックの座標他仕込みも行う
def event_proc(x1_pt: int, y1_pt: int) -> object:
    # イベント処理
    for event in pygame.event.get():
        if event.type == QUIT:  # 閉じるボタンが押されたら終了
            pygame.quit()  # Pygameの終了(画面閉じられる)
            sys.exit()
        # キー操作(追加したとこ)
        elif event.type == KEYDOWN:
            print("event.type=" + str(event.type))
            print("event.key=" + str(event.key))
            if event.key == K_LEFT:
                print("←")
                x1_pt -= 50
            elif event.key == K_RIGHT:
                print("→")
                x1_pt += 50
            elif event.key == K_UP:
                print("↑")
                y1_pt -= 50
            elif event.key == K_DOWN:
                print("↓")
                y1_pt += 50
    # 　座標のみ返す
    return x1_pt, y1_pt

##　指定のブロック絵柄（猫など）をイメージオブジェクトに入れて返す
def get_block_img(cat_color: int):
    if cat_color == 0:
        ret_img = pygame.image.load("./img/blank.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 1:
        ret_img = pygame.image.load("./img/block.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 2:
        ret_img = pygame.image.load("./img/neko0.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 3:
        ret_img = pygame.image.load("./img/neko1.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 4:
        ret_img = pygame.image.load("./img/neko2.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 5:
        ret_img = pygame.image.load("./img/neko3.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 6:
        ret_img = pygame.image.load("./img/neko4.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 7:
        ret_img = pygame.image.load("./img/neko5.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 8:
        #ret_img = pygame.image.load("./img/cat.png")  # 画像を読み込む(今回追加したとこ)
        ret_img = pygame.image.load("./img/u_cat.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 9:
        ret_img = pygame.image.load("./img/r_cat.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 10:
        ret_img = pygame.image.load("./img/d_cat.png")  # 画像を読み込む(今回追加したとこ)
    elif cat_color == 11:
        ret_img = pygame.image.load("./img/l_cat.png")  # 画像を読み込む(今回追加したとこ)
    else:
        ret_img = pygame.image.load("./img/block.png")  # 画像を読み込む(今回追加したとこ)
    return ret_img


##　移動ブロック（猫）を画面に置く
def put_drop_cat(screen, x1_pt: int, y1_pt: int,direction: int):
    # direction  0:上向き    1:右向き    2:下向き    3:左向き
    cat_no= 8 + direction
    drop_cat_img = get_block_img(cat_no)
    screen.blit(drop_cat_img, (x1_pt, y1_pt))


##フレーム内を描き直す
def put_frame(screen, list):
    # 枠のブロックを表示する。
    y_idx = 0
    for val1 in list:
        x_idx = 0
        for val2 in val1:
            # idBlokck = list2[0][index2]
            id_blokck = int(val2)
            put_block(screen, get_block_img(id_blokck), x_idx, y_idx)
            x_idx += 1
        y_idx += 1


## 絵を表示する
def put_img(screen, img_obj, x, y):
    screen.blit(img_obj, (x, y, 50, 50))  # 絵を画面に貼り付ける


## ブロックを画面に置く ※50ドット単位
def put_block(screen, img_obj, x, y):
    screen.blit(img_obj, (50 * x, 50 * y, 50, 50))  # 絵を画面に貼り付ける


##画面に四角を書く
def put_rect(screen, x, y):
    RED = (255, 0, 0)
    rect = ((50 * x), (50 * y), 50, 50)
    pygame.draw.rect(screen, RED, rect)
    # screen.blit(font.render( in_chr, True, (255, 255, 0)), [(50 * x_idx), (40 * y_idx)])  # 文字列の表示位置


##　既定　これが無いと動かない    #############################
if __name__ == "__main__":
    main()
