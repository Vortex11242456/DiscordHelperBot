import discord
from random import randint, choice
from discord.ext import commands
import datetime, pyowm
import speech_recognition as sr
from discord.utils import get
import youtube_dl
import config 
import os
from time import sleep
import requests
from PIL import Image, ImageFont, ImageDraw
import io
import asyncio
 
"""
ЕСЛИ У ТЕБЯ ЧТО-ТО НЕ РАБОТАЕТ...
УСТАНОВИ МОДУЛИ.. НЕ ЗНАЕШЬ КАК? ГУГЛИ
"""
 
bad_words = [ 'маму ебал', 'путин хуйло', 'хохол', 'русня' ]
 
client = commands.Bot(command_prefix = "/", intents=discord.Intents.all())
client.remove_command('help')
 
@client.event
async def on_ready():
    print( 'client connected' )
 
    await client.change_presence( status = discord.Status.do_not_disturb, activity = discord.Game( 'Vortex Group Studio | IVTS' ) )
 
@client.event
async def on_command_error( ctx, error ):
    print(error)
    
@client.event
async def on_member_join( member ):
    channel = client.get_channel( 1104039559207067720 )
 
    role = discord.utils.get( member.guild.roles, id = 830734295538335774 )
 
    await member.add_roles( role )
    await channel.send( embed = discord.Embed( description = f'Пользователь ``{ member.name }``, присоеденился к нам!',
                         color = 0x3ec95d ) )
 
# Filter
@client.event
async def on_message( message ):
    await client.process_commands( message )
 
    msg = message.content.lower()
 
    if msg in bad_words:
        await message.delete()
        await message.author.send( f'{ message.author.name }, не надо такое писать!' )
 
 
@client.command()
async def math( ctx, a : int, arg, b : int ):
    if arg == '+':
        await ctx.send( f'Result: { a + b }' )
 
    elif arg == '-':
        await ctx.send( f'Result: { a - b }' )
 
    elif arg == '/':
        await ctx.send( f'Result: { a / b }' )
 
 
@client.command()
@commands.has_permissions(administrator=True)
async def ip_info( ctx, arg ):
    response = requests.get( f'http://ipinfo.io/{ arg }/json' )
 
    user_ip = response.json()[ 'ip' ]
    user_city = response.json()[ 'city' ]
    user_region = response.json()[ 'region' ]
    user_country = response.json()[ 'country' ]
    user_location = response.json()[ 'loc' ]
    user_org = response.json()[ 'org' ]
    user_timezone = response.json()[ 'timezone' ]
 
    global all_info
    all_info = f'\n<INFO>\nIP : { user_ip }\nCity : { user_city }\nRegion : { user_region }\nCountry : { user_country }\nLocation : { user_location }\nOrganization : { user_org }\nTime zone : { user_timezone }'
 
    await ctx.author.send( all_info )
 
@client.command()
@commands.has_permissions(administrator=True)
async def key( ctx ):
    import uuid
 
    await ctx.send( f'Key : { uuid.uuid4() }' )
 
@client.command()
async def w( ctx, *, arg ):
    owm = pyowm.OWM( 'e4e1efbc1a7afebbbc33ed068b32512c' )
    city = arg
 
    observation = owm.weather_at_place( city )
    w = observation.get_weather()
    temperature = w.get_temperature( 'celsius' )[ 'temp' ]
 
    await ctx.send( f'Температура в { city } : { temperature }' )
 
@client.command()
@commands.has_permissions(administrator=True)
async def phone_info( ctx, arg ):
    response = requests.get( f'https://htmlweb.ru/geo/api.php?json&telcod={ arg }' )
 
    user_country = response.json()[ 'country' ][ 'english' ]
    user_id = response.json()[ 'country' ][ 'id' ]
    user_location = response.json()[ 'country' ][ 'location' ]
    user_city = response.json()[ 'capital' ][ 'english' ]
    user_width = response.json()[ 'capital' ][ 'latitude' ]
    user_lenth = response.json()[ 'capital' ][ 'longitude' ]
    user_post = response.json()[ 'capital' ][ 'post' ]
    user_oper = response.json()[ '0' ][ 'oper' ]
 
    global all_info
    all_info = f'<INFO>\nCountry : { user_country }\nID : { user_id }\nLocation : { user_location }\nCity : { user_city }\nLatitude : { user_width }\nLongitude : { user_lenth }\nIndex post : { user_post }\nOperator : { user_oper }'
 
    await ctx.author.send( all_info )
 
# Clear message
@client.command()
@commands.has_permissions( administrator = True )
 
async def clear( ctx, amount : int ):
    await ctx.channel.purge( limit = amount )
 
    await ctx.send(embed = discord.Embed(description = f':white_check_mark: Удалено {amount} сообщений', color=0x0c0c0c))
 
# Kick
@client.command()
@commands.has_permissions( administrator = True )
 
async def kick( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )
    await member.kick( reason = reason )
 
    emb = discord.Embed( title = 'Информация об изгнании', description = f'{ member.name.title() }, был выгнан в связи нарушений правил',
    color = 0xc25151 )
 
    emb.set_author( name = member, icon_url = member.avatar_url )
    emb.set_footer( text = f'Был изганан администратором { ctx.message.author.name }', icon_url = ctx.author.avatar_url )
 
    await ctx.send( embed = emb )
 
# Ban
@client.command()
@commands.has_permissions( administrator = True )
 
async def ban( ctx, member: discord.Member, *, reason = None ):
    await ctx.channel.purge( limit = 1 )
    await member.ban( reason = reason )
 
    emb = discord.Embed( title = 'Информация о блокировке участника', description = f'{ member.name }, был заблокирован в связи нарушений правил',
    color = 0xc25151 )
 
    emb.set_author( name = member.name, icon_url = member.avatar_url )
    emb.add_field( name = f'ID: { member.id }', value = f'Блокированный участник : { member }' )
    emb.set_footer( text = 'Был заблокирован администратором {}'.format( ctx.author.name ), icon_url = ctx.author.avatar_url )
 
    await ctx.send( embed = emb )
 
# Unba
 
# Command help
@client.command()
@commands.has_permissions(administrator=True)
async def help( ctx ):
    emb = discord.Embed( 
        title = 'Навигация по командам :clipboard:',
        color = 0x7aa13d
     )
 
    emb.add_field( name = '**Основные команды**', value = '''
        .time - узнать текущее время :clock3:
        .ip_info - узнать информацию о IP адресе :satellite:
        .phone_info - узнать информацию о номере телефона :iphone:
        .w - узнать температуру в городе
        ''' )
 
    emb.add_field( name = '**Приколюшки**', value = '''
        .hack - взлом сервера :tools:
        .joke - шутка дня :face_with_raised_eyebrow:
        .fsociety - сектретная разработка :gear:
        ''' )
 
    await ctx.send( embed = emb )
 
@client.command()
 
async def time( ctx ):
    emb = discord.Embed( title = 'ВРЕМЯ', description = 'Вы сможете узнать текущее время', colour = discord.Color.green(), url = 'https://www.timeserver.ru' )
 
    emb.set_author( name = client.user.name, icon_url = client.user.avatar_url )
    emb.set_footer( text = 'Спасибо за использование нашего бота!' )
    emb.set_thumbnail( url = 'https://sun9-35.userapi.com/c200724/v200724757/14f24/BL06miOGVd8.jpg' )
 
    now_date = datetime.datetime.now()
 
    emb.add_field( name = 'Time', value = 'Time : {}'.format( now_date ) )
 
    await ctx.author.send( embed = emb )
 
 
@client.command()
@commands.has_permissions(administrator=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        engine = pyttsx3.init()
        engine.say('Привет, человечушки. Как жизнь на земле!?')
        engine.runAndWait()
 
@client.command()
@commands.has_permissions(administrator=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await channel.connect()
 

 
@client.command(aliases = ['я', 'карта']) # .я
async def card_user(ctx):
    await ctx.channel.purge(limit = 1)
 
    img = Image.new('RGBA', (400, 200), '#232529')
    url = str(ctx.author.avatar_url)[:-10]
 
    response = requests.get(url, stream = True)
    response = Image.open(io.BytesIO(response.content))
    response = response.convert('RGBA')
    response = response.resize((100, 100), Image.ANTIALIAS)
 
    img.paste(response, (15, 15, 115, 115))
 
    idraw = ImageDraw.Draw(img)
    name = ctx.author.name # Fsoky
    tag = ctx.author.discriminator # 9610
 
    headline = ImageFont.truetype('arial.ttf', size = 20)
    undertext = ImageFont.truetype('arial.ttf', size = 12)
 
    idraw.text((145, 15), f'{name}#{tag}', font = headline) # Fsoky#9610
    idraw.text((145, 50), f'ID: {ctx.author.id}', font = undertext)
 
    img.save('user_card.png')
 
    await ctx.send(file = discord.File(fp = 'user_card.png'))
 
 
@client.command(aliases = ['mute'])
@commands.has_permissions(administrator=True)
async def __mute(ctx, member: discord.Member = None, amount_time = None, *, reason = None):
    if member is None:
        await ctx.send(embed = discord.Embed(
            title = f'{ctx.author.mention}, **укажите пользователя**',
            description = f'Пример: .mute **@user** time reason'
        ))
    elif amount_time is None:
        await ctx.send(embed = discord.Embed(
            title = f'{ctx.author.mention}, **укажите кол-во времени**',
            description = f'Пример: .mute @user **time** reason'
        ))
    elif reason is None:
        await ctx.send(embed = discord.Embed(
            title = f'{ctx.author.mention}, **укажите причину**',
            description = f'Пример: .mute @user time **reason**'
        ))
    else:
        if 'm' in amount_time:
            await ctx.send(embed = discord.Embed(
                description = f'''**[<:_off:714370680463949834>]** Вы были замучены на **{amount_time}**.
                **Выдал мут:** {ctx.author}
                ```css
Причина: [{reason}]
                ```
                ''',
                color = 0x36393E,
            ))
 
            mute_role = discord.utils.get(ctx.guild.roles, id = 714369082492846150)
            await member.add_roles(mute_role)
            await asyncio.sleep(int(amount_time[:-1]) * 60)
            await member.remove_roles(mute_role)
 
            await ctx.send(embed = discord.Embed(
                description = f'''**[<:_on:714370680312954980>]** Время мута истекло, вы были размучены''',
                color = 0x2F3136
            ))  
        elif 'h' in amount_time:
            await ctx.send(embed = discord.Embed(
                description = f'''**[<:_off:714370680463949834>]** Вы были замучены на **{amount_time}**.
                **Выдал мут:** {ctx.author}
                ```css
Причина: [{reason}]
                ```
                ''',
                color = 0x36393E,
            ))
 
            mute_role = discord.utils.get(ctx.guild.roles, id = 714369082492846150)
            await member.add_roles(mute_role)
            await asyncio.sleep(int(amount_time[:-1]) * 60 * 60)
            await member.remove_roles(mute_role)
 
            await ctx.send(embed = discord.Embed(
                description = f'''**[<:_on:714370680312954980>]** Время мута истекло, вы были размучены''',
                color = 0x2F3136
            ))  
        elif 'd' in amount_time:
            await ctx.send(embed = discord.Embed(
                description = f'''**[<:_off:714370680463949834>]** Вы были замучены на **{amount_time}**.
                **Выдал мут:** {ctx.author}
                ```css
Причина: [{reason}]
                ```
                ''',
                color = 0x36393E,
            ))
 
            mute_role = discord.utils.get(ctx.guild, id = 714369082492846150)
            await member.add_roles(mute_role)
            await asyncio.sleep(int(amount_time[:-1]) * 60 * 60 * 24)
            await member.remove_roles(mute_role)
 
            await ctx.send(embed = discord.Embed(
                description = f'''**[<:_on:714370680312954980>]** Время мута истекло, вы были размучены''',
                color = 0x2F3136
            ))  
        else:
            await ctx.send(embed = discord.Embed(
                description = f'''**[<:_off:714370680463949834>]** Вы были замучены на **{amount_time}s**.
                **Выдал мут:** {ctx.author}
                ```css
Причина: [{reason}]
                ```
                ''',
                color = 0x36393E,
            ))
 
            mute_role = discord.utils.get(ctx.guild.roles, id = 714369082492846150)
            await member.add_roles(mute_role)
            await asyncio.sleep(int(amount_time))
            await member.remove_roles(mute_role)
 
            await ctx.send(embed = discord.Embed(
                description = f'''**[<:_on:714370680312954980>]** Время мута истекло, вы были размучены''',
                color = 0x2F3136
            ))  
 
 
# Get token
client.run(config.TOKEN)