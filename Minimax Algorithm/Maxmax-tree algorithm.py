#from math import inf
import os
import sys
def getAppId(s):
    return s[:5]
def getGender(s):
    return s[5]
def getAge(s):
    return int(s[6:9])
def getPet(s):
    return s[9]
def getMedicalCondition(s):
    return s[10]
def getCar(s):
    return s[11]
def getDrivingLicense(s):
    return s[12]
def getDays(s):
    return s[13:20]
def getCountDays(s):
    count = 0
    s1 = getDays(s)
    for i in getDays(s):
        if(i == '1'):
            count+=1
    return count
def checkCompatible(s1, category):
	# print('category', category,'getGender', getGender(s1), 'getAge', getAge(s1), 'getPet', getPet(s1), 'getCar', getCar(s1), 'getDrivingLicense', getDrivingLicense(s1), 'getMedicalCondition', getMedicalCondition(s1))
	#check L compatibility first
	if(getGender(s1) == 'F' and getAge(s1)>17 and getPet(s1) == 'N' and category == 'lahsa'):
		return True
	#check S compatibility otherwise
	elif(getCar(s1) == 'Y' and getDrivingLicense(s1)=='Y' and getMedicalCondition(s1) =='N' and category == 'spla'):
		# print('in here??')
		return True
	else:
		return False
class Applicant:
	def __init__(self, str):
		self.appId = getAppId(str)
		self.gender = getGender(str)
		self.age = getAge(str)
		self.pet = getPet(str)
		self.medicalCondition = getMedicalCondition(str)
		self.car = getCar(str)
		self.drivinglicense = getDrivingLicense(str)
		self.days = getDays(str)
		self.utility = 0
		self.parent = None
		self.fullStr = str
		self.isAvailable = 0
		self.numberDays = getCountDays(str)
def max_value(applicantsList, Grid, turn):
	if(terminal_test(applicantsList)):
		return applicant.utility
	v = -infinity
	for a in successor(applicant):
		v = max(v, max_value(a))
	return v
def GamePlay(applicantsList, Grid):
	max_value(applicantsList, Grid)

def checkIfAdditionValid(days, List,limit):
	flag = 1
	#print('days:', days, 'List', List, 'limit', limit)
	for i in range(7):
		if(List[i] + int(days[i])>limit):
			flag = 0
			break
	if(flag == 0):
		#print('return False')
		return False
	else:
		#print('return True')
		return True

def isAvailable(applicantsList, List,turn):
	availableList = []
	#print('here?', applicantsList, List, turn)
	for i in applicantsList:
		if(turn == 1):
			global spaces
			#print(i.fullStr)
			if(checkCompatible(i.fullStr,'spla') and checkIfAdditionValid(i.days,List,spaces)):
				#print('in here?')
				availableList.append(i)
		elif(turn == -1):
			global beds
			if(checkCompatible(i.fullStr,'lahsa') and checkIfAdditionValid(i.days,List,beds)):
				availableList.append(i)
	return availableList

def addToList(List, days):
	for i in range(7):
		if(int(days[i]) == 1):
			List[i] += 1
def subtractFromList(List, days):
	for i in range(7):
		if(int(days[i]) == 1):
			List[i] -= 1
def evaluate(List):
	count = 0
	for i in List:
		if i >=0:
			count += i
	return count
def fetchFromApplicantList(appId,applicantsList):
	for i in range(len(applicantsList)):
		if(applicantsList[i].appId == appId):
			return i
def maxmax(SPLAList, LAHSAList, applicantsList,parentPath,turn):
	#print('maxmax being called')
	bestMove = {}
	bestMove['bestMoveLAHSA'] = {}
	bestMove['bestMoveSPLA'] = {}
	bestMoveLAHSA = {}
	bestMove['bestMoveLAHSA']['appId'] = -1
	bestMove['bestMoveLAHSA']['score'] = float("-inf")
	bestMoveSPLA = {}
	bestMove['bestMoveSPLA']['appId'] = -1
	bestMove['bestMoveSPLA']['score'] = float("-inf")
	#print(bestMove)[]
	List = []
	if(turn == 1):
		List = SPLAList
	elif(turn == -1):
		List = LAHSAList
	availableList = isAvailable(applicantsList,List,turn)
	#print('????',availableList)
	#for i in range(len(availableList)):
		#print('here')
		#print('======',availableList[i].appId)
	#	x = fetchFromApplicantList(availableList[i].appId,applicantsList)
		#print('available applicant', applicantsList[x].appId)
	if(len(availableList) == 0 and turn == -1):#LAHSA ke chances khtm
		score = {}
		score['bestMoveLAHSA'] = {}
		score['bestMoveSPLA'] = {}
		score['bestMoveSPLA']['appId'] = parentPath[0].appId 
		score['bestMoveSPLA']['score'] = evaluate(SPLAList)	#S Calculate
		if(len(parentPath)>1):
			score['bestMoveLAHSA']['appId'] = parentPath[1].appId 
		else:
			score['bestMoveLAHSA']['appId'] = -1
		score['bestMoveLAHSA']['score'] = evaluate(List) #L Calculate
		#print('parentPath:',':')
		#for p in parentPath:
			#print(p.appId, ',')
		#print()
		#print('LAHSA ke chances khtm')
		return score
	if(len(availableList) == 0 and turn == 1):#SPLA ke chances khtm
		score = {}
		score['bestMoveLAHSA'] = {}
		score['bestMoveSPLA'] = {}
		score['bestMoveSPLA']['appId'] = parentPath[0].appId 
		score['bestMoveSPLA']['score'] = evaluate(List) #S Calculate
		if(len(parentPath)>1):
			score['bestMoveLAHSA']['appId'] = parentPath[1].appId 
		else:
			score['bestMoveLAHSA']['appId'] = -1
		score['bestMoveLAHSA']['score'] = evaluate(LAHSAList) #L Calculate
		#print('changing score each time', score)
		#print('list', List)
		#print('parentPath:', ':')
		#for p in parentPath:
			#print(p.appId,',')
		#print()
		return score
	moves = []
	for i in range(len(availableList)):
		move = {}
		move['bestMoveLAHSA'] = {}
		move['bestMoveSPLA'] = {}
		x = fetchFromApplicantList(availableList[i].appId,applicantsList)
		#print('picking element:',applicantsList[x].appId)
		poppedApp = applicantsList.pop(x)
		addToList(List,poppedApp.days)
		#print('List after picking', List)
		parentPath.append(poppedApp)
		#SPLA's chance
		if(turn == 1 and len(isAvailable(applicantsList,LAHSAList,-turn))>0): #LHASA still exist
			#print('here when lhasa exists')
			result = maxmax(List,LAHSAList,applicantsList,parentPath,-turn)
			#print('result:', result)
			move = result
		elif(turn == -1 and len(isAvailable(applicantsList, SPLAList, -turn))>0): #SPLA still exist
			#print('here when spla still exists')
			result = maxmax(SPLAList, List, applicantsList, parentPath, -turn)
			#print('result: ==', result)
			move = result
		elif(turn == 1 and len(isAvailable(applicantsList, LAHSAList, -turn)) == 0): #No more lahsa left
			#print('no more lahsa left')
			if(len(parentPath)>1):
				move['bestMoveLAHSA']['appId'] = parentPath[1].appId
			else:
				move['bestMoveLAHSA']['appId'] = -1
			move['bestMoveLAHSA']['score'] = evaluate(LAHSAList)
			result = maxmax(List, LAHSAList, applicantsList, parentPath, turn)#turn -> spla's turn only
			#print('result: ==', result)
			move['bestMoveSPLA']['appId'] = result['bestMoveSPLA']['appId']
			move['bestMoveSPLA']['score'] = result['bestMoveSPLA']['score']
		elif(turn == -1 and len(isAvailable(applicantsList, SPLAList, -turn)) == 0): #No more spla left
			#print('no more spla left')
			move['bestMoveSPLA']['appId'] = parentPath[0].appId
			move['bestMoveSPLA']['score'] = evaluate(SPLAList)
			result = maxmax(SPLAList, List, applicantsList, parentPath, turn) #turn -> lahsa's turn only
			#print('result: ==', result)
			move['bestMoveLAHSA']['appId'] = result['bestMoveLAHSA']['appId']
			move['bestMoveLAHSA']['score'] = result['bestMoveLAHSA']['score']

		#print('comparing', move)
		if('appId' in move['bestMoveSPLA'] and'score' in move['bestMoveSPLA'] and move['bestMoveSPLA']['score']>bestMove['bestMoveSPLA']['score'] and turn == 1):
			bestMove = move
		if('appId' in move['bestMoveLAHSA'] and'score' in move['bestMoveLAHSA'] and move['bestMoveLAHSA']['appId'] != -1 and move['bestMoveLAHSA']['score']>bestMove['bestMoveLAHSA']['score'] and turn == -1):
			bestMove = move
		parentPath.remove(poppedApp)
		#print('Inserting back and removing from list',poppedApp.appId)
		#print('Path after removing',':')
		#for p in parentPath:
			#print(p.appId,',')
		#print()
		applicantsList.append(poppedApp)
		subtractFromList(List,poppedApp.days)
		
	return bestMove

def maxCount(List):
	maxC = float("-inf")
	appId = -1
	for i in List:
		if(maxC<i.numberDays):
			maxC = i.numberDays
			appId = i.appId
	return {'max': maxC, 'appId':appId}
def smallestApplicantId(List):
	id = float("inf")
	k = 0
	for i in List:
		if id>int(i.appId):
			id = int(i.appId)
			k = i
	return k.appId
def applyDP(listSPLA, applicants, spacesLeft):
	global spaces
	print(SPLAList)
	opt = [[0 for x in range(spacesLeft+1)] for x in range(applicants+1)]
	for i in range(0, applicants+1):
		for j in range(0, spacesLeft+1):
			if(i == 0 or j == 0):
				opt[i][j] = 0
			elif(checkIfAdditionValid(listSPLA[i-1].days, SPLAList, spaces)):
				opt[i][j] = max(opt[i-1][j], listSPLA[i-1].numberDays + opt[i-1][j-listSPLA[i-1].numberDays])
			else:
				opt[i][j] = opt[i-1][j]
	n = applicants
	W = spacesLeft
	choices = []
	#print(opt)
	res = opt[n][W]
	while(n>0 and W >0):
		if(res == opt[n-1][W]):
			continue
		else:
			choices.append(listSPLA[n-1].appId)
			res = res - listSPLA[n-1].numberDays
			W = W - listSPLA[n-1].numberDays
		n = n-1
	#print('choices:',choices)
	return choices[-1]

if __name__ == "__main__":
	with open("input.txt") as fp:
		global beds
		global spaces
		beds = int(fp.readline())
		spaces = int(fp.readline())
		lPicked = int(fp.readline())
		lSelected = []
		for i in range(lPicked):
			line = fp.readline()
			lSelected.append(line[:5])
		sPicked = int(fp.readline())
		sSelected = []
		for i in range(sPicked):
			line = fp.readline()
			sSelected.append(line[:5])
		a = int(fp.readline())
		appList = {}
		applicantsList = []
		for i in range(a):
			line = fp.readline()
			appList[getAppId(line)] = line
		#print('+++++',appList)
		SPLAList = [0,0,0,0,0,0,0]
		LAHSAList = [0,0,0,0,0,0,0]
		countArr = [0,0,0,0,0,0,0]
		# print(lSelected)
		for i in lSelected:
			if i in appList:
				k = appList.pop(i,None)
				addToList(LAHSAList,getDays(k))
		for i in sSelected:
			if i in appList:
				k = appList.pop(i,None)
				addToList(SPLAList,getDays(k))
		for i in appList:
			x = Applicant(appList[i])
			applicantsList.append(x)		
		
		listSPLA = []
		listLAHSA = []
		for i in applicantsList:
			if(checkCompatible(i.fullStr, 'spla')):
				listSPLA.append(i)
			if(checkCompatible(i.fullStr, 'lahsa')):
				listLAHSA.append(i)
		#print('compatibility Spla')
		#print('compatibility LAHSA')
		#for i in range(len(listLAHSA)):
		#	print(listLAHSA[i].appId)
		#print('applicantsList')
		#for i in range(len(applicantsList)):
		#	print(applicantsList[i].appId)
		#print('splaList till now', SPLAList)
		#print('lahsaList till now', LAHSAList)
		CommonPool = []
		for i in listSPLA:
			if i in listLAHSA:
				CommonPool.append(i)

		for i in range(7):
			countArr[i] = SPLAList[i]
		flag = 0
		for i in applicantsList:
			for j in range(7):
				if(i.days[j] == '1' and (countArr[j]+1)<=spaces):
					countArr[j] +=1
				elif(i.days[j] == '1' and (countArr[j]+1)>spaces):
					flag = 1
					break
		fout = open('output.txt', 'w')
		if(flag == 0 and len(CommonPool)>=1):
			#number of spacecs is always greater than 
			#then can pick greedy
			#pick highest from common pool
			resp = maxCount(CommonPool)
			#print('greedy basic')
			#print(resp['appId'], resp['max'])
			
			fout.write(str(resp['appId']))
		elif(flag == 0 and len(CommonPool)==0):
			resp = smallestApplicantId(listSPLA)
			#print(resp)
			fout.write(resp)
		elif(flag == 1 and len(CommonPool) == 0):#separate applicants apply dp. 
				spacesLeft = 7*spaces
				for i in SPLAList:
					spacesLeft -= i
				#print('DP ==')
				# print(applyDP(listSPLA, len(listSPLA), spacesLeft))
				# fout = open('output.txt', 'w')
				fout.write(applyDP(listSPLA, len(listSPLA), spacesLeft)) 
		else:	
			#print('splaList till now ============', SPLAList)
			#print('lahsaList till now', LAHSAList)	
			# print(maxmax(SPLAList, LAHSAList,applicantsList,[],1))
			bestMove = maxmax(SPLAList, LAHSAList,applicantsList,[],1)
			fout.write(bestMove['bestMoveSPLA']['appId'])