import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
from email.errors import InvalidMultipartContentTransferEncodingDefect
import json
import discord_components
from BTSET import BD

class CheckMesBTST:
    def __init__(self, interaction):
        self.interaction: discord_components.Interaction = interaction

    def check(self, mes: discord.Message):
        return self.interaction.author == mes.author and self.interaction.channel == mes.channel

class SetForBTST():
    def __init__(self, bot, interaction, old_emb, arg):
        self.bot = bot
        self.interaction: discord_components.Interaction = interaction
        self.old_emb = old_emb
        self.arg = arg
        self.check = CheckMesBTST(interaction)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)

        self.data = data
        self.roles = data[str(interaction.guild.id)]['JoinRoles']
        self.COLOR = int(data[str(interaction.guild.id)]['COLOR'], 16)
        self.Classes = data[str(interaction.guild.id)]['ROLES']
        self.chlens = []
        self.serverRoles = []


        for i in range(0, len(interaction.guild.roles),
                       24):
            self.serverRoles.append(interaction.guild.roles[
                               i:i + 24])

        for i in range(0, len([chlen for chlen in interaction.guild.text_channels]),
                       24):
            self.chlens.append([chlen for chlen in interaction.guild.text_channels][
                          i:i + 24])


    async def music(self):
        if [i for i in self.interaction.guild.categories if i.name == 'music']:
            for category in self.interaction.guild.categories:
                [await chnl.delete() for chnl in category.channels if category.name == 'music']
            [await i.delete() for i in self.interaction.guild.categories if i.name == 'music']
        else:

            with open('music.json', 'r') as file:
                data_mus: dict = json.load(file)
            if not (str(self.interaction.guild.id) in [i for i in data_mus.keys()]):
                data_mus.update(
                    {
                        self.interaction.guild.id: {
                            'songs': [],
                            'pl_id': None,
                            'chl_id': None
                        }
                    }
                )

            with open('music.json', 'w') as file:
                json.dump(data_mus, file, indent=4)

            ctg = await self.interaction.guild.create_category(name='music')
            txt_cnlen = await ctg.create_text_channel(name='великий дон ягон')
            vc_clen = await ctg.create_voice_channel(name='music')
            embd = discord.Embed(
                title='***                               wave player***',
                description=f'=================================',
                colour=0x00FFFF
            )
            embd.add_field(name='сейчас играет:', value='ничего')

            comp = [
                [
                    Button(emoji='◀', style=2),
                    Button(emoji='⏯', style=2),
                    Button(emoji='▶', style=2),
                    Button(emoji='🔀', style=2)
                ],
                [
                    Button(emoji='➕', style=2),
                    Button(emoji='🔊', style=2),
                    Button(emoji='🔈', style=2),
                    Button(emoji='🔇', style=2)
                ]
            ]

            msc_player = await txt_cnlen.send(embed=embd, components=comp)

            await vc_clen.connect()

            with open('music.json', 'r') as file:
                data_mus = json.load(file)
                data_mus[str(self.interaction.guild.id)]['pl_id'] = msc_player.id
                data_mus[str(self.interaction.guild.id)]['chl_id'] = txt_cnlen.id
            with open('music.json', 'w') as file:
                json.dump(data_mus, file, indent=4)

    async def role_set(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='Укажите классы в которые вы хотите добавить роли', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb,
               components=[
                   Select(
                       placeholder='Укажите классы в которые вы хотите добавить роли',
                       max_values=len(self.data[str(self.interaction.guild.id)]['ROLES']),
                       min_values=1,
                       options=[SelectOption(label=str(i), value=str(i)) for i in
                                [k for k in self.Classes.keys()]]
                   ),
                   [
                       Button(label='модерация'),
                       Button(label='настройка бота'),
                       Button(label='настройка рейтинга')
                   ],
                   [
                       Button(label='<---'),
                       Button(label='OK'),
                       Button(label='--->')
                   ]
               ])

    async def add_roleclass(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='отправьте сообщение с названием класса', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb)

        ms: discord.Message = await self.bot.wait_for('message', check=self.check.check)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        if not (ms.content in data[str(self.interaction.guild.id)]['ROLES']):
            with open(f'{BD}users.json', 'w') as file:
                data[str(self.interaction.guild.id)]['ROLES'].update({ms.content: [[], []]})
                json.dump(data, file, indent=4)

        await ms.delete()

    async def color_choice(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='отправьте сообщение с цветом в hex', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb)
        await self.interaction.edit_origin()

        ms: discord.Message = await self.bot.wait_for('message', check=self.check.check)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        with open(f'{BD}users.json', 'w') as file:
            data[str(self.interaction.guild.id)]['COLOR'] = '0x' + ms.content
            json.dump(data, file, indent=4)
        await ms.delete()

    async def er_col_choice(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='отправьте сообщение с цветом в hex', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb)
        await self.interaction.edit_origin()

        ms: discord.Message = await self.bot.wait_for('message', check=self.check.check)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        with open(f'{BD}users.json', 'w') as file:
            data[str(self.interaction.guild.id)]['ErCOLOR'] = '0x' + ms.content
            json.dump(data, file, indent=4)
        await ms.delete()

    async def admin_clen(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.old_emb.description,
            color=self.old_emb.color
        )
        emb.add_field(name='выберете канал который хотите сделать каналом администратора',
                      value=f'страница 1 из {len(self.chlens)}')

        await self.interaction.message.edit(embed=emb, components=[
            Select(
                placeholder='выберете канал который хотите сделать каналом администратора',
                options=[SelectOption(label=i.name, value=str(i.id)) for i in self.chlens[0]]
            ),
            [
                Button(label='модерация'),
                Button(label='настройка бота'),
                Button(label='настройка рейтинга')
            ],
            [
                Button(label='<---'),
                Button(label='OK'),
                Button(label='--->')
            ]
        ])
        await self.interaction.edit_origin()

    async def ncaps(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='отправьте сообщение с цветом в hex', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb)

        ms: discord.Message = await self.bot.wait_for('message', check=self.check.check)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        with open(f'{BD}users.json', 'w') as file:
            data[str(self.interaction.guild.id)]['nCaps'] = ms.content
            json.dump(data, file, indent=4)
        await ms.delete()

    async def nwarns(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='отправьте сообщение с nwarns', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb)

        ms: discord.Message = await self.bot.wait_for('message', check=self.check.check)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        with open(f'{BD}users.json', 'w') as file:
            data[str(self.interaction.guild.id)]['nWarns'] = ms.content
            json.dump(data, file, indent=4)
        await ms.delete()

    async def add_bad_word(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='отправьте сообщение с цветом в hex', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb)

        ms: discord.Message = await self.bot.wait_for('message', check=self.check.check)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        with open(f'{BD}users.json', 'w') as file:
            data[str(self.interaction.guild.id)]['BADWORDS'].append(ms.content)
            json.dump(data, file, indent=4)
        await ms.delete()

    async def remove_bod_word(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='отправьте сообщение с цветом в hex', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb)

        ms: discord.Message = await self.bot.wait_for('message', check=self.check.check)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        if ms.channel in data[str(self.interaction.guild.id)]['BADWORDS']:
            with open(f'{BD}users.json', 'w') as file:
                data[str(self.interaction.guild.id)]['BADWORDS'].pop(
                    data[str(self.interaction.guild.id)]['BADWORDS'].index(ms.content))
                json.dump(data, file, indent=4)
        else:
            await self.interaction.send('слова нет')
        await ms.delete()

    async def selfrooms(self):
        chlen_krokodila = self.interaction.channel

        if self.data[str(self.interaction.guild.id)]['selfRoom'] != '0':
            for category in self.interaction.guild.categories:
                [await chnl.delete() for chnl in category.channels if
                 str(category.id) == self.data[str(self.interaction.guild.id)]['selfRoom']["ct"]]
            [await i.delete() for i in self.interaction.guild.categories if
             str(i.id) == self.data[str(self.interaction.guild.id)]['selfRoom']["ct"] or str(i.id) ==
             self.data[str(self.interaction.guild.id)]['selfRoom']["ctp"]]
            self.data[str(self.interaction.guild.id)]['selfRoom'] = '0'
            await chlen_krokodila.send(embed=discord.Embed(title='***Успешно***',
                                                           description='Канал для создания комнат удалён',
                                                           color=self.COLOR))
        else:
            ct = await self.interaction.guild.create_category(name='ССК', position=1)
            vcch = await self.interaction.guild.create_voice_channel(name=f'Создать комнату', category=ct)
            chn = await self.interaction.guild.create_text_channel(name=f'Настройка комнаты', category=ct)
            ctp = await self.interaction.guild.create_category(name='Свои румы', position=2)
            emb = discord.Embed(title='***⚙️ Управление приватными комнатами***',
                                description=f'<:corona1:1020971032309403758> - назначить нового создателя комнаты \n\
                                    <:notebook1:1020971040416993280> - ограничить/выдать доступ к комнате \n\
                                    <:meet1:1020971037741043713> - задать новый лимит участников \n\
                                    <:locker1:1020971036252053524> - закрыть/открыть комнату \n\
                                    <:pencil1:1020971043856330782> - изменить название комнаты \n\
                                    <:eye1:1020971035014746162> - скрыть/открыть комнату \n\
                                    <:door1:1020971033756450866> - выгнать участника из комнаты \n\
                                    <:microphone1:1020971039141920819> - ограничить/выдать право говорить',
                                color=self.COLOR)
            stb_gld: discord.Guild = self.bot.get_guild(id=981511419042361344)
            await chn.send(embed=emb,
                           components=[
                               [
                                   Button(emoji=await stb_gld.fetch_emoji(1020971032309403758)),
                                   Button(emoji=await stb_gld.fetch_emoji(1020971040416993280)),
                                   Button(emoji=await stb_gld.fetch_emoji(1020971037741043713)),
                                   Button(emoji=await stb_gld.fetch_emoji(1020971036252053524))
                               ],
                               [
                                   Button(emoji=await stb_gld.fetch_emoji(1020971043856330782)),
                                   Button(emoji=await stb_gld.fetch_emoji(1020971035014746162)),
                                   Button(emoji=await stb_gld.fetch_emoji(1020971033756450866)),
                                   Button(emoji=await stb_gld.fetch_emoji(1020971039141920819))
                               ]
                           ]
                           )
            self.data[str(self.interaction.guild.id)]['selfRoom'] = {"ct": str(ct.id), "ctp": str(ctp.id),
                                                           "vc": str(vcch.id),
                                                           "tc": str(chn.id)}
            ow2 = discord.PermissionOverwrite()
            ow2.send_messages = False
            await chn.set_permissions(target=self.interaction.guild.roles[0], overwrite=ow2)
            await chlen_krokodila.send(embed=discord.Embed(title='***Успешно***',
                                                           description='Канал для создания комнат создан',
                                                           color=self.COLOR))
            with open(f'{BD}users.json', 'w') as file:
                json.dump(self.data, file, indent=4)

    async def prefix(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='отправьте сообщение с цветом в hex', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb)

        ms: discord.Message = await self.bot.wait_for('message', check=self.check.check)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        with open(f'{BD}users.json', 'w') as file:
            data[str(self.interaction.guild.id)]['PREFIX'] = ms.content
            json.dump(data, file, indent=4)
        await ms.delete()

    async def selftitle(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.arg,
            color=self.COLOR
        )
        emb.add_field(name='отправьте сообщение с цветом в hex', value='страница 1 из 1')
        await self.interaction.message.edit(embed=emb)

        ms: discord.Message = await self.bot.wait_for('message', check=self.check.check)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        with open(f'{BD}users.json', 'w') as file:
            data[str(self.interaction.guild.id)]['SelfTitle'] = ms.content
            json.dump(data, file, indent=4)
        await ms.delete()

    async def join_roles(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.old_emb.description,
            color=self.old_emb.color
        )
        emb.add_field(name=f'Укажите роли которые будут выдоваться участникам при входе на сервер',
                      value=f'страница 1 из {len(self.serverRoles)}')

        await self.interaction.message.edit(components=[
            Select(
                placeholder=f'Укажите роли которые будут выдоваться участникам при входе на сервер',
                max_values=len(self.serverRoles[0]),
                min_values=0,
                options=[SelectOption(label=i.name, value=str(i.id)) for i in self.serverRoles[0]]
            ),
            [
                Button(label='модерация'),
                Button(label='настройка бота'),
                Button(label='настройка рейтинга')
            ],
            [
                Button(label='<---'),
                Button(label='OK'),
                Button(label='--->')
            ]
        ])

    async def info_clen(self):
        with open('glb_vote.json', 'r') as file:
            vt_data = json.load(file)

        if not (str(self.interaction.guild.id) in [k for k in vt_data.keys()]):

            ct = await self.interaction.guild.create_category(name='ссссссс', position=1)
            chn = await self.interaction.guild.create_text_channel(name=f'Голосование от wave', category=ct)
            chn1 = await self.interaction.guild.create_text_channel(name=f'Информация от wave', category=ct)

            vt_data.update({
                self.interaction.guild.id: {
                    'vote_id': chn.id,
                    'info_id': chn1.id
                }
            })
        else:
            await self.interaction.guild.get_channel(vt_data[str(self.interaction.guild.id)]['vote_id']).category.delete()
            await self.interaction.guild.get_channel(vt_data[str(self.interaction.guild.id)]['vote_id']).delete()
            await self.interaction.guild.get_channel(vt_data[str(self.interaction.guild.id)]['info_id']).delete()
            del vt_data[str(self.interaction.guild.id)]

        with open('glb_vote.json', 'w') as file:
            json.dump(vt_data, file, indent=4)


class SecSetForBTST():
    def __init__(self, bot, interaction, old_emb):
        self.bot = bot
        self.interaction: discord_components.Interaction = interaction
        self.old_emb = old_emb
        self.check = CheckMesBTST(interaction)

        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)

        self.data = data
        self.roles = data[str(interaction.guild.id)]['JoinRoles']
        self.COLOR = int(data[str(interaction.guild.id)]['COLOR'], 16)
        self.Classes = data[str(interaction.guild.id)]['ROLES']
        self.chlens = []
        self.serverRoles = []

        for i in range(0, len(interaction.guild.roles),
                       24):
            self.serverRoles.append(interaction.guild.roles[
                                    i:i + 24])

        for i in range(0, len([chlen for chlen in interaction.guild.text_channels]),
                       24):
            self.chlens.append([chlen for chlen in interaction.guild.text_channels][
                               i:i + 24])


    async def rolecass_choice(self):
        emb = discord.Embed(
            title=self.old_emb.title,
            description=self.old_emb.description,
            color=self.old_emb.color
        )
        emb.add_field(name=f'Укажите роли которые вы хотите добавить в класс {self.interaction.values[0]}',
                      value=f'страница 1 из {len(self.interaction.values)}')
        await self.interaction.message.edit(embed=emb,
           components=[
               Select(
                   placeholder=f'Укажите роли которые вы хотите добавить в класс *{self.interaction.values[0]}',
                   max_values=len(self.serverRoles[0]),
                   min_values=0,
                   options=[SelectOption(label=i.name, value=i.id) for i in
                            self.serverRoles[0]]
               ),
               [
                   Button(label='модерация'),
                   Button(label='настройка бота'),
                   Button(label='настройка рейтинга')
               ],
               [
                   Button(label='<---'),
                   Button(label='OK'),
                   Button(label='--->')
               ]
           ])

    async def role_choice(self):
        self.data[str(self.interaction.author.guild.id)]['ROLES'][self.interaction.component.placeholder.split('*')[1]][
            0] = self.interaction.values
        self.data[str(self.interaction.author.guild.id)]['ROLES'][self.interaction.component.placeholder.split('*')[1]][1] = [0 for
                                                                                                               i in
                                                                                                               self.interaction.values]
        await self.interaction.send(embed=discord.Embed(
            title=f'Роли выбранны',
            color=self.COLOR
        ))

        with open(f'{BD}users.json', 'w') as file:
            json.dump(self.data, file, indent=4)

    async def admin_clen(self):
        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        data[str(self.interaction.guild.id)]['idAdminchennel'] = self.interaction.values[0]
        with open(f'{BD}users.json', 'w') as file:
            json.dump(data, file, indent=4)
        await self.interaction.send(embed=discord.Embed(
            title="Успешно",
            description=f"*Канал администратора изменен на {self.interaction.values[0]}*",
        ))

    async def join_roles(self):
        with open(f'{BD}users.json', 'r') as file:
            data = json.load(file)
        data[str(self.interaction.guild.id)]['JoinRoles'] = self.interaction.values
        await self.interaction.send('роли выбранны')
        with open(f'{BD}users.json', 'w') as file:
            json.dump(data, file, indent=4)



