import discord
import asyncio, io
import config
import json

import time
import requests
import os
import random
import queue
import threading
import sys

import anime_images_api



from random import randint, choice

from config import *


from datetime import datetime
from discord import Guild, Member, Embed
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
from itertools import cycle








client = commands.Bot(command_prefix = '.')

client.remove_command('help')
client.remove_command('add')
client.remove_command('sub')
client.remove_command('div')
client.remove_command('mul')

status = cycle(['Hololive', '.help', 'VALORANT'])
anime = anime_images_api.Anime_Images()











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



@client.command()
async def userinfo(ctx, member : discord.Member):

    roles = [role for role in member.roles]

    roles = []
    for role in member.roles:
        roles.append(role)


    embed = discord.Embed(color = discord.Color.random(), timestamp = ctx.message.created_at)

    embed.set_author(name = f"User Info - {member}")

    embed.set_thumbnail(url = member.avatar_url)

    embed.add_field(name = "ID:", value = member.id)

    embed.add_field(name = "Guild name:", value = member.display_name)

    embed.add_field(name = "Created at:", value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name = "Joined at:", value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name = f"Roles ({len(roles)})", value = " ".join([role.mention for role in roles]))

    embed.add_field(name = "Top role:", value = member.top_role.mention)

    embed.add_field(name = "Bot?", value = member.bot)

    await ctx.send(embed = embed)



@client.command(pass_context = True)
@commands.has_permissions(manage_roles = True)
async def create_mute_role(guild : Guild):
    role_name = "muted"

    mute_role = get(guild.roles, name = role_name)

    if mute_role is None:
        await guild.create_role(name = role_name)

        mute_role = get(guild.roles, name = role_name)

    for channel in guild.text_channels:
        await asyncio.sleep(0)


        mute_permissions = discord.PermissionOverwrite()
        mute_permissions.send_messages = False

        await channel.set_permissions(mute_role, overwrite = mute_permissions)

    return (mute_role)


@client.command(pass_context=True)
@commands.has_permissions(manage_roles = True)
async def mute(ctx, member: discord.Member):
    guild = ctx.message.guild
    mute_role = await create_mute_role(guild)
    await member.add_roles(mute_role)

    await ctx.send(f"{member.name} has been muted !")
    return




@client.command()
@commands.has_permissions(administrator=True)
async def activity(ctx, *, activity):
    await client.change_presence(activity=discord.Game(name=activity))
    await ctx.send(f"Bot's activity changed to {activity}")




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

# @client.command()
# async def hug(ctx):
#     sfw = anime.get_sfw('hug')
#     await ctx.send(sfw)

@client.command()
async def hug(ctx, *, member : discord.Member = None):


    sfw = anime.get_sfw('hug')
    embed = discord.Embed(title = "Hug Command", description = "Hugged you", color = discord.Color.random())
    embed.set_image(url = sfw)
    await ctx.send(embed = embed)



async def get_photo():
    res = requests.get("https://cultured.skellymclane386.repl.co/photo/random")
    return res.json()

@client.command()
async def vtuber(ctx : commands.Context):
    _id, url = await get_photo()

    embed = discord.Embed(
        title = f"Vtuber: {_id}",
        color = discord.Color.random(),
        url = url
        )
    embed.set_image(url = url)
    embed.set_footer(text = "follow me on Instagram by `@foxymisa1102`!")

    await ctx.send(embed = embed)

@client.command()
async def source(ctx):
    embed = discord.Embed(title = "My source code !", description = "https://github.com/Just-Misaa/Kokichi", color = discord.Color.random())
    embed.set_footer(text = "follow me on Instagram by `@foxymisa1102")
    await ctx.send(embed = embed)

@client.command()
async def invite(ctx):
    embed = discord.Embed(title = "Invite me to your server!!!", description = "https://discord.com/api/oauth2/authorize?client_id=915419050358763540&permissions=8&scope=bot", color = discord.Color.random())
    embed.set_footer(text = "follow me on Instagram by `@foxymisa1102`")

    await ctx.send(embed = embed)


#    HELPS


@client.command()
async def help(ctx):
    helpEmbed = discord.Embed(title = "Help is on the way!", color = discord.Color.random())

    helpEmbed.add_field(name = "Fun", value = "`8ball`, `cool rate`, `ping`", inline = False)
    helpEmbed.add_field(name = "Math", value = "`sum`, `subtract`, `multi`, `division`", inline = False)
    helpEmbed.add_field(name = "Moderation", value = "`clear`, `kick`, `ban`, `unban`, `userinfo`, `activity`, `mute`", inline = False)
    helpEmbed.add_field(name = "Utils", value = "`hug`, `hentai`, `vtuber`, `source`, `invite`", inline = False)
    await ctx.send(embed = helpEmbed)







client.run('ur token here') #put ur token inside the ''
