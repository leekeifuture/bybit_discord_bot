import logging

import discord
from discord import User

from settings import DISCORD_BOT_TOKEN, LOG_LEVEL, DISCORD_GUILD_ID, \
    DISCORD_ADMINS, DISCORD_CHANNELS_ID

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=LOG_LEVEL)


def is_user_in_all_private_channels(user):
    for channel_id in DISCORD_CHANNELS_ID:
        channel_members = client \
            .get_guild(DISCORD_GUILD_ID) \
            .get_channel(int(channel_id)) \
            .members
        channel_members_id = list(
            map(lambda member: member.id, channel_members)
        )
        if user.id not in channel_members_id:
            return False
    return True


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180, user=None, admin=None):
        super().__init__(timeout=timeout)
        self.user = user
        self.admin = admin

    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def green_button(self, interaction: discord.Interaction,
                           button: discord.ui.Button):
        invite_content = ''
        for channel_id in DISCORD_CHANNELS_ID:
            channel = client \
                .get_guild(DISCORD_GUILD_ID) \
                .get_channel(int(channel_id))
            invite_link = await channel.create_invite(max_uses=1, unique=True)
            invite_text = '\n**' + channel.name + '**:\n' + str(invite_link)
            invite_content += invite_text

        await self.user.send(
            'You\'re successful approved and '
            'been invited to join private channels :white_check_mark:\n' +
            invite_content
        )

        self.green_button.disabled = True
        self.red_button.disabled = True
        await interaction.response.edit_message(
            content=self.user.name + ' has been successfully approved and '
                                     'invited to the private channels!',
            view=self
        )

        logger.info(self.user.name + ' has been approved by ' + self.admin.name)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def red_button(self, interaction: discord.Interaction,
                         button: discord.ui.Button):
        await self.user.send(
            'You was denied to join to the private channels :cry:')

        self.green_button.disabled = True
        self.red_button.disabled = True
        await interaction.response.edit_message(
            content=self.user.name + ' has been successfully denied!',
            view=self
        )

        logger.info(self.user.name + ' has been denied by ' + self.admin.name)


class MyClient(discord.Client):
    @staticmethod
    async def on_ready():
        guild_count = 0

        for guild in client.guilds:
            logger.info(f'- {guild.id} (name: {guild.name})')
            guild_count = guild_count + 1

        logger.info('SampleDiscordBot is in ' + str(guild_count) + ' guilds.')

    @staticmethod
    async def on_message(message: discord.Message):
        if type(message.author) == User:
            if is_user_in_all_private_channels(message.author):
                await message.channel.typing()
                await message.author.send(
                    'You already consist in the private channels! '
                    ':white_check_mark:'
                )
            elif message.content.isdigit():
                logger.info('Started processing ' + message.author.name +
                            ' with id: ' + str(message.author.id))
                await message.channel.typing()

                uid = message.content

                for admin_id in DISCORD_ADMINS:
                    admin = await client.fetch_user(admin_id)
                    await admin.send('**' + message.author.name + '**' +
                                     ' sent request to join to '
                                     'the private channels!\n'
                                     'ByBit UID: ' + uid,
                                     view=Buttons(
                                         user=message.author,
                                         admin=admin
                                     ))

                await message.author.send(
                    'Your request has been successfully created! '
                    'Please wait up to 48 hours to approve your request '
                    ':timer:'
                )

                logger.info(message.author.name +
                            ' (' + str(message.author.id) + ') ' +
                            'is successfully processed!')
            else:
                await message.channel.typing()
                await message.author.send(
                    'Incorrect message! Please send your ByBit UID...'
                )


if __name__ == '__main__':
    intents = discord.Intents.all()
    client = MyClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)
