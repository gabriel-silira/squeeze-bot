import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from datetime import datetime
import random
from piadas import piadas_p

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Squeeze online como {bot.user}")

@bot.command()
async def dev(ctx):
    await ctx.send("feito por SLRDev, discord: **oliveira__.**")

@bot.command()
async def squeeze(ctx):
    await ctx.send("fala")

@bot.command()
async def ping(ctx):
    ping = round(bot.latency * 1000)
    await ctx.send(f"pong **{ping}ms**")

@bot.command()
async def data(ctx):
    data = datetime.now().strftime("%d/%m/%Y")
    await ctx.send(f"hoje é dia {data}")

@bot.command()
async def hora(ctx):
    hora = datetime.now().strftime("%H:%M:%S")
    await ctx.send(f"agora são {hora}")

@bot.command()
async def moeda(ctx):
    cara_coroa = ["cara", "coroa"]
    await ctx.send(random.choice(cara_coroa))

@bot.command()
async def d6(ctx):
    dado_d6 = random.randint(1, 6)
    await ctx.send(f"o dado caiu no {dado_d6}")

@bot.command()
async def d20(ctx):
    dado_d20 = random.randint(1, 20)
    await ctx.send(f"o dado caiu no {dado_d20}")

@bot.command()
async def d100(ctx):
    dado_d100 = random.randint(1, 100)
    await ctx.send(f"o dado caiu no {dado_d100}")

@bot.command()
async def piada(ctx):
    await ctx.send("carrascosa")

@bot.command()
async def piadas(ctx):
    piada = random.choice(piadas_p)
    await ctx.send(piada)

@bot.command()
async def help(ctx):
    comandosmod = [
        "**ban:** bane um usuário (_.ban @usuário 5min_)",
        "**expulsar:** expulsa um usuário (_.expulsar @usuário 5min_)",
        "**castigo:** castiga um usuário (_.castigo @usuário 5min_)",
    ]

    comandosdiv = [
        "**squeeze:** uma saudação",
        "**moeda:** tira cara ou coroa",
        "**d6:** rola um dado de 6 lados",
        "**d20:** rola um dado de 20 lados",
        "**d100:** rola um dado de 100 lados",
        "**piadas:** envia uma piada aleatória",
    ]

    comandosinfo = [
        "**dev:** mostra o criador do bot",
        "**servidores:** em quantos servidores o bot está",
        "**info:** informação aleátoria sobre o bot",
        "**ping:** devolve o ping do bot",
        "**data:** a data atual (GMT-3)",
        "**hora:** a hora atual (GMT-3)",
    ]

    listamod = "\n".join(f"- {c}" for c in comandosmod)
    listadiv = "\n".join(f"- {c}" for c in comandosdiv)
    listainfo = "\n".join(f"- {c}" for c in comandosinfo)

    embedm = discord.Embed(
        title='Comandos de Moderação | Prefixo = "."',
        description=listamod,
        color=discord.Color.blue()
    )

    embedd = discord.Embed(
        title='Comandos de Diversão | Prefixo = "."',
        description=listadiv,
        color=discord.Color.blue()
    )

    embedi = discord.Embed(
        title='Comandos de Informação | Prefixo = "."',
        description=listainfo,
        color=discord.Color.blue()
    )

    await ctx.send(embeds=[embedm, embedd, embedi])

bot.run(TOKEN)