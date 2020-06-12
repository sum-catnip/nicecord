import sys
import heapq

import discord
from tinydb import TinyDB, Query

try: token = sys.argv[1]
except IndexError:
    print('usage: python3 nicecord.py <token>')

client = discord.Client()
db = TinyDB('db.json')


async def embed_addusr(embed, uid, count, inline=True):
    name = (await client.fetch_user(uid)).name
    embed.add_field(name=name, value=f'{count} nices', inline=inline)


async def nice(userid: int, channel: discord.TextChannel):
    user = db.get(Query().userid == userid)
    if user: count = user['count']
    else: count = 0
    count += 1
    db.upsert({'userid': userid, 'count': count}, Query().userid == userid)

    top = heapq.nlargest(3, db, lambda x: x['count'])

    embed=discord.Embed(title='𝓷𝓲𝓬𝓮 ☜(ﾟヮﾟ☜)', description='Nice Leaderboard')
    for t in top: await embed_addusr(embed, t['userid'], t['count'])
    await embed_addusr(embed, userid, count, False)
    await channel.send(embed=embed)


@client.event
async def on_ready():
    print('nicecord online :pepeok:')


@client.event
async def on_message(msg: discord.Message):
    if not msg.author.bot and msg.content == 'nice':
        uid = msg.author.id
        await nice(uid, msg.channel)


client.run(token)
