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
# * to notice algo game error
#
# FILE ISSUE
#
# #########################################################################


# #########################################################################
# library importing
# #########################################################################


# #########################################################################
# class
# #########################################################################
class RoomNumberError(Exception):
    """
    error about room number
    * guide: room number must be 4 digits number.
    """
    pass


class AttackNumberError(Exception):
    """
    attack number must be 0 <= n <= 11
    """
    pass


class AttackSelectorError(Exception):
    """
    attack selector is out of [a-l]
    """
    pass


class IsNoAttackerError(Exception):
    """
    the text sender is not an attacker now.
    """
    pass
