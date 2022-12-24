from cryptography.fernet import Fernet
import json
import os

key = os.getenv('DECRYPTED_KEY')
fernet = Fernet(key)

def Encryption(update, context):
	userId = update.effective_user.id
	if userId == int(os.getenv('DEV_ID')):
		file = open('Test/decrypted.json', 'rb')
		original = file.read()
		encrypted = fernet.encrypt(original)
		with open('Test/encrypted.txt', 'wb') as encryptedFile:
			encryptedFile.write(encrypted)
		update.effective_message.reply_text('Encryption has done!')
	else:
		update.effective_message.reply_text('Only dev can use this command.')

def Decryption(update, context):
	userId = update.effective_user.id
	if userId == int(os.getenv('DEV_ID')):
		encryptedFile = open('Test/encrypted.txt', 'rb')
		encrypted = encryptedFile.read()
		decrypted = fernet.decrypt(encrypted)
		with open('Test/decrypted.json', 'w') as decryptedFile:
			json.dump(json.loads(decrypted), decryptedFile, indent=2)
		update.effective_message.reply_text('Decryption has done!')
	else:
		update.effective_message.reply_text('Only dev can use this command.')

def Clean(update, context):
	userId = update.effective_user.id
	if userId == int(os.getenv('DEV_ID')):
		if len(context.args) > 0:
			if int(context.args[0]) == 0:
				open('Test/decrypted.json', 'w')
			elif int(context.args[0]) == 1:
				open('Test/encrypted.txt', 'w')
			update.effective_message.reply_text('File cleaned!')
		else:
			update.effective_message.reply_text('/clean [0/1]')
	else:
		update.effective_message.reply_text('Only dev can use this command.')