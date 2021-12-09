import discord
import asyncio, io
import config

import time
import requests
import os
import random

import anime_images_api

from random import randint
from config import *
from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
from itertools import cycle


client = commands.Bot(command_prefix = '.')
status = cycle(['Hololive', '.help'])
anime = anime_images_api.Anime_Images()



client.remove_command('help')
client.remove_command('add')
client.remove_command('sub')
client.remove_command('div')
client.remove_command('mul')

@client.event
async def on_ready():
    print('Kokichi is online!')
    
@tasks.loop(seconds = 120)
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))


@client.event
async def on_member_join(member):
     print(f"{member} has joined the server.")

@client.event
async def on_member_remove(member):
     print(f"{member} has left the server.")









#    FUN COMMANDS

@client.command()
async def ping(ctx):
    embed = discord.Embed(

        title = 'Ping',
        description = f"Pong! {round(client.latency)}ms.",
        color = discord.Color.random()

        )
    await ctx.send(embed = embed)



@client.command(aliases = ["8ball", '8b'])
async def _8ball(ctx, *, question):
        answers = [
            "Yes.",
            "Nah i don't know",
            "No.",
            "Nope",
            "Yea!",
            'Maybe...',
            "Not now, im busy...",
            "I love you",
            "I hate you dumbass",
            "Breh",
            "Lmao.",
            "I will not answer this question.",
            "Damn.",
            "Can you write more clearly?",
            "Hmm...",
            "My source code say 'Yes'!!",
            "My source code say 'No' :<",
            "Take it easy dude.",
            "No horny",
            "Calm",
            "Do you watch Hololive? If not, don't ask me.",
            "GAWR!",
            "I love Gura",
            "I love Ame",
            "Will you marry me?"


        ]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(answers)} ")


@client.command(aliases = ['cr'])
async def coolrate(ctx):
    embed = discord.Embed(title = 'Cool Rate', description = f"{ctx.author.mention} is {random.randrange(101)}% cool!", color = discord.Color.random())
    await ctx.send(embed = embed)











#      MATH COMMANDS

@client.command(aliases = ['sum'])
async def add(ctx, left : int, right : int):
    sum1 = left + right
    await ctx.send("The answer is: " + str(sum1))

@client.command(aliases = ['subtract'])
async def sub(ctx, left : int, right : int):
    sum2 = left - right
    await ctx.send("The answer is: " + str(sum2))

@client.command(aliases = ['multi'])
async def mul(ctx, left : int, right : int):
    sum3 = left * right
    await ctx.send("The answer is: " + str(sum3))

@client.command(aliases = ['division'])
async def div(ctx, left : int, right : int):
    sum4 = left / right
    await ctx.send("The answer is: " + str(sum4))









#    MODERATION
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit = amount)


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f"Kicked {member.mention}")


@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f"Banned {member.mention}")


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    
    for ban_entry in banned_users:
        user = ban_entry.user 

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send("Unbanned {user.mention}")











#   OTHERS COMMANDS

@client.command()
async def hentai(ctx):
    nsfw = anime.get_nsfw('hentai')
    embed = discord.Embed(
        title = "Hentai",
        description = "You are lewd.",
        color = discord.Color.random()
    )

    embed.set_footer(text = "Follow me on instagram by `@foxymisa1102`!")
    embed.set_image(url = nsfw)
    await ctx.send(embed = embed)



@client.command()
async def hug(ctx, *, member : discord.Member = None):


    sfw = anime.get_sfw('hug')
    embed = discord.Embed(title = "Hug Command", description = "Hugged you", color = discord.Color.random())
    embed.set_image(url = sfw)
    await ctx.send(embed = embed)














#    HELPS


@client.command()
async def help(ctx):
    helpEmbed = discord.Embed(title = "Help is on the way!", color = discord.Color.random())

    helpEmbed.add_field(name = "Fun", value = "`8ball`, `cool rate`, `ping`", inline = False)
    helpEmbed.add_field(name = "Math", value = "`sum`, `subtract`, `multi`, `division`", inline = False)
    helpEmbed.add_field(name = "Moderation", value = "`clear`, `kick`, `ban`, `unban`", inline = False)
    helpEmbed.add_field(name = "Utils", value = "`hug`, `hentai`", inline = False)
    await ctx.send(embed = helpEmbed)







client.run('ur token here') #put ur token inside the ''
