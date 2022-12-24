from cryptography.fernet import Fernet
from datetime import datetime
import pytz
import json
import os

key = os.getenv('DECRYPTED_KEY')
fernet = Fernet(key)
length = 10

def ConvertClients():
	new = {}
	for fileName in os.listdir('Encrypted/Batches'):
		data = Decryption(f'Encrypted/Batches/{fileName}')
		for a in data:
			for b in data[a]:
				new[b['name']] = {
					'birthday': ''.join(list(a)[:-5]),
					'className': b['className']
				}
	return new

def Decryption(fileName):
	encryptedFile = open(fileName, 'rb')
	encrypted = encryptedFile.read()
	decrypted = fernet.decrypt(encrypted)
	return json.loads(decrypted)

def Encryption(data):
	original = json.dumps(data).encode('utf-8')
	encrypted = fernet.encrypt(original)
	return encrypted

def Search(update, context):
	data = ConvertClients()
	if len(context.args) > 0:
		query = ' '.join([i for i in context.args])
		if len(query) <= MaxNameLength():
			possibilities = [i for i in data if query in i]
			if len(possibilities) > 0:
				grouping = [possibilities[i:i+length] for i in range(0, len(possibilities), length)]
				for group in range(len(grouping)):
					update.effective_message.reply_text(f'Search result for `{query}`\nGroup {group + 1}\n' + ''.join([f'{index + 1}. {grouping[group][index].title()} - {data[grouping[group][index]]["birthday"]}\n' for index in range(len(grouping[group]))]))
			else:
				update.effective_message.reply_text(f'Search result for `{query}` not found.')
		else:
			update.effective_message.reply_text(f'The query you search should be less than `{MaxNameLength()}` letters.')
	else:
		update.effective_message.reply_text('/search [Name]')

def MaxNameLength():
	data = ConvertClients()
	max = 0
	for name in data:
		if len(name) > max:
			max = len(name)
	return max

def Day(update, context):
	data = ConvertClients()
	validDays = 31
	ordinalNumberSuffix = ['st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'st']
	alert = f'/day [Number]\nNumber given should be more than 0 and less than {validDays}.'
	if len(context.args) > 0:
		query = context.args[0].lower()
		if query.isdigit():
			if int(query) > 0 and int(query) <= validDays:
				result = DayFinder(query)
				for group in range(len(result)):
					update.effective_message.reply_text(f'Birthday in `{query}{ordinalNumberSuffix[int(query) - 1]}`\nGroup {group + 1}\n' + ''.join([f'{index + 1}. {result[group][index].title()} - {data[result[group][index].lower()]["birthday"]}\n' for index in range(len(result[group]))]))
			else:
				update.effective_message.reply_text(alert)
		else:
			update.effective_message.reply_text(alert)
	else:
		update.effective_message.reply_text(alert)

def Month(update, context):
	data = ConvertClients()
	monthsName = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
	alert = f'/month [Number/Text]\n`Integer`\nNumber given for query should be in between 1 to {len(monthsName)}.\n\n`String`\nAvailable months for text query:\n' + ''.join([f'{i + 1}. {monthsName[i].title()}\n' for i in range(len(monthsName))])
	if len(context.args) > 0:
		query = context.args[0].lower()
		if query.isdigit():
			if int(query) > 0 and int(query) <= len(monthsName):
				result = MonthFinder(query)
				for group in range(len(result)):
					update.effective_message.reply_text(f'Birthday in `{monthsName[int(query) - 1].title()}`\nGroup {group + 1}\n' + ''.join([f'{index + 1}. {result[group][index].title()} - {data[result[group][index].lower()]["birthday"]}\n' for index in range(len(result[group]))]))
			else:
				update.effective_message.reply_text(alert)
		elif query in monthsName:
			result = MonthFinder(monthsName.index(query) + 1)
			for group in range(len(result)):
				update.effective_message.reply_text(f'Birthday in `{monthsName[monthsName.index(query)].title()}`\nGroup {group + 1}\n' + ''.join([f'{index + 1}. {result[group][index].title()} - {data[result[group][index].lower()]["birthday"]}\n' for index in range(len(result[group]))]))
		else:
			update.effective_message.reply_text(alert)
	else:
		update.effective_message.reply_text(alert)

def MonthFinder(month):
	format = ['0', '0']
	for i in range(len(str(month))):
		format[-(i + 1)] = list(str(month))[-(i + 1)]
	for a in os.listdir('Encrypted/Batches'):
		data = Decryption(f'Encrypted/Batches/{a}')
		names = [c['name'] for b in data if b.split('/')[1] == ''.join(format) for c in data[b]]
		grouping = [names[i:i+length] for i in range(0, len(names), length)]
		return grouping

def DayFinder(day):
	format = ['0', '0']
	for i in range(len(str(day))):
		format[-(i + 1)] = list(str(day))[-(i + 1)]
	for a in os.listdir('Encrypted/Batches'):
		data = Decryption(f'Encrypted/Batches/{a}')
		names = [c['name'] for b in data if b.split('/')[0] == ''.join(format) for c in data[b]]
		grouping = [names[i:i+length] for i in range(0, len(names), length)]
		return grouping

def Remind(context):
	for fileName in os.listdir('Encrypted/Batches'):
		data = Decryption(f'Encrypted/Batches/{fileName}')
		chatId = -1001690280022
		today = datetime.now().astimezone(pytz.timezone('asia/kuala_lumpur')).strftime('%d/%m/%Y')
		seperate = today.split('/')
		year = seperate[2]
		if today in data:
			names = [i['name'] for i in data[today]]
			if os.getenv('HIDDEN') in names:
				message = context.bot.send_message(chat_id=os.getenv('DEV_ID'), text=f"Today is {os.getenv('HIDDEN')}'s birthday!")
				context.bot.pin_chat_message(
    chat_id=os.getenv('DEV_ID'), message_id=message.message_id)
				names.remove(os.getenv("HIDDEN"))
			if len(names) > 0:
				figures = ', '.join(names).title()
				context.bot.send_message(chat_id=chatId, text=f"Today is {figures}'s birthday!")
			data[f'{today[:-len(year)]}{int(year) + 1}'] = data.pop(today)
			with open(f'Encrypted/Batches/{fileName}', 'wb') as encryptedFile: encryptedFile.write(Encryption(data))

def Test(update, context):
	pass