# -*- coding: utf-8 -*-
# !/usr/bin/env python3
# #########################################################################
#
# 2020/04/19
# written by: Apoi
# version: 0.1.0
#
# #########################################################################
#
# PROJECT:
# * Algo Dealer
#
# FILE PURPOSE:
# * communicate information between discord and this project
#
# FILE ISSUE
#
# #########################################################################


# #########################################################################
# library importing
# #########################################################################
import discord
import os

# #########################################################################
# python file importing
# #########################################################################
from manage import AlgoManager

# #########################################################################
# TOKEN
# #########################################################################
TOKEN = os.environ['discord_token']

# #########################################################################
# make an object which needs to communicate with discord
# #########################################################################
client = discord.Client()

# #########################################################################
# class
# #########################################################################


class Front:
    def __init__(self, client):
        self.client = client

    async def main(self, discord_event):
        get_text = discord_event.content
        channel_id = discord_event.channel.id
        user_id = discord_event.author.id

        # check {$command} or not
        if get_text:
            if get_text[0] == '$':
                obj = AlgoManager(user_id=user_id, user_text=get_text).main()
                for i in obj.items():
                    if i[0] is None:
                        continue
                    tmp = i[1]
                    if 'png' in tmp:
                        # sending photo
                        s = "generated_img/{}".format(i[1])
                        user = client.get_user(int(i[0]))
                        await user.send(file=discord.File(s))
                    else:
                        # sending text
                        try:
                            user = client.get_user(int(i[0]))
                            await user.send(i[1])
                        except AttributeError:
                            pass


# #########################################################################
# instance
# #########################################################################
discord_bot = Front(client)


# #########################################################################
# process when the client start-up
# #########################################################################
@client.event
async def on_ready():
    print('Login')
    user = client.get_channel(XXXXXXXXXXXXXXXXXX)  # <- 18-digits integer
    await user.send("Got it, The server started successfully!")


# #########################################################################
# process when the bot get a message
# #########################################################################
@client.event
async def on_message(message):
    if message.author.bot:
        return

    await discord_bot.main(message)

# #########################################################################
# bot start-up and connection to a discord server
# #########################################################################
client.run(TOKEN)
