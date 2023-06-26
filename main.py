import discord
from discord.ext import commands
import random
import re
from keep_alive import keep_alive
import os



my_secret = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True

otuzbir_words = ["otuzbir", "otuz bir", "3bir", "3 bir", "62/2", "uc ve bir", "uc bir", "ucbir", "uc bir", "3 1", "31"]
starter_words = ["sen galiba "]
end_words = ["seviyorsun", "bağımlısısın", "'i komik buluyorsun", "'e biraz gülüyorsun"]

bot = commands.Bot(command_prefix='$', intents=intents)

word_counts = {}

@bot.event
async def on_ready():
    print('Bot is ready.')

async def handle_31_message(message):
    user_name = str(message.author)
    await message.channel.send(
        random.choice(starter_words) + random.choice(otuzbir_words) + random.choice(end_words))
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg = message.content.lower()

    if any(word in msg for word in otuzbir_words):
        user_name = str(message.author)
        if not user_name.startswith("Bot"):
            await handle_31_message(message)
            increment_word_count(user_name)
            return  # İşlem tamamlandıktan sonra dön

    math_expression = re.findall(r'\d+[-+*/]\d+', msg)
    if math_expression:
        expression = re.sub(r'\s', '', math_expression[0])
        result = evaluate_expression(expression)
        if result == 31:
            await handle_31_message(message)
            return  # İşlem tamamlandıktan sonra dön

    await bot.process_commands(message)


def increment_word_count(user_name):
    if user_name in word_counts:
        word_counts[user_name] += 1
    else:
        word_counts[user_name] = 1


def evaluate_expression(expression):
    operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y
    }

    operator = re.findall(r'[-+*/]', expression)[0]
    operands = re.findall(r'\d+', expression)

    if operator in operators:
        return operators[operator](int(operands[0]), int(operands[1]))
    else:
        return None



@bot.command(name='count')
async def show_word_count(ctx):
    if ctx.author != bot.user:
        user_name = str(ctx.author)
        if user_name in word_counts:
            count = word_counts[user_name]
            await ctx.send(f"{user_name}, kullanıcı 'otuzbir' kelimesini {count} kez kullandı.")
        else:
            await ctx.send(f"{user_name}, kullanıcı 'otuzbir' kelimesini hiç kullanmadı.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def delete_message(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)

@delete_message.error
async def delete_message_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Yetkiniz yok.")


@bot.command()
async def server(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    join_time = member.joined_at
    current_time = ctx.message.created_at
    duration = current_time - join_time

    await ctx.send(f"{member.name}, bu sunucuda {duration.days} gün, {duration.seconds // 3600} saat ve {(duration.seconds // 60) % 60} dakika süredir bulunuyor.")

@bot.command()
async def selam(ctx, member: discord.Member):
    if member == bot.user:
        await ctx.send(f"{member.mention}, Bana selam demene gerek yok, ben zaten buradayım!")
    else:
        await ctx.send(f"{member.mention}, {ctx.author.mention} sana selam diyor!")


@bot.command()
async def secim(ctx):
    await ctx.send("Zaten AQ'p tarafından hayatımız sıkılmış, lütfen konuşmayalım.")


@bot.command()
async def komut(ctx):
    prefix = "$"  # Botunuzun komut ön eki
    embed = discord.Embed(title="Bot Komutları", description="İşte botun mevcut komutları:", color=discord.Color.blue())

    # Komutlar ve açıklamaları
    commands = [
        {"name": "count", "description": "Kullanıcının 'otuzbir' kelimesini kaç kez kullandığını gösterir."},
        {"name": "delete_message <amount>", "description": "Belirtilen miktarda mesajı siler."},
        {"name": "server [user]", "description": "Kullanıcının sunucuda ne kadar süredir bulunduğunu gösterir."},
        
        {"name": "selam <@kullanıcı>", "description": "Kullanıcıya selam mesajı gönderir."},
        {"name": "secim", "description": "Zaten AQ'p tarafından hayatımız sıkıldı mesajı gönderir."},
        {"name": "ahhhh", "description": "Hani nerde çorap? Ohhhh kalbim! mesajı gönderir."},
        # Eklemek istediğiniz diğer komutları buraya ekleyin
    ]

    for command in commands:
        embed.add_field(name=f"{prefix}{command['name']}", value=command['description'], inline=False)

    await ctx.send(embed=embed)
@bot.command()
async def ahhhh(ctx):
    await ctx.send("Hani nerde çorap? Ohhhh kalbim!")



keep_alive()
bot.run(os.getenv("TOKEN"))