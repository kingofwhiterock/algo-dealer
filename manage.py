# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# #########################################################################
# 
# 2020/04/19
# written by: Apoi
# version: 0.3.0
# 
# #########################################################################
# 
# PROJECT:
# * Algo Dealer
# 
# FILE PURPOSE: 
# * to analyze messages from users and send them to appropriate processing.
# * return the result messages and files to line-bot sending system
#
# FILE ISSUE
# * at least one attack should be done, so hide-without-attack-action should be banned
# 
# #########################################################################


# #########################################################################
# library importing
# #########################################################################
from collections import deque
import random
import pymysql.cursors
import re
import os
# #########################################################################
# python file importing
# #########################################################################
from err import *
from img_gen import ImageGenerator
# #########################################################################
# class
# #########################################################################


class AlgoManager:
    def __init__(self, user_id, user_text, *args, **kwargs):
        self.user_id = user_id
        self.user_text = AlgoManager.trs(user_text)
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password=os.environ['MySQL_pw'],
                                          db='bot',
                                          cursorclass=pymysql.cursors.DictCursor)
        self.card_status = ' '.join(map(str, [0, 0, 0, 0]))

        self.usage_text = "-*- Syntax Error -*-\n\"$help\" to see the help utility."

        self.player_text = "ALGO Basic Dealer\nTell another player the room number and let's play the game!" \
                           "\n\"$help\" to see the help utility."

        self.joined_text = "ALGO Basic Dealer\nlet's play the game!\n\"$help\" to see the help utility."

        self.invalid_text = "Sorry, this is an invalid command :("

    @staticmethod
    def trs(text: str) -> str:
        """translate ZEN-kaku chars to HAN-kaku chars"""
        text = text.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
        text = text.replace('　', ' ')
        return text

    @staticmethod
    def help():
        """return help text"""
        # print(os.chdir())
        with open('C:/Users/Apoi/PycharmProjects/bot/usage.txt', mode='r') as f:
            text = f.read()
            return text

    def new_player(self):
        """a player who is not playing the Algo game"""
        # create method
        if "$create" in self.user_text and "algo" in self.user_text:
            # TODO: syntax check
            #       inputted room number existing check
            #       create room
            #       create cards, isOpen, yamafuda
            #       updating database

            # command syntax check
            try:
                command = self.user_text.split()
                room_id = command[2]
                if len(room_id) != 4:
                    raise RoomNumberError
            except IndexError:
                text = self.usage_text
                return {self.user_id: text}
            except RoomNumberError:
                text = self.usage_text
                return {self.user_id: text}

            # search inputted number
            with self.connection.cursor() as cursor:
                sql = 'select * from algo where room_id = %s'
                cursor.execute(sql, int(room_id))
                results = cursor.fetchall()

            # already used number or not
            if results:
                text = 'Sorry, this room number is already used.\n' \
                       'Try another number :('
                return {self.user_id: text}

            # f-command check
            # 0: no f-command, 1: f-command without friend code, 2: f-command with friend code
            f_command = 0
            if '-f' in command:
                idx = command.index('-f')
                try:
                    friend_code = int(command[idx + 1])
                    if len(str(friend_code)) == 18:
                        f_command = 2
                    else:
                        f_command = 1
                except (IndexError, ValueError):
                    f_command = 1

            # create room, cards, isOpen, yamafuda
            # create yamafuda
            yamafuda = list(range(0, 24))
            random.shuffle(yamafuda)
            yamafuda = deque(yamafuda)

            # create players cards
            player0_cards = []
            player1_cards = []

            for i in range(4):
                player0_cards.append(yamafuda.popleft())
            player0_cards.sort()
            player0_cards_str = ' '.join(map(str, player0_cards))

            for i in range(4):
                player1_cards.append(yamafuda.popleft())
            player1_cards.sort()
            player1_cards_str = ' '.join(map(str, player1_cards))

            yamafuda = ' '.join(map(str, yamafuda))

            # updating database
            with self.connection.cursor() as cursor:
                sql = 'insert into algo ' \
                      '(room_id, player0_id, player0_cards, player1_cards, player0_isOpen, player1_isOpen, yamafuda)' \
                      ' values (%s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(sql, (room_id, self.user_id, player0_cards_str, player1_cards_str, self.card_status,
                                     self.card_status, yamafuda))
                self.connection.commit()

            # f-command
            if f_command == 1:
                with self.connection.cursor() as cursor:
                    sql = 'update algo set player1_id="f" where room_id = {}'.format(room_id)
                    cursor.execute(sql)
                    self.connection.commit()

            if f_command == 2:
                with self.connection.cursor() as cursor:
                    sql = 'update algo set player1_id="{}" where room_id = {}'.format(friend_code, room_id)
                    cursor.execute(sql)
                    self.connection.commit()

            # return text
            text = self.player_text
            return {self.user_id: text}

        # join method
        elif "$join" in self.user_text and "algo" in self.user_text:
            # TODO: syntax check
            #       room existing check
            #       room full check
            #       first attack second attack
            #       draw the next

            # command syntax check
            try:
                command = self.user_text.split()
                room_id = command[2]
                if len(room_id) != 4:
                    raise RoomNumberError
            except IndexError:
                text = self.usage_text
                return {self.user_id: text}
            except RoomNumberError:
                text = self.usage_text
                return {self.user_id: text}

            # room search
            with self.connection.cursor() as cursor:
                sql = 'select * from algo where room_id = %s'
                cursor.execute(sql, int(room_id))
                results = cursor.fetchone()

            # room existing check
            if not results:
                text = 'Sorry, we can\'t find the room :('
                return {self.user_id: text}

            # room full check
            if results['player1_id'] is not None:
                if results['player1_id'] == 'f':
                    pass
                elif results['player1_id'] != str(self.user_id):
                    text = 'Sorry, the room is already full :('
                    return {self.user_id: text}
                else:
                    pass

            text = self.joined_text

            # first attack or second attack
            fa = random.randint(0, 1)

            # draw the next cards
            yamafuda = deque(map(int, results['yamafuda'].split()))
            next_hand = yamafuda.popleft()
            hand_insrtr = 'player{}_hand'.format(fa)

            # updating database
            with self.connection.cursor() as cursor:
                cursor.execute('update algo set player1_id="{}" where room_id={}'.format(self.user_id, int(room_id)))
                cursor.execute('update algo set attacker={} where room_id={}'.format(fa, int(room_id)))
                cursor.execute('update algo set {}={} where room_id={}'.format(hand_insrtr, next_hand, int(room_id)))
                self.connection.commit()

                # get newest information
                sql = 'select * from algo where room_id = %s'
                cursor.execute(sql, int(room_id))
                results = cursor.fetchone()

            # generating image
            ig = ImageGenerator(None, results['player0_cards'], results['player1_cards'], results['player0_isOpen'],
                                results['player1_isOpen'], attacker=fa, hand=next_hand)
            img_number = ig.main()
            img_title_0 = '{}.png'.format(img_number)
            img_title_1 = '{}.png'.format(img_number + 1)

            # return objects
            return {results['player1_id']: text, results['player0_id']: img_title_0, results['player1_id']: img_title_1}

        else:
            return {}

    def attack(self, now_user, results, cs):
        t = self.user_text.split()

        # -*-*- syntax check -*-*-
        attack_number, card_selector = None, None
        for i in t:
            try:
                tmp = int(i)
                if 0 <= tmp <= 11:
                    attack_number = tmp
                else:
                    raise AttackNumberError
            except ValueError:
                pass
            except AttackNumberError:
                pass

            try:
                if len(i) != 1:
                    raise AttackSelectorError
                elif re.fullmatch('[a-l]', i):
                    card_selector = i
                else:
                    raise AttackSelectorError
            except AttackSelectorError:
                pass

            if attack_number is not None and card_selector is not None:
                break

        if attack_number is None or card_selector is None:
            return {self.user_id: self.usage_text}

        # check the text sender is an attacker or not
        try:
            if int(results['attacker']) != now_user:
                raise IsNoAttackerError
        except IsNoAttackerError:
            return {self.user_id: self.invalid_text}

        # check the attack is succeeded or failed
        attacked_user_num = (now_user + 1) % 2  # 1 -> 0, 0 -> 1
        tmp = 'player{}_cards'.format(attacked_user_num)
        attacked_cards = list(map(int, results[tmp].split()))
        attacked_cards = list(reversed(attacked_cards))
        try:
            tgt = attacked_cards[cs[card_selector]]
        except IndexError:
            return {self.user_id: self.invalid_text}

        if tgt == attack_number * 2 or tgt == (attack_number * 2) + 1:

            # attack is done successfully!
            tmp = 'player{}_isOpen'.format(attacked_user_num)
            open_lst = list(map(int, results[tmp].split()))
            open_lst = list(reversed(open_lst))
            open_lst[cs[card_selector]] = 1
            open_lst = list(reversed(open_lst))
            yamafuda = deque(map(int, results['yamafuda'].split()))

            # draw the next card
            tmp = 'player{}_hand'.format(now_user)
            next_hand = results[tmp]
            if next_hand is None:  # next_hand is None?
                try:
                    next_hand = yamafuda.popleft()
                except IndexError:
                    next_hand = None

            # is now_user the winner?
            if (len(yamafuda) == 0 and next_hand is not None) or 0 not in open_lst:
                # now_user is the winner.
                # check winner and loser
                if now_user == 0:
                    winner = results['player0_id']
                    loser = results['player1_id']
                else:
                    winner = results['player1_id']
                    loser = results['player0_id']

                # database deleting
                with self.connection.cursor() as cursor:
                    cursor.execute('delete from algo where room_id={}'.format(int(results['room_id'])))
                    self.connection.commit()

                # return objects
                return {winner: '28.png', loser: '29.png'}

            # database update
            yamafuda = ' '.join(map(str, yamafuda))

            with self.connection.cursor() as cursor:
                # update player[01]_isOpen
                cursor.execute('UPDATE algo set {}="{}" where room_id={}'
                               .format(tmp, ' '.join(map(str, open_lst)), int(results['room_id'])))

                # update yamafuda
                cursor.execute('UPDATE algo set yamafuda="{}" where room_id={}'
                               .format(yamafuda, int(results['room_id'])))

                # update hand information
                cursor.execute('UPDATE algo set player{}_hand={} where room_id={}'
                               .format(now_user, next_hand, int(results['room_id'])))

                self.connection.commit()

                sql = 'select * from algo where room_id = %s'
                cursor.execute(sql, int(results['room_id']))
                results = cursor.fetchone()

            # image generation
            # TODO: use new information!
            ig = ImageGenerator(None, results['player0_cards'], results['player1_cards'], results['player0_isOpen'],
                                results['player1_isOpen'], attacker=now_user, hand=next_hand)
            img_number = ig.main()
            img_title_0 = '{}.png'.format(img_number)
            img_title_1 = '{}.png'.format(img_number + 1)

            # return objects
            return {results['player0_id']: img_title_0, results['player1_id']: img_title_1}

        else:
            # the attack failed.
            # TODO: hand -> player_card
            #       player_isOpen[player_card.index(hand)] -> 1
            #       attacker -> change
            #       draw the next card
            #       database update (player_card, player_isOpen, opp_hand, yamafuda, attacker)
            #       image generation

            # hand -> player_card
            tmp_cards = 'player{}_cards'.format(now_user)
            tmp_hand = 'player{}_hand'.format(now_user)
            hand_lst = list(map(int, results[tmp_cards].split()))
            hand_lst.append(results[tmp_hand])
            hand_lst.sort()

            # player_isOpen[player_card.index(hand)] -> 1
            tmp_opn = 'player{}_isOpen'.format(now_user)
            idx = hand_lst.index(results[tmp_hand])
            opn_lst = list(map(int, results[tmp_opn].split()))
            opn_lst.insert(idx, 1)

            # attacker changes
            atkr = (results['attacker'] + 1) % 2  # 0 -> 1, 1 -> 0

            # draw the next card
            yamafuda = deque(map(int, results['yamafuda'].split()))
            next_hand = yamafuda.popleft()

            # updating database
            with self.connection.cursor() as cursor:
                # player_card
                cursor.execute('update algo set {}="{}" where room_id={}'
                               .format(tmp_cards, ' '.join(map(str, hand_lst)), results['room_id']))

                # player_isOpen
                cursor.execute('update algo set {}="{}" where room_id={}'
                               .format(tmp_opn, ' '.join(map(str, opn_lst)), results['room_id']))
                
                # delete now_user's hand
                s = 'player{}_hand'.format(now_user)
                cursor.execute('update algo set {}=NULL where room_id={}'
                               .format(s, results['room_id']))

                # opponents hand
                s = 'player{}_hand'.format(atkr)
                cursor.execute('update algo set {}={} where room_id={}'
                               .format(s, next_hand, results['room_id']))

                # yamafuda
                cursor.execute('update algo set yamafuda="{}" where room_id={}'
                               .format(' '.join(map(str, yamafuda)), results['room_id']))

                # attacker
                cursor.execute('update algo set attacker={} where room_id={}'
                               .format(atkr, results['room_id']))

                self.connection.commit()

                cursor.execute('select * from algo where room_id={}'.format(results['room_id']))
                results = cursor.fetchone()

            # image generation
            ig = ImageGenerator(None, results['player0_cards'], results['player1_cards'], results['player0_isOpen'],
                                results['player1_isOpen'], attacker=atkr, hand=next_hand)
            img_number = ig.main()
            img_title_0 = '{}.png'.format(img_number)
            img_title_1 = '{}.png'.format(img_number + 1)

            # return objects
            return {results['player0_id']: img_title_0, results['player1_id']: img_title_1}

    def hide(self, now_user, results):
        # TODO: check a text sender is an attacker
        #       check hide without attack
        #       insert the hand into player_card
        #       insert 0 into player_isOpen
        #       attacker -> change
        #       draw the next card
        #       database updating (attacker, player_cards, player_isOpen, oppo_hand)
        #       generate image

        # check a text sender is an attacker
        try:
            if results['attacker'] != now_user:
                raise IsNoAttackerError
        except IsNoAttackerError:
            return {self.user_id: self.invalid_text}
        
        # check hide without attack
        s = 'player{}_hand'.format(now_user)
        hide_wo_atk_txt = 'Hmmm, you should attack at least once for each of your turn, but you did? I don\'t think so :-('
        if results[s] is None:
            return {self.user_id, hide_wo_atk_txt}

        # insert the hand into player_card
        tmp_cards = 'player{}_cards'.format(now_user)
        tmp_hand = 'player{}_hand'.format(now_user)
        hand_lst = list(map(int, results[tmp_cards].split()))
        hand_lst.append(results[tmp_hand])
        hand_lst.sort()

        # insert 0 into player_isOpen
        tmp_opn = 'player{}_isOpen'.format(now_user)
        idx = hand_lst.index(results[tmp_hand])
        opn_lst = list(map(int, results[tmp_opn].split()))
        opn_lst.insert(idx, 0)

        # attacker changes
        atkr = (results['attacker'] + 1) % 2

        # draw the next hand
        yamafuda = deque(map(int, results['yamafuda'].split()))
        next_hand = yamafuda.popleft()

        # database updating
        with self.connection.cursor() as cursor:
            # player_card
            cursor.execute('update algo set {}="{}" where room_id={}'
                           .format(tmp_cards, ' '.join(map(str, hand_lst)), results['room_id']))

            # player_isOpen
            cursor.execute('update algo set {}="{}" where room_id={}'
                           .format(tmp_opn, ' '.join(map(str, opn_lst)), results['room_id']))

            # delete now_user's hand
            s = 'player{}_hand'.format(now_user)
            cursor.execute('update algo set {}=NULL where room_id={}'
                           .format(s, results['room_id']))

            # opponents hand
            s = 'player{}_hand'.format(atkr)
            cursor.execute('update algo set {}={} where room_id={}'
                           .format(s, next_hand, results['room_id']))

            # yamafuda
            cursor.execute('update algo set yamafuda="{}" where room_id={}'
                           .format(' '.join(map(str, yamafuda)), results['room_id']))

            # attacker
            cursor.execute('update algo set attacker={} where room_id={}'
                           .format(atkr, results['room_id']))

            self.connection.commit()

            cursor.execute('select * from algo where room_id={}'.format(results['room_id']))
            results = cursor.fetchone()

        # image generation
        ig = ImageGenerator(None, results['player0_cards'], results['player1_cards'], results['player0_isOpen'],
                            results['player1_isOpen'], attacker=atkr, hand=next_hand)
        img_number = ig.main()
        img_title_0 = '{}.png'.format(img_number)
        img_title_1 = '{}.png'.format(img_number + 1)

        # return objects
        return {results['player0_id']: img_title_0, results['player1_id']: img_title_1}

    def interrupt(self, now_user, results):
        room_id = results['room_id']
        p0 = results['player0_id']
        p1 = results['player1_id']
        text = 'The game was interrupted by player {}.\n' \
               'If you want to play a game, create a room again. Thank you.'.format(now_user)

        # updating database
        with self.connection.cursor() as cursor:
            cursor.execute('delete from algo where room_id={}'.format(room_id))
            self.connection.commit()

        # return objects
        return {p0: text, p1: text}

    def gamer(self):
        """a player who is now playing the game"""
        # -*- init -*-
        cs = {chr(x + 97): x for x in range(12)}

        with self.connection.cursor() as cursor:
            sql = 'select * from algo where player0_id = %s'
            cursor.execute(sql, self.user_id)
            results = cursor.fetchone()
            now_user = 0
            if not results:
                sql = 'select * from algo where player1_id = %s'
                cursor.execute(sql, self.user_id)
                results = cursor.fetchone()
                now_user = 1

        if "$attack" in self.user_text:
            return self.attack(now_user=now_user, results=results, cs=cs)
        elif "$hide" in self.user_text:
            return self.hide(now_user=now_user, results=results)
        elif "$quit" in self.user_text:
            return self.interrupt(now_user=now_user, results=results)
        else:
            return {}

    def main(self):
        if '$help' in self.user_text:
            return {self.user_id: AlgoManager.help()}

        if '$mashiro' in self.user_text:
            img = '{}.png'.format(random.randint(100, 111))
            return {self.user_id: img}

        if '$lobby' in self.user_text:
            with self.connection.cursor() as cursor:
                sql = 'select * from algo where player1_id is null'
                cursor.execute(sql)
                lobby_lst = cursor.fetchall()

            # make lobby text
            text = 'Found {}.\n'.format(len(lobby_lst))
            text += '```| room_id |  host  |\n'
            for i in lobby_lst:
                text += '|  ' + str(i['room_id']) + '   | ' + i['player0_id'][0: 4] + '...|\n'
            text += '```'
            return {self.user_id: text}

        # check the text sender is playing the game or not
        with self.connection.cursor() as cursor:
            sql = 'select * from algo where player0_id = %s or player1_id = %s'
            cursor.execute(sql, (self.user_id, self.user_id))
            results = cursor.fetchall()

        if results:
            return self.gamer()
        else:
            return self.new_player()


if __name__ == '__main__':
    pass
