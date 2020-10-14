import discord
from discord.ext import tasks
import requests
from datetime import datetime
import os

TOKEN = os.getenv("h")

url = 'http://moodle.nu.edu.kz'
url2 = 'http://asddasadhdas.com'
n = 0

bot = discord.Client()


@bot.event
async def on_ready():
    channel = bot.get_channel(int(764473005568294923))
    tmp = await channel.send('Cleaning...')
    await channel.purge()
    print('discord set up sucessfully')
    failed = await channel.send('Past Incidents:')
    messageready = await channel.send('Currently:')

    failedstatus = discord.Embed(title='Past Incidents:')
    failedstatus.set_footer(text='\nEnd of Past Incidents Report'.format(datetime.now()))
    await failed.edit(embed=failedstatus)

    embed = discord.Embed(title='Web resources Live status')
    embed.add_field(name='Moodle', value='loading...', inline=True)
    embed.add_field(name='MyNU', value='loading...', inline=True)
    embed.add_field(name='Registrar', value='loading...', inline=True)

    embed.add_field(name='WebWork ', value='loading...', inline=True)
    embed.add_field(name='Turnitin', value='loading...', inline=True)
    embed.add_field(name='Library', value='loading...', inline=True)

    embed.set_footer(text='\n✅ - Running\n❌ - Unavailable\nLast Update: not updated yet')

    await messageready.edit(embed=embed)

    await query.start(messageready, failedstatus, failed)


@tasks.loop(minutes=1.0, count=None)
async def query(messageready, failedstatus, failed):
    moodle = '✅' if await checkstatus(url, failedstatus, failed) else '❌'
    mynu = '✅' if await checkstatus(url,failedstatus, failed) else '❌'
    lib = '✅' if await checkstatus(url2,failedstatus, failed) else '❌'
    webwork = '✅' if await checkstatus(url2,failedstatus, failed) else '❌'
    registrar = '✅' if await checkstatus(url,failedstatus, failed) else '❌'
    turnitin = '✅' if await checkstatus(url,failedstatus, failed) else '❌'

    embed = discord.Embed(title='Web resources Live status')
    embed.add_field(name='Moodle', value=moodle, inline=True)
    embed.add_field(name='MyNU', value=mynu, inline=True)
    embed.add_field(name='Registrar', value=registrar, inline=True)

    embed.add_field(name='WebWork ', value=webwork, inline=True)
    embed.add_field(name='Turnitin', value=turnitin, inline=True)
    embed.add_field(name='Library', value=lib, inline=True)

    embed.set_footer(text='\n✅ - Running\n❌ - Unavailable\nLast Update: {}'.format(datetime.now()))

    await messageready.edit(embed=embed)


async def checkstatus(url,failedstatus, failed):
    try:
        requests.get(url, timeout=10)
        return True
    except:
        await offline(url, failedstatus, failed)
        return False


async def offline(url, failedstatus, failed):
    global n
    failedstatus.insert_field_at(index=n, name=url, value='❌ at {}'.format(datetime.now()), inline=False)
    n = n+1
    await failed.edit(embed=failedstatus)


#   await failed.edit(content='Past Incidents: \nDate {}\n{} - unavailable'.format(datetime.now(), url))


bot.run(TOKEN)