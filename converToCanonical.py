import re
from collections import defaultdict
f = open('equations.txt','r')

def readFromFile():
	eq_Queue=[]
	for each in f:
		### '=' is equal to `- (`  pair so append `-(` instead of '='
		each = each.replace('=','-(')

		for eachSplit in  filter(None,re.split('(-)|(\+)|(\()|(\))',(each.replace(' ','')).strip()))   :			
			### 'a^k' is equal to `1a^k` so append `1` to the string
			if re.match(r'(^[a-z])',eachSplit):
				eq_Queue.append( ('1' + eachSplit) )
				continue
			if eachSplit:
				eq_Queue.append(eachSplit)

		convert(eq_Queue)
		del eq_Queue
		eq_Queue=[]

def removeBraces(equation):
	''' Use simple stacks as always to simplify the braces and signs. Calling it a stack as I do append and pop operations.
		Still is a list object
	'''
	braces_C = 0	
	plus_Minus = []
	for i in range(1,len(equation)):

		if equation[i].find('(') != -1:
			plus_Minus.append(equation[i-1])			
			braces_C += 1
			equation[i]=''
			equation[i-1]=''	
			continue

		if equation[i].find(')') != -1:
			braces_C -= 1
			equation[i]=''
			plus_Minus.pop()
			continue

		if braces_C > 0:
			if equation[i] == '+' or equation[i] == '-':
				if ord(plus_Minus[-1]) ^ ord(equation[i]) == 0:
					equation[i] = '+'
				else:
					equation[i] = '-'
				continue
			elif equation[i-1] == '':
				print equation[i-1],equation[i]
				input()
				if ord(plus_Minus[-1]) ^ ord('+') == 0:
					equation[i-1] = '+'
				else:
					equation[i-1] = '-'
				continue


	equation.insert(0,'+')
	return equation

def convert(equation):
	''' Remove braces first before evaluation in Dictionary Object
	'''
	equation = filter(None,removeBraces(equation))
	eq_Dict=defaultdict(int)
	for i in range(0,len(equation)):
		if equation[i] == '':
			continue
		##### Collect inputs of the from ax^k
		if len(re.split('(^\d+\.*\d*)',equation[i])) > 2:			
			temp = re.split('(^\d+\.*\d*)',equation[i])[1:]

			if equation[i-1] == "-":
				temp[0] = float(temp[0]) * - 1
			else:
				temp[0] = float(temp[0])	
			temp[1] = filter(None,re.split('(\w\^\d+\.\d+)',temp[1]))
			temp[1].sort()
			temp[1] = ''.join(temp[1])
			eq_Dict[temp[1]] += temp[0]

			continue			
	
	sortEquation(eq_Dict)


def sortEquation(eq_Dict):

	allKeys = [key for key in eq_Dict.keys()]
	allKeys.sort()
	if allKeys[0] == '':
		allKeys.append('')
		del allKeys[0]

	finalSolved_Equation = ""	
	for key in allKeys:
		if eq_Dict[key] == 1.0:
			eq_Dict[key] = ''
		if eq_Dict[key] > 1.0:
			eq_Dict[key] = ' + ' + str(eq_Dict[key])
		if eq_Dict[key] == 0:
			continue
		finalSolved_Equation += str(eq_Dict[key]) + key
	print finalSolved_Equation,"=0"

def main():

	while 1:
		C = input("Enter 1 for input, 2 for exit")
		if C != 1:
			break
		readFromFile()			

if __name__ == "__main__":
	main()