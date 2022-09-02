from turtle import title
from typing import Optional
import discord
import json
from discord.ext import commands
from discord.utils import get
from BD import bdpy, bdint
from typing import Optional
import interactions
from interactions import TextInput, Modal, TextStyleType, SelectMenu, SelectOption
import datetime
import pytz
from BTSET import embint
moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
n = {}
class Warnspy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx: commands.Context, memberr: discord.Member, reason: str):
        member = memberr
        COLOR = bdpy(ctx)['COLOR']
        BADWORDS = bdpy(ctx)['BADWORDS']
        LINKS = bdpy(ctx)['LINKS']
        WARN = []
        WARN.extend(BADWORDS); WARN.extend(LINKS)
        warns = bdpy(ctx)['USERS'][str(memberr.id)]['WARNS']
        nWarns = bdpy(ctx)['nWarns']

        
        with open('users.json', 'r') as file:
            data = json.load(file)
        with open('users.json', 'w') as file:
            data[str(member.guild.id)]['USERS'][str(member.id)]['WARNS'] += 1
            json.dump(data, file, indent=4)
        #====================================================================
        #audit
        #====================================================================
        emb = discord.Embed(
            title='Нарушение',
            description=f"*Ранее, у нарушителя было уже {data[str(member.guild.id)]['USERS'][str(member.id)]['WARNS'] - 1} нарушений, после {nWarns} он будет забанен!*",
            timestamp=ctx.message.created_at,
            color=COLOR
        )
        emb.add_field(name='Канал:', value='Не определён', inline=True)
        emb.add_field(name='Нарушитель:', value=member.mention, inline=True)
        emb.add_field(name='Причина:', value=f'{reason}', inline=True)
        await get(ctx.guild.text_channels, id=int(data[str(ctx.author.guild.id)]['idAdminchennel'])).send(embed=emb)
        #====================================================================
        #rep
        #====================================================================
        await ctx.message.reply(embed=discord.Embed(
            title="Успешно",
            description="*Предупреждение выдано*",
            timestamp=ctx.message.created_at,
            color=COLOR
        )) #delete_after(10.0) float
        #====================================================================
        #ls
        #====================================================================
        emb=discord.Embed(
            title='Нарушение',
            description=f'Вы получили нарушение на сервере ***{ctx.guild.name}***\nПричина: {reason}',
            timestamp=ctx.message.created_at,
            color = COLOR
        )
        emb.add_field(name='Текущее кол-во нарушений', value=f'{warns}/{nWarns}', inline=True)
        emb.set_footer(text=f'Нарушение выдано {ctx.author.name}#{ctx.author.discriminator} ID модератора: {ctx.author.id}')
        await memberr.send(embed=emb)
        #====================================================================
        if data[str(member.guild.id)]['USERS'][str(member.id)]['WARNS'] >= nWarns:
            await member.ban(reason='Вы привысили допустимое количество нарушений')
        #====================================================================


    #======================ERROR=======================================
    @warn.error
    async def error(self, ctx: commands.Context, error):
        ErCOLOR = bdpy(ctx)['ErCOLOR']
        pref = bdpy(ctx)['PREFIX']
        BADWORDS = bdpy(ctx)['BADWORDS']
        LINKS = bdpy(ctx)['LINKS']
        WARN = []
        WARN.extend(BADWORDS); WARN.extend(LINKS)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                title="Ошибка",
                description=f"*Использование: {pref}warn (@Участник) (Причина)",
                color=ErCOLOR
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                title="Ошибка",
                description="*У вас недостаточно прав!*",
                color=ErCOLOR
            ))
    #======================ERROR=======================================

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unwarn(self, ctx: commands.Context, memberr: Optional[discord.Member]):
        member = memberr or ctx.author
        COLOR = bdpy(ctx)['COLOR']
        BADWORDS = bdpy(ctx)['BADWORDS']
        LINKS = bdpy(ctx)['LINKS']
        WARN = []
        WARN.extend(BADWORDS); WARN.extend(LINKS)
        nWarns = bdpy(ctx)['nWarns']
        warns = bdpy(ctx)['USERS'][str(memberr.id)]['WARNS']
        with open('users.json', 'r') as file:
            data = json.load(file)
        with open('users.json', 'w') as file:
            data[str(member.guild.id)]['USERS'][str(member.id)]['WARNS'] -= 1
            json.dump(data, file, indent=4)
        #====================================================================
        #audit
        #====================================================================
        emb = discord.Embed(
            title='Нарушение снято!',
            description=f"*Ранее, у участника было уже {data[str(member.guild.id)]['USERS'][str(member.id)]['WARNS'] - 1} нарушений, после {nWarns} он будет забанен!*",
            timestamp=ctx.message.created_at,
            color=COLOR
        )                                                                                                                   #переписать под unwarn
        emb.add_field(name='Канал:', value='Не определён', inline=True)
        emb.add_field(name='Участник:', value=member.mention, inline=True)
        emb.set_footer(text=f'Предупреждение снято участником {ctx.author.name}#{ctx.author.discriminator} ID модератора: {ctx.author.id}')
        await get(ctx.guild.text_channels, id=int(data[str(ctx.author.guild.id)]['idAdminchennel'])).send(embed=emb)
        #====================================================================
        #rep
        #==================================================================== 
        await ctx.send(embed=discord.Embed(
            title="Успешно",
            description="Предупреждение снято!",
            timestamp=ctx.message.created_at,
            color=COLOR
        ))
        #====================================================================
        #ls
        #====================================================================
        emb=discord.Embed(
            title='Нарушение',
            description=f'Вам было прощено нарушение!',
            timestamp=ctx.message.created_at,
            color = COLOR
        )
        emb.add_field(name='Текущее кол-во нарушений', value=f'{warns}/{nWarns}', inline=True)
        emb.set_footer(text=f'Нарушение снято учасником{ctx.author.name}#{ctx.author.discriminator} ID модератора: {ctx.author.id}')
        await memberr.send(embed=emb)
        #====================================================================

    #======================ERROR=======================================
    @unwarn.error
    async def error(self, ctx: commands.Context, error):
        ErCOLOR = bdpy(ctx)['ErCOLOR']
        pref = bdpy(ctx)['PREFIX']
        BADWORDS = bdpy(ctx)['BADWORDS']
        LINKS = bdpy(ctx)['LINKS']
        WARN = []
        WARN.extend(BADWORDS); WARN.extend(LINKS)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                title="Ошибка",
                description=f"*Использование: {pref}unwarn (@Участник)",
                color=ErCOLOR
            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                title="Ошибка",
                description="*У вас недостаточно прав!*",
                color=ErCOLOR
            ))
    #======================ERROR=======================================

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear_warns(self, ctx: commands.Context, memberr: Optional[discord.Member]):
        member = memberr or ctx.author
        COLOR = bdpy(ctx)['COLOR']
        BADWORDS = bdpy(ctx)['BADWORDS']
        LINKS = bdpy(ctx)['LINKS']
        WARN = []
        WARN.extend(BADWORDS); WARN.extend(LINKS)
        warns = bdpy(ctx)['USERS'][str(memberr.id)]['WARNS']
        nWarns = bdpy(ctx)['nWarns']
        with open('users.json', 'r') as file:
            data = json.load(file)
        with open('users.json', 'w') as file:
            data[str(member.guild.id)]['USERS'][str(member.id)]['WARNS'] = 0
            json.dump(data, file, indent=4)
        #====================================================================
        #audit
        #====================================================================
        emb = discord.Embed(
            title='Нарушения очищены',
            description=f"*Ранее, у нарушителя было уже {data[str(member.guild.id)]['USERS'][str(member.id)]['WARNS'] - 1} нарушений, после {nWarns} он будет забанен!*",
            timestamp=ctx.message.created_at,
            color=COLOR
        )                                                                                                               #переписать под clear_warn
        emb.add_field(name='Канал:', value='Не определён', inline=True)
        emb.add_field(name='Участник:', value=member.mention, inline=True)
        emb.set_footer(text=f'Нарушения очищены учасником{ctx.author.name}#{ctx.author.discriminator} ID модератора: {ctx.author.id}')
        await get(ctx.guild.text_channels, id=int(data[str(ctx.author.guild.id)]['idAdminchennel'])).send(embed=emb)
        #====================================================================
        #rep
        #====================================================================
        await ctx.send(embed=discord.Embed(
            title="Успешно",
            description="Предупреждения сняты!",
            timestamp=ctx.message.created_at,
            color=COLOR
        ))
        #====================================================================
        #ls
        #====================================================================
        emb=discord.Embed(
            title='Нарушение',
            description=f'С вас сняли все предупреждения!',
            timestamp=ctx.message.created_at,
            color = COLOR
        )
        emb.add_field(name='Текущее кол-во нарушений', value=f'{warns}/{nWarns}', inline=True)
        emb.set_footer(text=f'Нарушения сняты участником{ctx.author.name}#{ctx.author.discriminator} ID модератора: {ctx.author.id}')
        await memberr.send(embed=emb)
        #====================================================================


    #======================ERROR=======================================
    @clear_warns.error
    async def error(self, ctx: commands.Context, error):
        ErCOLOR = bdpy(ctx)['ErCOLOR']
        pref = bdpy(ctx)['PREFIX']
        BADWORDS = bdpy(ctx)['BADWORDS']
        LINKS = bdpy(ctx)['LINKS']
        WARN = []
        WARN.extend(BADWORDS); WARN.extend(LINKS)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                title="Ошибка",
                description=f"*Использование: {pref}clear_warns (@Участник)",
                color=ErCOLOR

            ))
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(
                title="Ошибка",
                description="*У вас недостаточно прав!*",
                color=ErCOLOR
            ))
    #======================ERROR=======================================


class Warnsint(interactions.Extension):
    def __init__(self, client):
        self.client = client
    @interactions.extension_message_command(
        name='warns'
    )
    async def warns_int(self, ctx: interactions.CommandContext):
        n.update({str(ctx.author.id): [str(ctx.target.author.id), str(ctx.target.author.mention), str(ctx.target.content), str(ctx.target.timestamp.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Europe/Moscow')).strftime('%H:%M || %d.%m.%y')), str(ctx.target.channel_id)]})
        await ctx.popup(Modal(
                custom_id='warns',
                title=' ',
                components=[
                    TextInput(
                        style=TextStyleType.SHORT,
                        custom_id='qwertyuiop',
                        label='тип нарушения'
                    )
                ]
            ))
    @interactions.extension_modal('warns')
    async def wrn(self, ctx: interactions.CommandContext, shrt):
        with open('users.json', 'r') as file:
            data = json.load(file)
        COLOR = bdint(ctx)['COLOR']
        nWarns = bdint(ctx)['nWarns']
        idAdminchennel = bdint(ctx)['idAdminchennel']
        #====================================================================
        #audit
        #====================================================================
        emb = interactions.Embed(
            title='Нарушение',
            description=f"*Ранее, у нарушителя было уже {bdint(ctx)['USERS'][str(n[str(ctx.author.id)][0])]['WARNS'] - 1} нарушений, после {nWarns} он будет забанен!*",
            timestamp=moscow_time,
            color=COLOR
        )
        
        emb.add_field(name='Сообщение нарушителя:', value=str(n[str(ctx.author.id)][2]), inline=True)
        emb.add_field(name='Время нарушения:', value=n[str(ctx.author.id)][3])
        a = await ctx.get_guild()
        b = await a.get_all_channels()
        for i in b:
            if str(i.id) == str(n[str(ctx.author.id)][4]):
                emb.add_field(name='Канал:', value=i.mention, inline=True)
        emb.add_field(name='Нарушитель:', value=n[str(ctx.author.id)][1], inline=True)
        emb.add_field(name='Тип нарушения:', value=str(shrt), inline=True)
        emb.set_footer(text=f'Нарушение выдал учасник {ctx.author.name}, ID учасника: {ctx.author.id}')
        c = await ctx.get_guild()
        d = await c.get_all_channels()
        for i in d:
            if str(i.id) == str(idAdminchennel):
                await i.send(embeds=emb)
        with open('users.json', 'w') as file:
            data[str(ctx.guild_id)]['USERS'][str(n[str(ctx.author.id)][0])]['WARNS'] +=1
            json.dump(data, file, indent=4)
        for i in [k for k in n.keys()]:
            if i == str(ctx.author.id):
                n.pop(i)
        #====================================================================
        #rep
        #====================================================================
        await ctx.send(embeds=interactions.Embed(
            title='Успешно',
            description=f'Предупреждение успешно выдано участнику {n[str(ctx.author.id)][1]}!',
            timestamp=ctx.message.created_at,
            color=COLOR
        ), ephemeral=True)
        #====================================================================
        #ls
        #====================================================================
        emb=discord.Embed(
            title='Нарушение',
            description=f'Вы получили нарушение на сервере ***{ctx.guild.name}***\nПричина: {shrt}',
            timestamp=ctx.message.created_at,
            color = COLOR
        )
        emb.add_field(name='Текущее кол-во нарушений', value=f'{warns}/{nWarns}', inline=True)
        emb.set_footer(text=f'Нарушение выдано {ctx.author.name}#{ctx.author.discriminator} ID модератора: {ctx.author.id}')
        memberr = [ i for i in ctx.guild.get_all_mambers() if str(i.id) == str(n[str(ctx.author.id)][0])][0]
        await memberr.send(embed=emb)                                                                               #найти юзера
        #====================================================================
        if data[str(ctx.guild_id)]['USERS'][str(n[str(ctx.author.id)][0])]['WARNS'] >= nWarns:
            await member.ban(reason='Вы привысили допустимое количество нарушений')                                 #найти юзера
        #====================================================================
def setup(bot):
    if str(bot).startswith('<d'):
        bot.add_cog(Warnspy(bot))
    elif str(bot).startswith('<i'):
        Warnsint(bot)