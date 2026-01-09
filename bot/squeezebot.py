import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv
import os
from datetime import datetime
import random
from piadas import piadas_p
from infos import infos_b

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

@bot.event
async def on_ready():
    SCommands = await bot.tree.sync()
    print(f"Squeeze online como {bot.user}")
    print(f"{len(SCommands)} comandos sincronizados")

    allcomm = input("Deseja ver os comandos sincronizados? ")
    if allcomm == "true":
        for commands in SCommands:
            print(f"Comando - /{commands.name}")

# comandos de moderação
@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *, reason="Não especificado"):
    if member == ctx.author:
        await ctx.send("Você não pode se banir")
        return
    if member == bot.user:
        await ctx.send("Você não pode me banir")
        return
    try:
        await member.ban(reason=reason)
        embedb = discord.Embed(
            title="Banimento Aplicado",
            description=f"O usuário {member.mention} foi banido",
            color=discord.Color.blue()
        )
        embedb.add_field(name="Motivo", value=reason)
        embedb.set_footer(text=f"Aplicado por {ctx.author.display_name}")
        await ctx.send(embed=embedb)
    except discord.Forbidden:
        await ctx.send(f"Não tenho permissão para banir {member.mention}.")
    except Exception as erro:
        await ctx.send(f"Ocorreu um erro: {erro}")

@bot.command(name='unban')
@has_permissions(ban_members=True)
async def unban(ctx, user:discord.User, *, reason="Não especificado"):
    try:
        await ctx.guild.unban(user, reason=reason)
        embedub = discord.Embed(
            title="Banimento Removido",
            description=f"O usuário {user.mention} foi desbanido",
            color=discord.Color.blue()
        )
        embedub.add_field(name="Motivo", value=reason)
        embedub.set_footer(text=f"Aplicado por {ctx.author.display_name}")
        await ctx.send(embed=embedub)
    except discord.NotFound:
        await ctx.send(f"Não foi possível encontrar o banimento de {user.mention}")
    except MissingPermissions:
        await ctx.send("Você não tem permissão para desbanir usuários")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {e}")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member, *, reason="Não especificado"):
    if member == ctx.author:
        await ctx.send("Você não pode se expulsar")
        return
    if member == bot.user:
        await ctx.send("Você não pode me expulsar")
        return
    try:
        await member.kick(reason=reason)
        embedk = discord.Embed(
            title="Expulsão Aplicada",
            description=f"O usuário {member.mention} foi expulso",
            color=discord.Color.blue()
        )
        embedk.add_field(name="Motivo", value=reason)
        embedk.set_footer(text=f"Aplicado por {ctx.author.display_name}")
        await ctx.send(embed=embedk)
    except discord.Forbidden:
        await ctx.send(f"Não tenho permissão para expulsar {member.mention}.")
    except Exception as erro:
        await ctx.send(f"Ocorreu um erro: {erro}")

@bot.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, time: int, *, reason="Não especificado"):
    if time > 43200:
        return await ctx.send("O tempo máximo de castigo é de 30 dias (43200 minutos)")
    if member == ctx.author:
        return await ctx.send("Você não pode se dar timeout")
    if member == bot.user:
        return await ctx.send("Você não pode me dar timeout")
    try:
        if time == 0:
            await member.timeout(None, reason=reason)
            embed = discord.Embed(
                title="Timeout Removido",
                description=f"O usuário {member.mention} saiu do timeout",
                color=discord.Color.blue()
            )
            embed.add_field(name="Motivo", value=reason)
            embed.set_footer(text=f"Aplicado por {ctx.author.display_name}")
            return await ctx.send(embed=embed)
        else:
            duracao = datetime.timedelta(minutes=time)
            await member.timeout(duracao, reason=reason)
            embed = discord.Embed(
                title="Timeout Aplicado",
                description=f"O usuário {member.mention} tomou timeout",
                color=discord.Color.blue()
            )
            embed.add_field(name="Duração", value=f"{time} minutos")
            embed.add_field(name="Motivo", value=reason)
            embed.set_footer(text=f"Aplicado por {ctx.author.display_name}")
            await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send(f"Não tenho permissão para dar timeout em {member.mention}")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro: {e}")

# comandos de entretenimento
@bot.tree.command(description="Envia uma saudação")
async def squeeze(interact:discord.Integration):
    await interact.response.send_message(f"Olá, {interact.user.display_name}")

@bot.tree.command(description="Cara ou Coroa")
async def moeda(interact:discord.Integration):
    listacc = ["Cara", "Coroa"]
    cara_coroa = random.choice(listacc)
    await interact.response.send_message(cara_coroa)

@bot.tree.command(description="Rola um dado de 6 lados")
async def d6(interact:discord.Integration):
    dado_d6 = random.randint(1, 7)
    await interact.response.send_message(f"O dado caiu em {dado_d6}")

@bot.tree.command(description="Rola um dado de 20 lados")
async def d20(interact:discord.Integration):
    dado_d20 = random.randint(1, 21)
    await interact.response.send_message(f"O dado caiu em {dado_d20}")

@bot.tree.command(description="Rola um dado de 100 lados")
async def d100(interact:discord.Integration):
    dado_d100 = random.randint(1, 101)
    await interact.response.send_message(f"O dado caiu em {dado_d100}")

@bot.command(description="carrascosa")
async def piada(ctx):
    await ctx.send("carrascosa")

@bot.tree.command(description="Envia uma piada aleatória de uma lista com 501")
async def piadas(interact:discord.Integration):
    piada = random.choice(piadas_p)
    await interact.response.send_message(piada)

#infocommand

# comandos de informação
@bot.tree.command(description="Quem fez o bot")
async def dev(interact:discord.Integration):
    await interact.response.send_message("Feito por SLRDev, discord: **oliveira__.**")

@bot.tree.command(description="Envia o ping")
async def ping(interact:discord.Integration):
    ping = round(bot.latency * 1000)
    await interact.response.send_message(f"Pong: **{ping}ms**")

@bot.tree.command(description="Envia a data atual")
async def data(interact:discord.Integration):
    data = datetime.now().strftime("%d/%m/%Y")
    await interact.response.send_message(f"Hoje é dia {data}")

@bot.tree.command(description="Envia a hora atual")
async def hora(interact:discord.Integration):
    hora = datetime.now().strftime("%H:%M:%S")
    await interact.response.send_message(f"O horário atual é {hora}")

@bot.tree.command(description="Envia uma informação aleatória sobre o bot")
async def infos(interact:discord.Integration):
    info = random.choice(infos_b)
    await interact.response.send_message(info)

@bot.tree.command(description="Envia a Embed de help com os comandos do bot")
async def help(interact:discord.Integration):
    comandosmod = [
        "**ban:** Bane um usuário (_/ban @usuário motivo_)",
        "**kick:** Expulsa um usuário (_/kick @usuário motivo_)",
        "**timeout:** Castiga um usuário (_/timeout @usuário 5 motivo_)",
    ]

    comandosdiv = [
        "**squeeze:**Envia uma saudação",
        "**moeda:** Tira um cara ou coroa",
        "**d6:** Rola um dado de 6 lados",
        "**d20:** Rola um dado de 20 lados",
        "**d100:** Rola um dado de 100 lados",
        "**piadas:** Envia uma piada aleatória",
    ]

    comandosinfo = [
        "**dev:** Mostra o criador do bot",
        "**servidores:** Em quantos servidores o bot está",
        "**info:** Informação aleátoria sobre o bot",
        "**ping:** Devolve o ping do bot",
        "**data:** A data atual (GMT-3)",
        "**hora:** A hora atual (GMT-3)",
    ]

    listamod = "\n".join(f"- {c}" for c in comandosmod)
    listadiv = "\n".join(f"- {c}" for c in comandosdiv)
    listainfo = "\n".join(f"- {c}" for c in comandosinfo)

    embedm = discord.Embed(
        title='Comandos de Moderação | Prefixo = "/"',
        description=listamod,
        color=discord.Color.blue()
    )

    embedd = discord.Embed(
        title='Comandos de Diversão | Prefixo = "/"',
        description=listadiv,
        color=discord.Color.blue()
    )

    embedi = discord.Embed(
        title='Comandos de Informação | Prefixo = "/"',
        description=listainfo,
        color=discord.Color.blue()
    )

    await interact.response.send_message(embeds=[embedm, embedd, embedi])

# comandos de música

bot.run(TOKEN)