import json
from discord.ext import commands

class Json_write(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def jsonwrite(self):
        for guild in self.bot.guilds:
            with open('../WaveBot-main/users.json', 'r') as file:
                data = json.load(file)
                if not (str(guild.id) in [k for k in data.keys()]):
                    data.update({
                        guild.id: {
                            'COLOR': '0x0000FF',
                            'ErCOLOR': '0x8B0000',
                            'AUDIT': {},
                            'AUDIT_CHANNEL': '0',
                            'JoinRoles': [],
                            'ModRoles': [],
                            'ROLES': {},
                            'actmoduls': '',
                            'nCaps': -1,
                            'nWarns': 10,
                            'idAdminchennel': '0',
                            'idMainch': '0',
                            'selfRoom': '0',
                            'BADWORDS': [],
                            'LINKS': [],
                            'PREFIX': '~',
                            'JNMSG': '',
                            'SelfTitle': '*Выберите ваши роли:* ',
                            'Selfrooms': {},
                            'Mafrooms': {},
                            'IgnoreChannels': [[], []],
                            'IgnoreRoles': [[], []],
                            'card': 'wave.png',
                            'text_color': '#d0ed2b',
                            'bar_color': '#ec5252',
                            'blend': 1,
                            'USERS': {},
                        }})

            with open('users.json', 'w') as file:
                json.dump(data, file, indent=4)
            for member in guild.members:
                with open('users.json', 'r') as file:
                    dat = json.load(file)
                if not (str(member.id) in [str(k) for k in dat[str(guild.id)]['USERS'].keys()]):
                    dat[str(guild.id)]['USERS'].update({
                        str(member.id): {
                            'WARNS': 0,
                            'CAPS': 0,
                            "SCR": 0,
                            'LvL': 1
                        }})
                with open('users.json', 'w') as file:
                    json.dump(dat, file, indent=4)



    @commands.Cog.listener('on_member_join')
    async def n_mr_join(self, ctx):
        Json_write.jsonwrite()

    @commands.Cog.listener('on_member_remove')
    async def on_meove(self, ctx):
        Json_write.jsonwrite()

    @commands.Cog.listener('on_guild_join')
    async def on_gld_jn(self, ctx):
        Json_write.jsonwrite()

    @commands.Cog.listener('on_guild_remove')
    async def on_gld_remove(self, ctx):
        Json_write.jsonwrite()

def setup(bot):
    bot.add_cog(Json_write(bot))
