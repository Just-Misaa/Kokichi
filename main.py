import discord
import asyncio
import os
import random


from discord.ext import commands, tasks
from itertools import cycle


client = commands.Bot(command_prefix = '.')
status = cycle(['Hololive', '.help'])
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
          'Yes',
          'No',
          "I don't know...",
          #You can just add more the answer that you want to make the bot do a random and pick it up by the syntax below
          #"the answer here",
          #and remember that THE LAST ANSWERS in this dict do not have the ','
          
          #example
          #"this is the last answer"


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



#    HELPS
#i am a newbie to discord.py, so i dont know how to make auto collect commands, so you just need to ADD commands by YOURSELF

@client.command()
async def help(ctx):
    helpEmbed = discord.Embed(title = "Help is on the way!", color = discord.Color.random())

    helpEmbed.add_field(name = "Fun", value = "`8ball`, `cool rate`, `ping`", inline = False)
    helpEmbed.add_field(name = "Math", value = "`sum`, `subtract`, `multi`, `division`", inline = False)
    helpEmbed.add_field(name = "Moderation", value = "`clear`, `kick`, `ban`, `unban`", inline = False)

    await ctx.send(embed = helpEmbed)






client.run('ur token here') #put ur token inside the ''
