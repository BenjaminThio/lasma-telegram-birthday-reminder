import json
from datetime import date, datetime

file = open('birthday.json', 'r')
data = json.load(file)
new = {}

def Reformat():
    for i in data:
        name = data[i]['name'].title()
        birthday = data[i]['birthday'].split('-')
        day = int(birthday[1])
        month = int(birthday[0])
        year = date.today().year
        customDate = datetime(year, month, day)
        now = datetime.now()
        if customDate < now:
            year += 1
        reformattedBirthday = datetime(year, month, day).strftime("%d/%m/%Y")
        className = data[i]['tkt']
        if reformattedBirthday not in new:
            new[reformattedBirthday] = [
                {
                    'name': name,
                    'className': className
                }
            ]
        elif reformattedBirthday in new:
            new[reformattedBirthday].append(
                {
                    'name': name,
                    'className': className
                }
            )
    with open("clients.json", "w") as jfile: json.dump(new, jfile, indent=2)

def Clear():
    with open("clients.json", "w") as jfile: json.dump(new, jfile, indent=2)

def GetLen():
    print(('abc')[:-1])
    counter = 0
    for a in new:
        counter += len(new[a])
    print(counter)

def Reformat2():
	with open('JSON/Info/clients.json', 'r') as file: data = json.load(file)
	new = {}
	for i in data:
		new[i.lower()] = {
			'birthday': data[i]['birthday'].replace('-', '/') + '/2005',
			'className': data[i]['tkt']
		}
	with open('JSON/Info/clients.json', 'w') as jfile: json.dump(new, jfile, indent=2)

def Reformat3():
	with open('JSON/Info/clients.json', 'r') as file: data = json.load(file)
	new = {}
	for i in data:
		new[i.lower()] = {
			'birthday': data[i]['birthday'].split('-')[1] + '/' + data[i]['birthday'].split('-')[0] + '/2005',
			'className': data[i]['tkt'].replace('4 ', '')
		}
	with open('JSON/Info/clients.json', 'w') as jfile: json.dump(new, jfile, indent=2)

def reformat():
	with open(f'JSON/Info/clients.json', 'r') as file: data = json.load(file)
	for i in data:
		data[i]['birthday'] = data[i]['birthday'].replace('/2005', '')
	with open("JSON/Info/clients.json", "w") as jfile: json.dump(data, jfile, indent=2)

Clear()
Reformat()
GetLen()