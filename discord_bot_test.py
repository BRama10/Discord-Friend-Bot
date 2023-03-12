import discord
from discord.ext import commands



TOKEN = "MTA1Mjc2NzE2MDIyMjYzNDAzNg.GWHOA6.VZviWLmrJJ_eiUz7Li6aNaSfsyyoIWP0kYGAT8"

intents = discord.Intents.all()

discord_client = discord.Client(intents=intents)



async def test():
    
    
    print(member)
USERNAME ='BR_Study#6314'
COLOR = 'Pink'
HOBBY = 'Waltz'

@discord_client.event
async def on_ready():
    global inviteLink, USERNAME, result
    
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
    
discord_client.run(TOKEN)

    
