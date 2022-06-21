import logging

import discord
from discord import User

from database import Database
from settings import DISCORD_BOT_TOKEN, LOG_LEVEL, DB_URL, DISCORD_GUILD_ID, \
    DISCORD_CHANNEL_ID, DISCORD_ADMINS

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=LOG_LEVEL)

db = Database(DB_URL)


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180, user=None, admin=None):
        super().__init__(timeout=timeout)
        self.user = user
        self.admin = admin

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Interaction,
                           button: discord.ui.Button):
        channel = client.get_guild(DISCORD_GUILD_ID).get_channel(
            DISCORD_CHANNEL_ID)
        invite_link = await channel.create_invite(max_uses=1, unique=True)
        await self.user.send(
            'You\'re successful approved and '
            'been invited to join ByBit chat :white_check_mark:\n' +
            str(invite_link)
        )

        self.green_button.disabled = True
        self.red_button.disabled = True
        await interaction.response.edit_message(
            content=self.user.name + ' has been successfully approved and '
                                     'invited to the ByBit chat!',
            view=self
        )

        logger.info(self.user.name + ' has been approved by ' + self.admin.name)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def red_button(self, interaction: discord.Interaction,
                         button: discord.ui.Button):
        await self.user.send('You was denied to join to the ByBit chat :(')

        self.green_button.disabled = True
        self.red_button.disabled = True
        await interaction.response.edit_message(
            content=self.user.name + ' has been successfully denied!',
            view=self
        )

        logger.info(self.user.name + ' has been denied by ' + self.admin.name)


class MyClient(discord.Client):
    async def on_ready(self):
        guild_count = 0

        for guild in client.guilds:
            logger.info(f'- {guild.id} (name: {guild.name})')
            guild_count = guild_count + 1

        logger.info('SampleDiscordBot is in ' + str(guild_count) + ' guilds.')

    async def on_message(self, message: discord.Message):
        if type(message.author) == User:
            if message.content.isdigit():
                user = db.find_by_discord_id(message.author.id)  # TODO: remove db
                uid = message.content

                if user:  # TODO: check if user already in channels
                    await message.author.send(
                        'You already sent a request. '
                        'Please wait up to 48 hours to approve your request.'
                    )
                else:
                    logger.info('Started processing ' + message.author.name +
                                ' with id: ' + str(message.author.id))

                    for admin_id in DISCORD_ADMINS:
                        admin = await client.fetch_user(admin_id)
                        await admin.send('**' + message.author.name + '**' +
                                         ' sent request to join to the ByBit '
                                         'chat!\n'
                                         'ByBit UID: ' + uid,
                                         view=Buttons(
                                             user=message.author,
                                             admin=admin
                                         ))

                    await message.author.send(
                        'Your request has been successfully created! '
                        'Please wait up to 48 hours to approve your request.'
                    )

                    logger.info(message.author.name +
                                ' (' + str(message.author.id) + ') ' +
                                'is successfully processed!')
            else:
                await message.author.send(
                    'Incorrect message! Please send your ByBit UID...'
                )


if __name__ == '__main__':
    intents = discord.Intents.all()
    client = MyClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)
