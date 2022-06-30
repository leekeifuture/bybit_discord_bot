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
        guild = client.get_guild(DISCORD_GUILD_ID)
        channel = guild.get_channel(int(channel_id))
        if not channel:
            continue
        channel_members = channel.members

        channel_members_id = list(
            map(lambda member: member.id, channel_members)
        )
        if user.id not in channel_members_id:
            return False
    return True


def is_admin(user_id):
    return True if user_id in DISCORD_ADMINS else False


async def approve_user(admin, user):
    channels_been_added = ''
    for channel_id in DISCORD_CHANNELS_ID:
        guild = client.get_guild(DISCORD_GUILD_ID)
        channel = guild.get_channel(int(channel_id))

        channel_members_id = list(
            map(lambda member: member.id, channel.members)
        )
        if user.id not in channel_members_id:
            await channel.set_permissions(
                guild.get_member(user.id),
                send_messages=True,
                read_messages=True,
                connect=True
            )

            channels_been_added += '- **' + channel.name + '**\n'

    await user.send(
        'You\'re successful approved and '
        'been added to the private channels :white_check_mark:\n' +
        'Added to:\n' +
        channels_been_added
    )

    await admin.send(user.name + ' has been successfully approved and '
                                 'added to the private channels!')

    logger.info(user.name + ' has been approved by ' +
                admin.name + ' and added to channels:\n' +
                channels_been_added)


async def deny_user(admin, user):
    await user.send(
        'You was denied to join to the private channels :cry:'
    )

    await admin.send(user.name + ' has been successfully denied!')

    logger.info(user.name + ' has been denied by ' + admin.name)


class MyClient(discord.Client):
    @staticmethod
    async def on_ready():
        logger.info('---------------------------------------------------------')
        guild_count = 0

        logger.info('Connected guilds:')
        for guild in client.guilds:
            logger.info(f'- {guild.name} (ID: {guild.id})')
            for channel in guild.channels:
                logger.info(f' |---- {channel.name} (ID: {channel.id}):')

            guild_count = guild_count + 1

        logger.info('SampleDiscordBot is in ' + str(guild_count) + ' guilds.')

    @staticmethod
    async def on_member_join(member):
        if member.guild.id == DISCORD_GUILD_ID and \
                not is_user_in_all_private_channels(member):
            await member.send(
                'Welcome! I\'m here to help you get access to ByBit '
                'private channels. Just send me your UID from ByBit '
                'affiliates and wait a bit when someone from admins '
                'approves your request :fingers_crossed:'
            )

    @staticmethod
    async def on_message(message: discord.Message):
        if type(message.author) == User and \
                DISCORD_GUILD_ID in \
                list(map(lambda guild: guild.id, message.author.mutual_guilds)):
            if is_admin(message.author.id):
                if message.content.lower() == 'yes' or \
                        message.content.lower() == 'no':
                    await message.channel.typing()

                    if message.reference:
                        user = None
                        if 'Discord ID: ' in message.reference.resolved.content:
                            user_id = message.reference.resolved \
                                .content.split('Discord ID: ')[-1]
                            user = await client.fetch_user(int(user_id))
                        else:
                            members = client.get_guild(DISCORD_GUILD_ID).members
                            for member in members:
                                user_name = message.reference.resolved.content \
                                                .split(
                                    '** sent request to join')[0][2:]
                                if member.name == user_name:
                                    user = member

                        if message.content.lower() == 'yes':
                            await approve_user(message.author, user)
                        elif message.content.lower() == 'no':
                            await deny_user(message.author, user)
                    else:
                        await message.author.send(
                            'Please make a reference to message '
                            'where bot asks to approve!'
                        )
                else:
                    await message.author.send('Wrong command!')
            elif is_user_in_all_private_channels(message.author):
                await message.channel.typing()
                await message.author.send(
                    'You already consist in the all needed channels! '
                    ':white_check_mark:'
                )
            elif message.content.isdigit():
                await message.channel.typing()

                uid = message.content

                logger.info('Started processing ' + message.author.name +
                            ' with id: ' + str(message.author.id) +
                            ' and uid: ' + str(uid))

                for admin_id in DISCORD_ADMINS:
                    admin = await client.fetch_user(admin_id)
                    await admin.send(f'**{message.author.name}** '
                                     'sent request to join to '
                                     'the private channels!\n'
                                     f'ByBit UID: {uid}\n'
                                     f'Discord ID: {str(message.author.id)}')

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
