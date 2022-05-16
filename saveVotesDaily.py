from datetime import datetime, timedelta, date
from firebase import firebase
firebase = firebase.FirebaseApplication('https://python-firebase-70524.firebaseio.com/', None)

subtotal1 = 0
subtotal2 = 0
subtotal3 = 0

dateStart = date(2020, 1, 27)
dbStart = 'votes27_01_2020'
dbEnd = 'votes'
dateEnd = date.today()

daysToSubtract = 0
dateDiff = (dateEnd - dateStart).days

currentDay = 'votes' + datetime.date(datetime.now()).strftime('%d_%m_%Y')
previousDay = 'votes' + (datetime.date(datetime.now()) - timedelta(days=daysToSubtract)).strftime('%d_%m_%Y')


resArr = []
 

for x in range(dateDiff):
	#set days to subtract
	daysToSubtract += 1
	previousDay = 'votes' + (datetime.date(datetime.now()) - timedelta(days=daysToSubtract)).strftime('%d_%m_%Y')
	currentDay = 'votes' + (datetime.date(datetime.now()) - timedelta(days=daysToSubtract-1)).strftime('%d_%m_%Y')
	
	#get day total
	subtotal1 = firebase.get('/python-firebase-70524/' + currentDay + '/', 'ch0001')
	subtotal2 = firebase.get('/python-firebase-70524/' + currentDay + '/', 'ch0002')
	subtotal3 = firebase.get('/python-firebase-70524/' + currentDay + '/', 'ch0003')
	
	#get previous day and create obj
	obj = []
	obj.append(subtotal1 - firebase.get('/python-firebase-70524/' + previousDay + '/', 'ch0001'))
	obj.append(subtotal2 - firebase.get('/python-firebase-70524/' + previousDay + '/', 'ch0002'))
	obj.append(subtotal3 - firebase.get('/python-firebase-70524/' + previousDay + '/', 'ch0003'))
	resArr.insert(0, obj)

#add start
obj = []
obj.append(firebase.get('/python-firebase-70524/' + dbStart + '/', 'ch0001'))
obj.append(firebase.get('/python-firebase-70524/' + dbStart + '/', 'ch0002'))
obj.append(firebase.get('/python-firebase-70524/' + dbStart + '/', 'ch0003'))
resArr.insert(0, obj)

#format
#Votes for dd/mm/yyyy
#Mind = votes, money
#Children's Hospice = votes, money
#Homeless in Barnet = votes, money
#Total = votes, money
#---------------------
#

#set date
i = 0
dateToPrint = dateStart.strftime('%d_%m_%Y')

#string for file
writeToFile = '';

#calculate all totals
totalM = 0
totalC = 0
totalH = 0

#print for console
for l in resArr:
	writeToFile += 'Votes for ' + dateToPrint + '\n'
	if(i==8 or i==11 or i==18):
		writeToFile += '(Added non-button votes.)\n'
	elif(i%7 == 6 or i%7 == 5):
		writeToFile += '(Weekend.)\n'
	writeToFile += 'Mind = ' + str(resArr[i][0]) + '\n'
	writeToFile += 'Childrens Hospice = ' + str(resArr[i][1]) + '\n'
	writeToFile += 'Homeless in Barnet = ' + str(resArr[i][2]) + '\n'
	writeToFile += 'Total = ' + str(resArr[i][0] + resArr[i][1] + resArr[i][2]) + '\n'
	writeToFile += '\n\n\n'
	totalM += resArr[i][0]
	totalC += resArr[i][1]
	totalH += resArr[i][2]
	i += 1
	dateToPrint = (dateStart - timedelta(days=-i)).strftime('%d_%m_%Y')


#write to file
writeToFile += '\n\n-- Total Votes --\n'
writeToFile += 'Mind = ' + str(totalM) + '\n'
writeToFile += 'Childrens Hospice = ' + str(totalC) + '\n'
writeToFile += 'Homeless in Barnet = ' + str(totalH) + '\n'
writeToFile += 'Total = ' + str(totalM + totalC + totalH) + '\n'

writeToFile += '\n-- Total Money Raised --\n'
writeToFile += 'Mind = £' + str(totalM * 5) + '\n'
writeToFile += 'Childrens Hospics = £' + str(totalC * 5) + '\n'
writeToFile += 'Homeless in Barnet = £' + str(totalH * 5) + '\n'
writeToFile += 'Total = £' + str((totalM*5) + (totalC*5) + (totalH*5)) + '\n'

f = open('C:/Users/Krys/Desktop/PythonFiles/votes' + dateEnd.strftime('%d_%m_%Y') + '.txt','w+')
f.write(writeToFile)

print('Done! :)')

