from telegram.ext import Updater, CommandHandler
from alive import alive
import os
from birthday import Search, Day, Month, Remind, Test
from debug import Decryption, Encryption, Clean

commands = {}

def Help(update, context):
	userId = update.effective_user.id
	new = {a:[commands[a][b]['name'] for b in range(len(commands[a])) if not commands[a][b]['dev'] or commands[a][b]['dev'] and userId == int(os.getenv('DEV_ID'))] for a in commands}
	update.effective_message.reply_text(''.join([', '.join([f"/{new[a][b]}" for b in range(len(new[a]))]) + f' - {a}\n' for a in new]))

def Credits(update, context):
	update.effective_message.reply_text(
	"""
	Credits:
	This bot was made by @BenjaminThio
	This bot project started in 3/9/2021 and ended in 4/9/2022
	Language used: Python
	Source Code: https://replit.com/@BenjaminThio/Lasma-Birthday-Reminders#main.py
	Company's Name: LASMA STUDIO
	"""
	)

def main():
	alive()
	updater = Updater(os.getenv('TOKEN'))
	addHandler = updater.dispatcher.add_handler
	def addCommand(name, description, function, dev, args=None):
		if description not in commands:
			if args == None:
				commands[description] = [{'name': name, 'dev': dev}]
			else:
				commands[description] = [{'name': '{} {}'.format(name, ' '.join([f'[{i}]' for i in args])), 'dev': dev}]
		else:
			commands[description].append({'name': name, 'dev': dev})
		addHandler(CommandHandler(name, function))
	updater.job_queue.run_repeating(Remind, 1)
	addCommand('start', 'To get all commands info', Help, False)
	addCommand('help', 'To get all commands info', Help, False)
	addCommand("credits", "Credits and special thanks", Credits, False)
	addCommand('search', 'To Search someone for info', Search, False, ['Name'])
	addCommand('day', "To get all persons' birthday in the day", Day, False, ['Number'])
	addCommand('month', "To get all persons' birthday in the month", Month, False, ['Number/Text'])
	addCommand('decrypt', "For developer's debug purpose", Decryption, True)
	addCommand('encrypt', "For developer's debug purpose", Encryption, True)
	addCommand('clean', "For developer's debug purpose", Clean, True, ['0/1'])
	addCommand('test', "For developer's debug purpose", Test, True)
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()