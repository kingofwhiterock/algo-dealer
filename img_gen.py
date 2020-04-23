# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# #########################################################################
#
# 2020/04/19
# written by: Apoi
# version: 0.1
#
# #########################################################################
#
# PROJECT:
# * ImageGenerator
#
# FILE PURPOSE:
# * to generate algo image
#
# FILE ISSUE
# * have to paste hand, how we get appropriate pos?
# * current hand
#
# #########################################################################


# #########################################################################
# library importing
# #########################################################################
from PIL import Image
from math import floor
import time

import boto3


# #########################################################################
# class
# #########################################################################
class ImageGenerator:
    """to generate algo image"""
    def __init__(self, user_id, player0_cards, player1_cards, player0_isopen, player1_isopen, attacker,
                 hand=None, *args, **kwargs):
        self.usr = user_id
        self.img = [Image.open('img/{}.png'.format(i)) for i in range(28)]
        self.p0_c = list(map(int, player0_cards.split()))
        self.p0_cr = list(reversed(self.p0_c))
        self.p1_c = list(map(int, player1_cards.split()))
        self.p1_cr = list(reversed(self.p1_c))
        self.p0_o = list(map(int, player0_isopen.split()))
        self.p0_or = list(reversed(self.p0_o))
        self.p1_o = list(map(int, player1_isopen.split()))
        self.p1_or = list(reversed(self.p1_o))
        self.atkr = int(attacker)
        if hand:
            self.hand = int(hand)
        else:
            self.hand = hand
        self.img_name = floor(time.time())

    def main(self):
        # player0's view
        bs = self.img[27].copy()
        if self.atkr:
            bs.paste(self.img[26], (20, 50))
        else:
            bs.paste(self.img[26], (20, 220))

        for x, i in enumerate(self.p1_cr):
            tmp = 150 + x * 100
            if self.p1_or[x]:
                # open
                bs.paste(self.img[i], (tmp, 0))
            else:
                # closed
                bs.paste(self.img[24 + i % 2], (tmp, 0))

        for x, i in enumerate(self.p0_c):
            tmp = 150 + x * 100
            if self.p0_o[x]:
                bs.paste(self.img[i], (tmp, 200))
            else:
                bs.paste(self.img[i], (tmp, 360))

        # hand
        if self.atkr == 0:
            bs.paste(self.img[self.hand], (1389, 360))
        else:
            bs.paste(self.img[24 + self.hand % 2], (1389, 0))

        bs.save('generated_img/{}.png'.format(self.img_name))

        # player1's view
        bs = self.img[27].copy()
        if self.atkr:
            bs.paste(self.img[26], (20, 220))
        else:
            bs.paste(self.img[26], (20, 50))

        for x, i in enumerate(self.p0_cr):
            tmp = 150 + x * 100
            if self.p0_or[x]:
                bs.paste(self.img[i], (tmp, 0))
            else:
                bs.paste(self.img[24 + i % 2], (tmp, 0))

        for x, i in enumerate(self.p1_c):
            tmp = 150 + x * 100
            if self.p1_o[x]:
                bs.paste(self.img[i], (tmp, 200))
            else:
                bs.paste(self.img[i], (tmp, 360))

        # hand
        if self.atkr == 1:
            bs.paste(self.img[self.hand], (1389, 360))
        else:
            bs.paste(self.img[24 + self.hand % 2], (1389, 0))

        bs.save('generated_img/{}.png'.format(self.img_name + 1))

        # ########################################################################################
        # -*-*-*- AWS upload code -*-*-*- ########################################################
        # ########################################################################################
        #
        # bucket_name = ""
        # s3 = boto3.resource('s3')
        # for i in range(2):
        #     s3.Bucket(bucket_name).upload_file('{}.png'.format(self.img_name + i), '{}.png'.format(self.img_name + i))
        #
        # ########################################################################################

        return self.img_name


if __name__ == '__main__':
    pass
