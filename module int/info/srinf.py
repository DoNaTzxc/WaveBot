import interactions
import discord
from BD import bdint
from discord.ext import commands
class Srinfint(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client
    @interactions.extension_command(
        name="server info",
        description="Узнать информацию о сервере",
    )
    async def server_info(self, ctx):
        COLOR = bdint(ctx)['COLOR']
            
        emb = interactions.Embed(title=f'Информация о сервере ***{str(ctx.message.guild)}***',
                            description="Основная информация",
                            color=COLOR
                            )
        emb.set_thumbnail(url=ctx.author.guild.icon_url) 
        emb.add_field(name='Количество участников: ', value=ctx.message.guild.member_count)
        emb.add_field(name='Владелец: ', value=ctx.message.guild.owner)
        emb.add_field(name='Дата создания: ', value=ctx.message.guild.created_at.strftime("%d.%m.%y"))
        await ctx.send(embeds=emb)

    @interactions.extension_command(
        name="server info in channels",
        description="Установить каналы с инфорацией о количестве пользователей",
    ) #Доделать. Знаю что доделать делаю делаю и думаю о том что ты пидр ведь мог бы и сам сделать а ты что-то другое делаешь а мне ещё документацию писать я тут сдохну 
    async def server_info_channel(self, ctx, arg=None):
        if arg == 'on':
            if not('📊Info📊' in [i.name for i in ctx.guild.categories]):
                ct = await ctx.guild.create_category(name='📊Info📊', position=0)
                await ctx.guild.create_voice_channel(name=f'👥Members: {len(ctx.guild.members)}👥', category=ct)
                await ctx.guild.create_voice_channel(name=f'🤖Bots: {len([i for i in ctx.guild.members if i.bot])}🤖', category=ct)
                await ctx.guild.create_voice_channel(name=f'👤Humans: {len(ctx.guild.members) - len([i for i in ctx.guild.members if i.bot])}👤', category=ct)
                pr = discord.PermissionOverwrite()
                pr.connect = False
                [await chlen.set_permissions(target=ctx.guild.roles[0], overwrite=pr) for chlen in ct.channels]
        if arg == 'off':
            if '📊Info📊' in [i.name for i in ctx.guild.categories]:
                [await i.delete() for i in [ii.channels for ii in ctx.guild.categories if ii.name == '📊Info📊'][0]]
                [await ii.delete() for ii in ctx.guild.categories if ii.name == '📊Info📊']
def setup(client):    
    Srinfint(client)