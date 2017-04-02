import re
from collections import defaultdict
inputFile = open('equations.txt','r')
outputFile = open('solved_equations.txt','ab+')

def readFromFile():
	eq_Queue=[]
	for each in inputFile:
		### '=' is equal to `- (`  pair so append `-(` instead of '='
		outputFile.write(each)
		each = each.replace('=','-(')
		
		for eachSplit in  filter(None,re.split('(-)|(\+)|(\()|(\))',(each.replace(' ','')).strip()))   :			
			### 'a^k' is equal to `1a^k` so append `1` to the string
			if re.match(r'(^[a-z])',eachSplit):
				eq_Queue.append( ('1' + eachSplit) )
				continue
			if eachSplit:
				eq_Queue.append(eachSplit)
		outputFile.write(convertToCanonical(eq_Queue))
		del eq_Queue
		eq_Queue=[]
	inputFile.close()
	outputFile.close()

def removeBraces(equation):
	''' Use simple stacks as always to simplify the braces and signs. Calling it a stack as I do append and pop operations.
		Still is a list object
	'''
	braces_C = 0	
	plus_Minus = []

	multiplicationFactor = ['1']

	for i in range(1,len(equation)):

		if equation[i].find('(') != -1:
			if equation[i-1] != '-' and equation[i-1] != '+':
				multiplicationFactor.append( multiplicationFactor[-1] + '*'+ equation[i-1] )
				print multiplicationFactor
				input()
				plus_Minus.append(equation[i-2])
			else:	
				multiplicationFactor.append( multiplicationFactor[-1] + '*'+ '1' )
				plus_Minus.append(equation[i-1])			
			braces_C += 1
			equation[i]=''
			equation[i-1]=''	
			continue

		if equation[i].find(')') != -1:
			braces_C -= 1
			equation[i]=''
			plus_Minus.pop()
			multiplicationFactor.pop()
			continue

		if braces_C > 0:
			if equation[i] == '+' or equation[i] == '-':
				if ord(plus_Minus[-1]) ^ ord(equation[i]) == 0:
					equation[i] = '+'
				else:
					equation[i] = '-'
				continue
			if equation[i-1] == '':
				if ord(plus_Minus[-1]) ^ ord('+') == 0:
					equation[i-1] = '+'
				else:
					equation[i-1] = '-'
				# continue
			if len(multiplicationFactor) > 1:
				equation[i] = multiplicationFactor[-1] + '*'+ equation[i] 
				print equation[i],"new changed equation after multiplcation"
				# input()


	equation.insert(0,'+')
	return equation


def convertToCanonical(equation):
	''' Remove braces first before evaluation in Dictionary Object
	'''
	print equation
	input()
	equation = filter(None,removeBraces(equation))
	print equation, "after removing braches"
	eq_Dict=defaultdict(int)
	for i in range(0,len(equation)):
		if equation[i] == '':
			continue
		##### Collect inputs of the from ax^k
		if len(re.split('\*'),equation[i]) > 0:
			equation[i] = calculateMultiplicationCoefficients(equation[i])

		if len(re.split('(^\d+\.*\d*)',equation[i])) > 2:			
			temp = re.split('(^\d+\.*\d*)',equation[i])[1:]
			print temp
			input()	
			if equation[i-1] == "-":
				temp[0] = float(temp[0]) * - 1

			#### move sorter here abc + acb + bac shud add to 3 abc
			temp[1] = filter(None,re.split('(\w\^\d+\.\d+)',temp[1]))
			temp[1].sort()
			temp[1] = ''.join(temp[1])
			eq_Dict[temp[1]] += float(temp[0])
	return sortEquation(eq_Dict)

def calculateMultiplicationCoefficients(subEquation):
	temEq = re.split('\*',subEquation)


def sortEquation(eq_Dict):

	allKeys = [key for key in eq_Dict.keys()]
	allKeys.sort()
	if allKeys[0] == '':
		allKeys.append('')
		del allKeys[0]

	finalSolved_Equation = ""	

	#### Output Formatting
	for key in allKeys:
		if eq_Dict[key] == 1.0:
			eq_Dict[key] = ''
		if eq_Dict[key] > 1.0 and len(finalSolved_Equation) > 0:
			eq_Dict[key] = ' + ' + str(eq_Dict[key])
		if 	eq_Dict[key] < 0 and len(finalSolved_Equation) > 0:
			eq_Dict[key] = ' - ' + str(eq_Dict[key]*-1)
		if eq_Dict[key] == 0:
			continue
		finalSolved_Equation += str(eq_Dict[key]) + key +' '
	return finalSolved_Equation +" = 0\n"

def main():
	while 1:
		C = input("Enter 1 for input, 2 for exit")
		if C != 1:
			break
		readFromFile()			

if __name__ == "__main__":
	main()