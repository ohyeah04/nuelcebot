import discord
from discord.ext import tasks
import requests
from datetime import datetime
import os
import pytz

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

moodleurl = "http://moodle.nu.edu.kz/"
mynuurl = "http://my.nu.edu.kz/"
liburl = "http://library.nu.edu.kz/"
webworkurl = "http://webwork.sst.nu.edu.kz/webwork2"
regisrarurl = "http://registrar.nu.edu.kz/"
turnitinurl = "http://ev.turnitin.com/"

n = 0

bot = discord.Client()


@bot.event
async def on_ready():
    channel = bot.get_channel(int(765830945428471808))
    tmp = await channel.send('Cleaning...')
    await channel.purge()
    print('discord set up sucessfully')
    failed = await channel.send('History:')
    messageready = await channel.send('Now:')

    failedstatus = discord.Embed(title='Past Incidents:')
    failedstatus.set_footer(text='\nEnd of Past Incidents Report'.format(datetime.now(pytz.timezone('Asia/Almaty')).replace(microsecond=0, tzinfo=None)))
    await failed.edit(embed=failedstatus)

    embed = discord.Embed(title='Web resources Live status')
    embed.add_field(name='Moodle', value='loading...', inline=True)
    embed.add_field(name='MyNU', value='loading...', inline=True)
    embed.add_field(name='Registrar', value='loading...', inline=True)

    embed.add_field(name='WebWork ', value='loading...', inline=True)
    embed.add_field(name='Turnitin', value='loading...', inline=True)
    embed.add_field(name='Library', value='loading...', inline=True)

    embed.set_footer(text='\n✅ - Up\n❌ - Unavailable\nLast Update: not updated yet')

    await messageready.edit(embed=embed)

    await query.start(messageready, failedstatus, failed)


@tasks.loop(minutes=1.5, count=None)
async def query(messageready, failedstatus, failed):
    moodle = '✅' if await checkstatus(moodleurl, failedstatus, failed) else '❌'
    mynu = '✅' if await checkstatus(mynuurl,failedstatus, failed) else '❌'
    lib = '✅' if await checkstatus(liburl,failedstatus, failed) else '❌'
    webwork = '✅' if await checkstatus(webworkurl,failedstatus, failed) else '❌'
    registrar = '✅' if await checkstatus(regisrarurl,failedstatus, failed) else '❌'
    turnitin = '✅' if await checkstatus(turnitinurl,failedstatus, failed) else '❌'

    embed = discord.Embed(title='Web resources Live status')
    embed.add_field(name='Moodle', value=moodle, inline=True)
    embed.add_field(name='MyNU', value=mynu, inline=True)
    embed.add_field(name='Registrar', value=registrar, inline=True)

    embed.add_field(name='WebWork ', value=webwork, inline=True)
    embed.add_field(name='Turnitin', value=turnitin, inline=True)
    embed.add_field(name='Library', value=lib, inline=True)

    embed.set_footer(text='\n✅ - Up\n❌ - Unavailable\nLast Update: {}'.format(datetime.now(pytz.timezone('Asia/Almaty')).replace(microsecond=0, tzinfo=None)))

    await messageready.edit(embed=embed)


async def checkstatus(url,failedstatus, failed):
    try:
        requests.get(url, timeout=7)
        return True
    except:
        await offline(url, failedstatus, failed)
        return False


async def offline(url, failedstatus, failed):
    global n
    failedstatus.insert_field_at(index=n, name=url, value='❌ at {}'.format(datetime.now(pytz.timezone('Asia/Almaty')).replace(microsecond=0, tzinfo=None)), inline=False)
    n = n+1
    await failed.edit(embed=failedstatus)


#   await failed.edit(content='Past Incidents: \nDate {}\n{} - unavailable'.format(datetime.now(), url))


bot.run(TOKEN)