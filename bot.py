import logging

import discord

from settings import DISCORD_BOT_TOKEN, LOG_LEVEL

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=LOG_LEVEL)

bot = discord.Client()


@bot.event
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1

    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")


@bot.event
async def on_message(message):
    if message.author.dm_channel and \
            message.channel.id == message.author.dm_channel.id and \
            message.content.isdigit():
        channel = bot.get_channel(986624704158765079)
        invite_link = await channel.create_invite(max_uses=1, unique=True)
        await message.author.send(
            'You\'re successful approved and '
            'been invited to join ByBit server :white_check_mark: \n' +
            str(invite_link)
        )


bot.run(DISCORD_BOT_TOKEN)


# async def main():
#     await client.start()
#     if await client.is_user_authorized():
#         me = await client.get_me()
#         logger.info(f'Connected as {me.username} ({me.phone})')
#
#         await asyncio.gather(
#             check_useful_chats(),
#             client.run_until_disconnected()
#         )
#     else:
#         logger.error('Cannot be authorized')
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop().run_until_complete(main())
