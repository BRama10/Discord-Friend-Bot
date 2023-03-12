import discord
from quart import Quart, render_template, request, redirect, url_for
from time import sleep
from mail import Email
from discord.ext import commands
import os
import asyncio
from google.cloud.sql.connector import Connector
import sqlalchemy


TOKEN = "MTA1Mjc2NzE2MDIyMjYzNDAzNg.GWHOA6.VZviWLmrJJ_eiUz7Li6aNaSfsyyoIWP0kYGAT8"

intents = discord.Intents.all()

discord_client = discord.Client(intents=intents)

#bot = commands.Bot(command_prefix='!', intents=intents)
#id1 = 839525228283822092
#await discord_client.run(TOKEN)

DB_USER = 'root'
DB_PASS= '1q2w3eASD123'
DB_NAME = 'user_data'
INSTANCE_CONNECTION_NAME = 'python-discord-bot-371723:us-east4:discord-user-info'



# function to return the database connection object
def getconn():
    connector = Connector()
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME
    )
    return conn


inviteLink = ''
USERNAME, COLOR, HOBBY = '', '', ''
FAIL = False
result = ''
app = Quart(__name__)


@app.route('/startup/gen/trigger/mail')
async def method1():
    return await render_template('generate_url.html')

@app.route('/startup/gen/trigger/send', methods = ['POST','GET'])
async def method2():
    global inviteLink, USERNAME, COLOR, HOBBY
    USERNAME, COLOR, HOBBY = '', '', ''
    if request.method == 'POST':
        details = await request.form
        email = details['username']

        await discord_client.start(TOKEN)
        print('started')

        print('closed')

        #print(account)
        
        e = Email(email)
        e.createHeaders('Discord Server Invite & Instructions.')
        e.createBody(str(inviteLink), 'https://docs.google.com/forms/d/e/1FAIpQLSd4MVcpUkzqz1sWSgKMbNE3QPH2GbFycfgHeIZlpjQK3qtfdQ/viewform?usp=sf_link')
        e.sendMessage()
        inviteLink = ' '

        return await render_template('submitted_url.html')


@app.route('/register_user/<username>/<identifier>', methods=['GET'])
async def method3(username, identifier):
    global USERNAME, result, COLOR, HOBBY
    
    USERNAME = username+'#'+identifier
    
    query = "SELECT * FROM `user_data` WHERE `user_data`.`username` = '{}'".format(USERNAME)

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )

    
    
    with pool.connect() as db_conn:
        result = db_conn.execute(query).fetchone()
    print('result', result)


    discord_roles_dict = {
        'Dying :)' : 'Dead Person xD',
        'Being Cheerful :)' : 'Happy Camper',
        'Sports :)' : 'Olympian',
        'Reading :)' : 'Professor',
        'Dancing :)' : 'Waltz',
        'Anything Else :(' : 'Somebody'
        }
    
    #harcode ftw [I BETTER CHANGE THIS LEST I DIE]
    COLOR = result['color']
    #HOBBY = result['hobby'].get(discord_roles_dict)
    HOBBY = discord_roles_dict.get(result['hobby'])
    print('USERNAME', USERNAME)
    print('start')
    await discord_client.start(TOKEN)
    print('end')

    #connector.close()
    
    return 'DONE'

async def get_members_all_of_them():
    
    #async for member in guild.fetch_members():
    
    #member = guild.get_member_named('..AirBorN...#3924')
    #print(member.name)

    
    print('abdcd')


@discord_client.event
async def on_ready():
    global inviteLink, USERNAME, result, COLOR, HOBBY
    
    guild = discord_client.guilds[0]
    channel = discord.utils.get(guild.channels, name='general')
    inviteLink = await channel.create_invite(max_uses=1, unique=True)
    print('USERNAME-DISCORD', USERNAME)
    if USERNAME == '':
        FAIL = True
        await discord_client.close()
    else:
        member =  guild.get_member_named(USERNAME)
        print('member', member)
        role_color = discord.utils.get(guild.roles, name = COLOR)
        print('role_color', role_color)
        role_hobby = discord.utils.get(guild.roles, name = HOBBY)
        print('role_hobby', role_hobby)
        
        j = await member.add_roles(role_color)
        k = await member.add_roles(role_hobby)

        print(j)
        print(k)
        USERNAME = ''

    await discord_client.close()


#app.run(port=8080,host='0.0.0.0')
  



