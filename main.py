import nextcord
from nextcord import Interaction
import os
from datetime import timedelta
import json
import aiohttp
import io
import re

messagesREACT = []
idS = nextcord.SlashOption(name='id',
                           description='The Id of the person you want to mute.',
                           required=True)

ore = nextcord.SlashOption(name='ore',
                           description='For how many hours?. (a day = 24 hours)',
                           required=True)

why = nextcord.SlashOption(name='why',
                           description='Why do you want to mute them?',
                           required=True)

st = nextcord.SlashOption(name='cuss',
                          description='Add a swear.',
                          required=True)

intents = nextcord.Intents.all()
client = nextcord.Client(intents=intents)


@client.event
async def on_ready():
    print(client.user)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    for i in message.guild.members:
        if i.id == 700811761972150374:
            if i.status != nextcord.Status.idle:
                #nitro
                try:
                    emojis = {}
                    for e in client.emojis:
                        if e.animated:
                            emojis[':' + e.name + ':'] = str(e)
                    if message.content.lower() == 'nitro.l':
                        embedVar = nextcord.Embed(title='nitro reactions:',
                                                  description=''.join([
                                                      '`' + i + '` : ' +
                                                      f'{emojis[i]}\n'
                                                      for i in emojis.keys()
                                                  ]),
                                                  color=0xff000)
                        await message.channel.send(embed=embedVar)
                    content = message.content
                    x = 0
                    for i in emojis.keys():
                        if i in content:
                            content = content.replace(i, emojis[i])
                            x += 1
                    if x != 0:
                        wbs = await message.channel.webhooks()
                        wb = []
                        for i in wbs:
                            if i.user.name == client.user.name:
                                wb.append(i)
                        if wb == []:
                            webhook = await message.channel.create_webhook(
                                name='nitro')
                        else:
                            webhook = wb[0]
                        urls = [
                            attachment.url
                            for attachment in message.attachments
                        ]
                        files = []
                        if len(urls) != 0:
                            for url in urls:
                                async with aiohttp.ClientSession() as session:
                                    async with session.get(url) as resp:
                                        data = io.BytesIO(await resp.read())
                                        files.append(
                                            nextcord.File(data, 'image.png'))
                        username = message.author.nick
                        if username == None:
                            username = message.author.name
                        if message.reference != None:
                            foo = await message.channel.fetch_message(
                                message.reference.message_id)
                            await webhook.send(
                                '> ' + str(foo.content) +
                                f" ||<@{foo.author.id}>||",
                                username=username,
                                avatar_url=message.author.avatar.url,
                                files=files)
                        await webhook.send(
                            str(content),
                            username=username,
                            avatar_url=message.author.avatar.url,
                            files=files)
                        await message.delete()
                except Exception as x:
                    print(x)

    #lower check was: if i in db['prostii'] and (True in [(("[9] " in (g.nick if g.nick != None else "")) if g != message.author else False) for g in message.guild.members]) and message.guild.id in (828357556975960124, 934870083589775470):
    try:
    	with open('db', 'r') as f:
    		db = json.loads(f.read())
        msg = re.sub("\|\|.+\|\|", "", message.content.lower())
        for i in msg.split():
            if i in db['cuss']:
                if "[9] " in message.author.display_name:
                    try:
                        await message.author.edit(
                            nick=message.author.display_name.replace(
                                "[9] ", ""))
                    except Exception as x:
                        await message.channel.send(x)
                if True in [
                    ("[9] " in g.display_name) for g in message.guild.members
                ] and message.guild.id in (828357556975960124,
                                           934870083589775470):
                    await message.delete()
                    await message.author.timeout(
                        timedelta(hours=1),
                        reason=
                        f'Said `{message.content.replace(i, f"///{i}///")}`.'
                    )
                    await message.channel.send(
                        f'<@{message.author.id}> was muted for a hour.'
                    )
                    return
    except:
        pass


@client.slash_command(
    name='mute',
    description='Mute someone. (Only for owners)',
    force_global=True)
async def mute(interaction: Interaction,
               id: str = idS,
               timp: str = ore,
               why: str = why):

    if interaction.permissions.administrator or interaction.user.id == 542741572169629704:
        try:
            member = await interaction.guild.fetch_member(id)
            await member.timeout(timedelta(hours=int(timp)), reason=why)
            await interaction.send(
                f'<@{id}> was muted for `{timp}` hours.\nReason: `{why}`',
                ephemeral=False)
        except:
            await interaction.send(
                'Error, maybe because of incorrect ID.',
                ephemeral=True)
    else:
        await interaction.send('You don\'t have the permission to use this.',
                               ephemeral=True)


@client.slash_command(name='unmute',
                      description='remove the mute',
                      force_global=True)
async def unmute(interaction: Interaction, id: str = idS):
    if interaction.permissions.administrator or interaction.user.id == 542741572169629704:  #interaction.user == interaction.guild.owner
        try:
            member = await interaction.guild.fetch_member(id)
            await member.timeout(None)
            await interaction.send(f'Removed the timeout for the user <@{id}>.',
                                   ephemeral=False)
        except:
            await interaction.send(
                'Error, maybe because of incorrect ID.',
                ephemeral=True)
    else:
        await interaction.send('You don\'t have the permission to use this.',
                               ephemeral=True)


@client.slash_command(name='addcuss',
                      description='add new words',
                      force_global=True)
async def addcuss(interaction: Interaction, cuss: str = st):
    try:
        if interaction.user.id in [542741572169629704, 758350007476289587]:
            cuss = cuss.lower()
            with open('db', 'r') as f:
    			db = json.loads(f.read())
            if len(cuss.split()) == 1:
                if not cuss in db['cuss']:
                    db['cuss'].append(cuss)
                    with open('db', 'w') as f:
    					f.write(json.dumps(db))
                    await interaction.send(
                        f'Done, `{cuss}` was added to the list.',
                        ephemeral=True)
                else:
                    await interaction.send(f'`{cuss}` is already in the list.',
                                           ephemeral=True)
            else:
                await interaction.send(f'Only one word accepted.',
                                       ephemeral=True)
        else:
            await interaction.send('You cannot use this.', ephemeral=True)
    except:
        await interaction.send('ERROR.', ephemeral=True)


@client.slash_command(name='recuss',
                      description='Remove a word from the dictionary.',
                      force_global=True)
async def recuss(interaction: Interaction, cuss: str = st):
    try:
        if interaction.user.id in [542741572169629704, 758350007476289587]:
            cuss = cuss.lower()
            with open('db', 'r') as f:
    			db = json.loads(f.read())
            if len(cuss.split()) == 1:
                if cuss in db['cuss']:
                    db['cuss'].remove(cuss)
                    with open('db', 'w') as f:
    					f.write(json.dumps(db))
                    await interaction.send(
                        f'Done, `{cuss}` was removed from the list.',
                        ephemeral=True)
                else:
                    await interaction.send(f'`{cuss}` isn\'t in the list.',
                                           ephemeral=True)
            else:
                await interaction.send(f'Only one word accepted.',
                                       ephemeral=True)
        else:
            await interaction.send('You cannot use this.', ephemeral=True)
    except:
        await interaction.send('ERROR.', ephemeral=True)


#nitro
@client.event
async def on_raw_reaction_add(reaction):
    if [reaction.channel_id, reaction.message_id,
            str(reaction.emoji)
        ] in messagesREACT and reaction.user_id != client.user.id:
        channel = await client.fetch_channel(reaction.channel_id)
        msg = await channel.fetch_message(reaction.message_id)
        await msg.remove_reaction(str(reaction.emoji), client.user)
        del messagesREACT[messagesREACT.index(
            [reaction.channel_id, reaction.message_id,
             str(reaction.emoji)])]


@client.slash_command(name='react',
                      description='React with an animated emoji!',
                      force_global=True)
async def slash(
    interaction: Interaction,
    Emoji: str = nextcord.SlashOption(
        name='emj',
        description=f'Emoji you want to react with.\n',
        required=True,
        choices=[
            e.name for e in filter(lambda emoji: emoji.animated, client.emojis)
        ]),
    MessageID: str = nextcord.SlashOption(
        name='msg',
        description='Enter ID of message you want to react.',
        required=False)):
    try:
        emojis = {}
        for e in client.emojis:
            if e.animated:
                emojis[e.name] = str(e)
        if MessageID == None:
            history = await interaction.channel.history(limit=1).flatten()
            msg = history[0]
            del history
        else:
            msg = await interaction.channel.fetch_message(MessageID)
        if not emojis[Emoji] in [str(i.emoji) for i in msg.reactions]:
            await msg.add_reaction(emojis[Emoji])
            messagesREACT.append([msg.channel.id, msg.id, emojis[Emoji]])
    except:
        pass
    await interaction.send(f'...', delete_after=0)


TOKEN = os.environ.get("TOKEN")
client.run(TOKEN)
