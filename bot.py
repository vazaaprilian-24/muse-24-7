import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix='L!', intents=intents)
loop_enabled = False

@bot.command()
async def volume(ctx, vol: int):
    if ctx.voice_client and ctx.voice_client.source:
        ctx.voice_client.source.volume = vol / 100
        await ctx.send(f"Volume set to {vol}%")
        
@bot.command()
async def join(ctx):
    # Cek apakah user ada di voice channel
    if not ctx.author.voice:
        await ctx.send("You Must in Voice Channel to Operate the Command.")
        return

    channel = ctx.author.voice.channel

    # Kalau bot sudah connect
    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
        await ctx.send(f"Moved to {channel.name}")
    else:
        await channel.connect()
        await ctx.send(f"Joining ke {channel.name}")

@bot.command()
async def play(ctx):
    global loop_enabled

    if not ctx.author.voice:
        await ctx.send("Enter Voice Channel First.")
        return

    channel = ctx.author.voice.channel

    if not ctx.voice_client:
        voice_client = await channel.connect()
    else:
        voice_client = ctx.voice_client

    def repeat(error):
        if loop_enabled:
            source = discord.FFmpegPCMAudio("song.mp3")
            source = discord.PCMVolumeTransformer(source, volume=0.5)
            voice_client.play(source, after=repeat)

    source = discord.FFmpegPCMAudio("song.mp3")
    source = discord.PCMVolumeTransformer(source, volume=0.5)

    voice_client.play(source, after=repeat)
    await ctx.send("Starting Lany Setlist 1 Hours 🎵")

@bot.command()
async def loop(ctx, mode: str):
    global loop_enabled

    if mode.lower() == "on":
        loop_enabled = True
        await ctx.send("Loop On.")
    elif mode.lower() == "off":
        loop_enabled = False
        await ctx.send("Loop Off.")
    else:
        await ctx.send("Gunakan: !loop on / !loop off")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Music on Pause ⏸")
    else:
        await ctx.send("No Music on the Queue.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resuming Music ▶")
    else:
        await ctx.send("Music tidak sedang di-pause.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("I'm Leaving The Vocie Channel.")
    else:
        await ctx.send("I'm not on the Voice Channel.")

@bot.event
async def on_ready():
    print('Bot is ready.')

    activity = discord.Activity(
        type=discord.ActivityType.listening,
        name="L!play"
    )

    await bot.change_presence(activity=activity)

bot.run(os.getenv("TOKEN"))
