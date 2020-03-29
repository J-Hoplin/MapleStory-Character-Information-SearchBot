#This code and description is written by Hoplin
#This code is written with API version 1.0.0(Rewirte-V)
#No matter to use it as non-commercial.

import discord
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
import time

token = ''

client = discord.Client() # Create Instance of Client. This Client is discord server's connection to Discord Room
def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>','',str(htmls[a]),0).strip()
    return htmls

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Type !help or !도움말 for help"))
    print("New log in as {0.user}".format(client))

@client.event
async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)
    print(message.content)
    if message.author == client.user:
        return

    if message.content.startswith('!메이플'):

        # Maplestroy base link
        mapleLink = "https://maplestory.nexon.com"
        # Maplestory character search base link
        mapleCharacterSearch = "https://maplestory.nexon.com/Ranking/Union?c="

        playerNickname = ''.join((message.content).split(' ')[1:])
        html = urlopen(mapleCharacterSearch + quote(playerNickname))  # Use quote() to prevent ascii error
        bs = BeautifulSoup(html, 'html.parser')


        if len(message.content.split(" ")) == 1:
            embed = discord.Embed(title="닉네임이 입력되지 않았습니다", description="", color=0x5CD1E5)
            embed.add_field(name="Player nickname not entered",
                            value="To use command !메이플 : !메이플 (Nickname)", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Error : Incorrect command usage ", embed=embed)

        elif bs.find('tr', {'class': 'search_com_chk'}) == None:
            embed = discord.Embed(title="Nickname not exist", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 플레이어가 존재하지 않습니다.", value="플레이어 이름을 확인해주세요", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Error : Non existing Summoner ", embed=embed)

        else:
            # Get to the character info page
            characterRankingLink = bs.find('tr', {'class': 'search_com_chk'}).find('a', {'href': re.compile('\/Common\/Character\/Detail\/[A-Za-z0-9%?=]*')})['href']
            #Parse Union Level
            characterUnionRanking = bs.find('tr', {'class': 'search_com_chk'}).findAll('td')[2].text

            html = urlopen(mapleLink + characterRankingLink)
            bs = BeautifulSoup(html, 'html.parser')

            # Find Ranking page and parse page
            personalRankingPageURL = bs.find('a', {'href': re.compile('\/Common\/Character\/Detail\/[A-Za-z0-9%?=]*\/Ranking\?p\=[A-Za-z0-9%?=]*')})['href']
            html = urlopen(mapleLink + personalRankingPageURL)
            bs = BeautifulSoup(html, 'html.parser')
            #Popularity

            popularityInfo = bs.find('span',{'class' : 'pop_data'}).text.strip()
            ''' Can't Embed Character's image. Gonna fix it after patch note
            #Character image
            getCharacterImage = bs.find('img',{'src': re.compile('https\:\/\/avatar\.maplestory\.nexon\.com\/Character\/[A-Za-z0-9%?=/]*')})['src']
            '''
            infoList = []
            # All Ranking information embeded in <dd> elements
            RankingInformation = bs.findAll('dd')  # [level,job,servericon,servername,'-',comprehensiveRanking,'-',WorldRanking,'-',JobRanking,'-',Popularity Ranking,'-',Maple Union Ranking,'-',Achivement Ranking]
            for inf in RankingInformation:
                infoList.append(inf.text)
            embed = discord.Embed(title="Player " + playerNickname + "'s information search from nexon.com", description=infoList[0] + " | " +infoList[1] + " | " + "Server : " + infoList[2], color=0x5CD1E5)
            embed.add_field(name="Click on the link below to view more information.", value = mapleLink + personalRankingPageURL, inline=False)
            embed.add_field(name="Overall Ranking",value=infoList[4], inline=True)
            embed.add_field(name="World Ranking", value=infoList[6], inline=True)
            embed.add_field(name="Job Ranking", value=infoList[8], inline=True)
            embed.add_field(name="Popularity Ranking", value=infoList[10] + "( " +popularityInfo + " )", inline=True)
            embed.add_field(name="Maple Union", value=infoList[12] + "( LV." + characterUnionRanking + " )", inline=True)
            embed.add_field(name="Achivement Ranking", value=infoList[14], inline=True)
            embed.set_thumbnail(url='https://ssl.nx.com/s2/game/maplestory/renewal/common/logo.png')
            embed.set_footer(text='Service provided by Hoplin.',icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Player " + playerNickname +"'s information search", embed=embed)
client.run(token)
