"""
      ___           ___           ___           ___                         ___           ___     
     /\  \         /\__\         /\  \         /\__\                       /\  \         /\  \    
     \:\  \       /:/ _/_        \:\  \       /:/ _/_         ___         /::\  \        \:\  \   
      \:\  \     /:/ /\__\        \:\  \     /:/ /\  \       /\__\       /:/\:\  \        \:\  \  
  _____\:\  \   /:/ /:/ _/_   ___  \:\  \   /:/ /::\  \     /:/  /      /:/  \:\  \   _____\:\  \ 
 /::::::::\__\ /:/_/:/ /\__\ /\  \  \:\__\ /:/_/:/\:\__\   /:/__/      /:/__/ \:\__\ /::::::::\__\
 \:\~~\~~\/__/ \:\/:/ /:/  / \:\  \ /:/  / \:\/:/ /:/  /  /::\  \      \:\  \ /:/  / \:\~~\~~\/__/
  \:\  \        \::/_/:/  /   \:\  /:/  /   \::/ /:/  /  /:/\:\  \      \:\  /:/  /   \:\  \      
   \:\  \        \:\/:/  /     \:\/:/  /     \/_/:/  /   \/__\:\  \      \:\/:/  /     \:\  \     
    \:\__\        \::/  /       \::/  /        /:/  /         \:\__\      \::/  /       \:\__\    
     \/__/         \/__/         \/__/         \/__/           \/__/       \/__/         \/__/    




Project Neuston

developed by E.G.B, script by 대표 

August 2023


"""
# other file imports

from shrine import *
from enums import *
from discord_auth import *
from discord.ext import commands
from place import *
from threads import *
from instance import *
from helper import *
from image import *


import google_sheets as gs
import owner_loader as ol
import formatter as frmat
import discord
import time
import random

places = {}
characters = {}
owners = {}
bulletin_board = {}

instances = {'S1': None, 'S2': None, 'S3': None}

debugging = True

@bot.event
async def on_ready():
    global places, characters, owners
    global debugging
    global restore_timer
    global bulletin_board

    print("starting time measuring thread...")
    restore_timer.start()

    # init places - hq(0), dawn(1)
    print("loading places ...")
    hq_desc = gs.get(Sheet.HQ.value, "D1:D2")
    hq_arrival = gs.get_single(Sheet.HQ.value, "D4")
    hq = Place("HQ", hq_desc[0][0], hq_desc[1][0], hq_arrival)
    hq.kor_acr = "본부"
    places["HQ"] = hq

    dawn_desc = gs.get(Sheet.DAWN.value, "D1:D2")       # official name and desc
    dawn_arrival = gs.get_single(Sheet.DAWN.value, "D4")
    dawn =  Place("DAWN", dawn_desc[0][0], dawn_desc[1][0], dawn_arrival)   # auto loads the search thing 
    dawn.kor_acr = "새벽녘마을"
    places["DAWN"] = dawn
    print("loading places complete")

    # init owners and characters
    print("loading owners / characters ...")
    unpack = ol.get_owners()
    characters = unpack[0]
    owners = unpack[1]

    for n, ch in characters.items():
        if ch.place == Dest.DAWN.value:
            ch.place = places["DAWN"]
            print(str(ch.name) + " is in dawn")
        elif ch.place == Dest.HQ.value:
            ch.place = places["HQ"]
            print(str(ch.name) + " is in hq ")
    for o, ow in owners.items():
        if ow.main != None:
            ow.main = ow.character_list[ow.main]

    print("loading owners / characters complete")

    print("setting up instances...")
    instances['S1'] = Instance('S1')
    instances['S2'] = Instance('S2')
    instances['S3'] = Instance('S3')
    print("setting up instances complete")

    print("setting up bulletin board...")
    bulletin_board = init_bulletin()

    print(f'{bot.user.name} -- Finished loading everything!')

# ========================================================================= helper functions

def channelChecker(ctx):
    inst = owners[str(ctx.author)].main.instance
    place = owners[str(ctx.author)].main.place
    channel = str(ctx.channel)
    # wrote in hq and is in hq, instance none
    if( ("본부" in channel and (inst == None and place.acr == "HQ")) or\
        # wrote in instance and you are in that instance
        (inst != None and (inst.ID == Channel(channel).name or inst.ID == M_Channel(channel).name)) or\
        # wrote in personal and is not in hq
        ("개인조사" in channel and (inst == None or place.acr != "HQ")) ):
        return True
    return False

# ========================================================================= channel commands

@bot.command(aliases=["오프", '끄기'])
async def quit(ctx, *arg):
    exit_event.set()
    restore_timer.join()
    await bot.close()

@bot.command(aliases=["사용법", '사용서', '사용', '커맨드'])
async def info(ctx):
    await ctx.author.send(SystemMessage.INFO.value)

@bot.command(aliases=['메인', '멘', '캐릭터'])
async def set_main(ctx, ch_name):
    await ctx.reply(owners[str(ctx.author)].set_main(ch_name))

@bot.command(name="나")
async def self_info(ctx):
    if owners[str(ctx.author)].main == None:
        await ctx.reply(f"*{SystemMessage.DENY.value}*\n*먼저 메인 캐릭터를 설정하자.*")
        return
    if(not channelChecker(ctx)):
       await ctx.reply(SystemMessage.WRONGCHANNEL.value)
       return

    await ctx.reply(frmat.character_formatter(owners[str(ctx.author)].main))

@bot.command(name="위치")
async def self_place_info(ctx):
    if owners[str(ctx.author)].main == None:
        await ctx.reply(f"*{SystemMessage.DENY.value}*\n*먼저 메인 캐릭터를 설정하자.*")
        return
    if(not channelChecker(ctx)):
       await ctx.reply(SystemMessage.WRONGCHANNEL.value)
       return
    
    await ctx.reply(frmat.character_formatter(owners[str(ctx.author)].main.place))

@bot.command(name="이동")
async def move(ctx, acr):
    if owners[str(ctx.author)].main == None:
        await ctx.reply(f"*{SystemMessage.DENY.value}*\n*먼저 메인 캐릭터를 설정하자.*")
        return
    if(not channelChecker(ctx)):
       await ctx.reply(SystemMessage.WRONGCHANNEL.value)
       return
    # find place by places[Dest(acr).name]
    # checks first
    place = None
    try:
        place = places[Dest(acr).name]
    except ValueError:
        await ctx.reply(f"*{SystemMessage.DENY.value}*")
        return

    character = owners[str(ctx.author)].main
    ret = character.move_places(place)

    # if trying to move in an instance
    if(character.instance != None):
        # moving worked
        if "SYS" in ret:
            # leaving instance to go to HQ
            if place.acr == "HQ":
                character.instance.remove(character)
                character.instance = None
                if "mock" in str(ctx.channel):
                    channel = discord.utils.get(ctx.guild.channels, name="mock-본부")
                    await channel.send(f"{ctx.author.mention}\n{ret}")
                else:
                    channel = discord.utils.get(ctx.guild.channels, name="본부")
                    await channel.send(f"{ctx.author.mention}\n{ret}")
            # move as a team to go somewhere else
            else:
                await ctx.reply(character.instance.move(character, place))

        elif "ERROR" in ret:
            await ctx.reply(f"{ret}")

    # if trying to move by oneself
    else:
        #moving worked
        if "SYS" in ret:
            #going to HQ -- mention in hq channel
            if place.acr == "HQ":
                if "mock" in str(ctx.channel):
                    channel = discord.utils.get(ctx.guild.channels, name="mock-본부")
                    await channel.send(f"{ctx.author.mention}\n{ret}")
                else:
                    channel = discord.utils.get(ctx.guild.channels, name="본부")
                    await channel.send(f"{ctx.author.mention}\n{ret}")
            #going somewhere else -- mention in channel 4
            else:
                if "mock" in str(ctx.channel):
                    channel = discord.utils.get(ctx.guild.channels, name="mock-개인조사4")
                    await channel.send(f"{ctx.author.mention}\n{ret}")
                else:
                    channel = discord.utils.get(ctx.guild.channels, name="개인조사-4")
                    await channel.send(f"{ctx.author.mention}\n{ret}")

        elif "ERROR" in ret:
            await ctx.reply(f"{ret}")


# incomplete
@bot.command(aliases=["참여", '가입', '참가', '참', '합류'])
async def join(ctx, server):
    if owners[str(ctx.author)].main == None:
        await ctx.reply(f"*{SystemMessage.DENY.value}*\n*먼저 메인 캐릭터를 설정하자.*")
        return
    if(not channelChecker(ctx)):
       await ctx.reply(SystemMessage.WRONGCHANNEL.value)
       return

   # instance.add(character), then character.instance = instance
    channel_name = ""
    character = owners[str(ctx.author)].main

   # figure out which channel to be joining
    if "mock" in str(ctx.channel):
        try:
            channel_name = M_Channel(server).name
        except ValueError:
            await ctx.reply("*{SystemMessage.WRONGFORM.value}*")
            return
    else:
        try:
            channel_name = Channel(server).name
        except ValueError:
            await ctx.reply("*{SystemMessage.WRONGFORM.value}*")
            return

    instance = instances[channel_name]
    instance.add(character)
    character.instance = instance
    channel = discord.utils.get(ctx.guild.channels, name=server)
    await channel.send(f"{ctx.author.mention}\n*[SYS] {character.name}(이)가 [{server}]에 합류한다.*")



# incomplete
@bot.command(alias=["탈퇴", '탈'])
async def exitt(ctx, server):
    if owners[str(ctx.author)].main == None:
        await ctx.reply(f"*{SystemMessage.DENY.value}*\n*먼저 메인 캐릭터를 설정하자.*")
        return
    if(not channelChecker(ctx)):
       await ctx.reply(SystemMessage.WRONGCHANNEL.value)
       return

# incomplete
@bot.command(name="탐색")
async def search(ctx, *args):
    if owners[str(ctx.author)].main == None:
        await ctx.reply(f"*{SystemMessage.DENY.value}*\n*먼저 메인 캐릭터를 설정하자.*")
        return
    if(not channelChecker(ctx)):
       await ctx.reply(SystemMessage.WRONGCHANNEL.value)
       return

    owner = owners[str(ctx.author)]
    character = owner.main

    # free search within instance
    if len(args) == 0 and not curr_instance == None:
        pass
    # free search by self (either hq or else)
    elif len(args) == 0:
        pass
    # talking to NPC/interacting with item within instance
    elif not curr_instance == None:
        pass
    # talking to NPC/interacting with item (either hq or else)
    else:
        pass


bot.run(TOKEN)
