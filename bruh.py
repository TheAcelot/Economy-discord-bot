import discord
import sqlite3
import random
import asyncio
from discord.ext import commands
from DataBase import * #DataBase manager
from config import creator, botID
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
token = '' #ваш токен // your token
if token == None or token == '':
	print('No token!\n')
prefix = '+' #ваш префикс // your prefix
bot = commands.Bot(command_prefix = prefix,  intents = discord.Intents.all())
bot.remove_command('help')

#lists
exp = []
#lists end

#create db
CreateDB("main", "name", "id", "money", "XP") #main
CreateShopDB() #shop
CreateBankDB()
@bot.event
async def on_ready():
	print(f"READY!\nNeeds help? {creator['CreatorDiscord']}")
@bot.event
async def on_message(msg):
	await bot.process_commands(msg) #it needs for commands
	cursor.execute(f"SELECT name FROM main where id={msg.author.id}")
	if cursor.fetchone() == None:
		InsertValues(msg.author, msg.author.id)
		print(f"{msg.author} has been registred!")
	else:
		if not msg.author.id == botID['id']:
			if not str(msg.author.id) in exp:
				xp_chanse = random.randint(1,4)
				if xp_chanse == 1:
					reward = random.randint(2,30)
					emb = discord.Embed(title= 'Новый опыт!',color=discord.Color.green())
					emb.add_field(name=f"Награда: {reward}",value=f"Через 30 секунд вы снова сможете его получить")
					UpdateValue('XP', reward, msg.author.id)
					await msg.channel.send(embed=emb)
					exp.append(str(msg.author.id))
					await asyncio.sleep(30)
					exp.remove(str(msg.author.id))
				else:
					pass
			else:
				pass
		else:
			pass
@bot.command()
async def help(ctx):
	emb = discord.Embed(title='HELP',colour=discord.Color.green())
	emb.add_field(name= 'ОСНОВНЫЕ:',value=f'{prefix}account - Аккаунт (также можно использовать {prefix}account @чел)\n{prefix}work - Работа\n{prefix}casino - Казино\n{prefix}shop - Магазин\n{prefix}replaceshop id roleID title cost - Замена предмета в магазине (если его нет, добавление)\n{prefix}buy id предмета - Покупка предмета\n{prefix}SetMoney @чел количество - Выдача денег пользователю\n{prefix}give @чел количество - Транзакция между 2 участниками')
	emb.add_field(name= 'ДЛЯ ОНВЕРА БОТА: ',value=f"{prefix}logout - выключить бота\n{prefix}clear количество - очистка сообщений\n{prefix}leave - ливает с сервера гле была заюзана команда")
	await ctx.send(embed=emb)
@bot.command() #account
async def account(ctx, member:discord.Member=None):
	if member == None:
		member = ctx.author
	emb = discord.Embed(title= 'ПРОФИЛЬ', colour=discord.Color.green())
	for row in cursor.execute(f"SELECT name,money,XP FROM main where id={member.id}"):
		emb.add_field(name='ОСНОВНАЯ ИНФА: ',value=f"Имя: {row[0]}\nМонеты: {row[1]}\nОпыт: {row[2]}")
		emb.set_footer(text= f"Used command: {ctx.author}", icon_url=ctx.message.author.avatar_url)
	await ctx.reply(embed=emb)
@bot.command()
async def delete(ctx, val=None):
	if val==None:
		await ctx.reply(f'Удалить аккаунт? Если да введите {prefix}delete y\nЕсли нет то введите: {prefix}delete n')
	elif val == 'y':
		DeleteAccount(ctx.author.id)
	elif val=='n':
		await ctx.send('Отменено!')
	else:
		pass
@bot.command()
async def work(ctx):
	emb = discord.Embed(title= 'РАБОТА', colour=discord.Color.green())
	revard = random.randint(1,120)
	try:
		UpdateValue('money', revard, ctx.author.id)
		emb.add_field(name= 'Ты работал и получил ',value= f"{revard} монет!")
		await ctx.reply(embed=emb)
	except:
		await ctx.send('Ошибка!')
@bot.command()
async def casino(ctx, money:int=None):
	emb = discord.Embed(title= 'КАЗИНО', colour=discord.Color.green())
	if money == None:
		await ctx.reply('Введите деньги')
	else:
		revard = "Win", "Lose"
		for row in cursor.execute(f"SELECT money FROM main where id={ctx.author.id}"):
			if row[0] <= money:
				await ctx.reply('Недостаточно ресурсов!')
			else:
				try:
					if random.choice(revard) == "Win":
						emb.add_field(name= "ВЫИГРЫШ", value= f"Вы получили {money*2} монет")
						UpdateValue('money', money*2, ctx.author.id)
					else:
						emb.add_field(name= 'ПРОИГРЫШ',value= f"Потеряли {money/2} монет")
						UpdateValue('money', money/2, ctx.author.id)
					await ctx.reply(embed=emb)
				except:
					await ctx.send('Ошибка!')
@bot.command()
async def leaderboard(ctx):
	for member in ctx.guild.members:
					for row in cursor.execute(f"SELECT name, money FROM main where id={member.id} ORDER BY money"):
						await ctx.reply(f"Имя: {row[0]}, Деньги: {row[1]}")
@bot.command()
async def shop(ctx, id:int=None):
	emb = discord.Embed(title= 'МАГАЗИН', colour=discord.Color.red())
	for row in cursor.execute(f"SELECT title,id,roleID,cost FROM shop"):
		emb.add_field(name=f'Название: {row[0]}\nID: {row[1]}',value=f"Роль: <@&{row[2]}>\nСтоимость: {row[3]}")
		await ctx.send(embed=emb)
@bot.command()
async def buy(ctx, id:int=None):
	for row in cursor.execute(f"SELECT title,roleID,cost FROM shop where id={id}"):
		for x in cursor.execute(f"SELECT money FROM main where id={ctx.author.id}"):
			if x[0] <= row[2]:
				await ctx.send('Не хватает денег!')
			else:
				try:
					role = discord.utils.get(ctx.guild.roles,id=row[1])
					new = x[0]-row[2]
					ReplaceValue('money', new, ctx.author.id)
					await ctx.author.add_roles(role)
					await ctx.reply('Вы купили роль!')
				except:
					await ctx.send('Ошибка!')
@bot.command()
@commands.is_owner()
async def replaceshop(ctx, id:int=None, roleID:int=None, title:str=None, cost:int=None):
	if id == None or roleID == None or title==None or cost == None:
		await ctx.reply(f'Использование: {prefix}addshop айди roleID название стоимость')
	else:
		cursor.execute(f"SELECT * FROM shop")
		if cursor.fetchone()==None:
			InsertShopValues('Hello!', 9339, 0, 1)
		else:
			ReplaceShopString('title', title)
			ReplaceShopValue('id', id)
			ReplaceShopString('roleID', roleID)
			ReplaceShopValue('cost', cost)
		await ctx.send('Added!')
@bot.command()
@commands.is_owner()
async def SetMoney(ctx, member:discord.Member=None, val:int=None):
	if member == None:
		await ctx.reply('Укажите юзера')
	else:
		if val == None:
			await ctx.reply('Укажите количество')
		else:
			UpdateValue('money', val, member.id)
			await ctx.reply(f"Вы дали **{member}** {val} монет!")
@bot.command()
async def give(ctx, member:discord.Member=None, val:int=None):
	emb = discord.Embed(title='ТРАНЗАКЦИЯ',colour=discord.Color.red())
	for row in cursor.execute(f"SELECT money FROM main where id={ctx.author.id}"):
		if val >= row[0]:
			await ctx.reply('Недостаточно средств.')
		else:
			emb.add_field(name= f"Вы перевели **{member}** {val} монет!",value=f"Но у вас стало меньше на {val} монет")
			UpdateValue('money', val, member.id)
			new = row[0]-val
			ReplaceValue('money', new, ctx.author.id)
			await ctx.send(embed=emb)
@bot.command()
async def bank(ctx, arg=None, val=None):
	cursor.execute(f"SELECT * FROM bank where id={ctx.author.id}")
	if cursor.fetchone()==None:
		InsertBankValues(ctx.author.id)
	else:
		if arg == None:
			for row in cursor.execute(f"SELECT money FROM bank where id={ctx.author.id}"):
				await ctx.reply(f"У вас {row[0]} монет в банке\nЧто положить/снять введите {prefix}bank положить количество/{prefix}bank снять количество")
		elif arg == 'снять':
			for row in cursor.execute(f"SELECT money FROM main where id={ctx.author.id}"):
				for b in cursor.execute(f"SELECT money FROM bank where id={ctx.author.id}"):
					if int(val) >= b[0]:
						await ctx.reply('Недостаточнг средств')
					else:
						UpdateValue('money', int(val), ctx.author.id)
						new = b[0]-int(val)
						ReplaceBankValue(new, ctx.author.id)
						await ctx.reply('Успешно')
		elif arg == 'положить':
			for row in cursor.execute(f"SELECT money FROM main where id={ctx.author.id}"):
				for b in cursor.execute(f"SELECT * FROM bank where id={ctx.author.id}"):
					if int(val) >= row[0]:
						await ctx.reply('Недостаточно средств')
					else:
						UpdateBankValue(int(val), ctx.author.id)
						new = row[0]-int(val)
						ReplaceValue('money', new, ctx.author.id)
						await ctx.reply('Успешно')
#---------------------#
#Reaction Factory#
@bot.event
async def on_reaction_add(payload):
        if payload.emoji.name == 'tada':
        	print('bruh')
#--------------------#
#==for admin==#
#---------------------#
@bot.command() #logout
@commands.is_owner()
async def logout(ctx):
	await ctx.bot.logout()
	emb = discord.Embed(title= 'УСПЕШНО',colour=discord.Color.green())
	emb.add_field(name= 'Loggining out...',value=f"...")
	await ctx.send(embed=emb)
@bot.command() #leave from guild
@commands.is_owner()
async def leave(ctx):
	await ctx.guild.leave()
@bot.command() #clear messages
@commands.is_owner()
async def clear(ctx, count:int=None):
	if count == None:
		emb = discord.Embed(title= 'ОШИБКА',colour=discord.Color.red())
		emb.add_field(name= 'Пример:',value=f"{prefix}clear 5")
	else:
		await ctx.channel.purge(limit=count+1)
		emb = discord.Embed(title= 'УСПЕШНО',colour=discord.Color.green())
		emb.add_field(name= 'Я ОЧИСТИЛ',value=f"{count} сообщений!")
	await ctx.send(embed=emb)
#bot login#
try:
	bot.run(token) #run bot
except:
	print("bruh")