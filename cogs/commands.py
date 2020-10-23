# Standard libraries
import os
import json
import logging
import datetime

# Third party libraries
import discord
from pathlib import Path
import motor.motor_asyncio
from discord.ext import commands, tasks

import time
import platform
from discord.utils import get
from itertools import cycle
from pymongo import MongoClient

get_logid = "1"

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded\n-----")

    @commands.command()
    async def stats(self, ctx):
        """
        A usefull command that displays bot statistics.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.bot.version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developers:', value="<@376800503566172160>")

        embed.set_footer(text=f"{self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def echo(self, ctx, *, message=None):
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "Please provide the message to be repeated."
        await ctx.message.delete()
        await ctx.send(message)
    
    @commands.command()
    async def help(self, ctx, command = "help"):
        embed = discord.Embed(
        title="Help",
        color=discord.Color(0x136EB4))
        
        embed.add_field(name="Music", value="`play`, `skip`, `clear`")
        await ctx.send(embed=embed)

    
    """
        @commands.command()
        @commands.has_permissions(administrator=True)
        async def logchannel(ctx, logid):
            with open("logchannel.json", "r") as f:
                logids = json.load(f)

                logids[str(ctx.guild.id)] = logid

            with open("logchannel.json", "w") as f:
                 json.dump(logids, f, indent=4)
            embed = discord.Embed(
        title="Prefix changed to " + str(logid),
        color=discord.Color(0x006d76))
    
    channel = bot.get_channel(ID)
    await channel.send(embed=embed)
    await ctx.send(embed=embed)
    """

    #Kick member 
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed( 
        description=(f"{member.mention}"),
        timestamp=datetime.datetime.utcnow(), 
        color=discord.Color.orange())
        embed.set_author(name=f"{member} was kicked", icon_url='{}'.format(member.avatar_url))
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/764527084298567740/764647595346755654/kick-icon-15.png")
        channel = self.bot.get_channel(get_logid)
        await channel.send(embed=embed)

    #Ban member
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed( 
        description=(f"{member.mention}"), 
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.red())
        embed.set_author(name=f"{member} was kicked", icon_url='{}'.format(member.avatar_url))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/653240348490989594/764610704111435796/ban_hammer_1.png")
        channel = self.bot.get_channel(get_logid)
        await channel.send(embed=embed)

    #Unban member
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed( 
                description=(f"{user.mention}"),
                timestamp=datetime.datetime.utcnow(), 
                color=discord.Color.green())
                embed.set_author(name=f"{member} was kicked", icon_url='{}'.format(member.avatar_url))
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/764527084298567740/764648864091209738/6-64461_handcuffs-cuffs-arrest-open-handcuffs-clipart.png")
                channel = self.bot.get_channel(get_logid)
                await channel.send(embed=embed)
                return

    #Avatar
    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member=None): 
        if not member: 
            member = ctx.message.author 
        userAvatar = member.avatar_url
        embed = discord.Embed(
            color=discord.Color.dark_teal()
        )
        embed.set_author(name=f"{member}'s Avatar", icon_url='')
        embed.set_image(url='{}'.format(userAvatar))
        await ctx.send(embed=embed)

    #Clear
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(
            title=str(amount) + " messages cleared.",  
            color=discord.Color.purple())
        await ctx.send(embed=embed)
    
        time.sleep(4)
        await ctx.channel.purge(limit=1)
    
    #Clear error 
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
            title="Error", 
            description="Please specify the amount you want to clear", 
            color=discord.Color.red())
            await ctx.send(embed=embed)


def setup(commands):
    commands.add_cog(Commands(commands))
