'''
Created by suhas on 3/31/2017.
Program to convert equations to Canonical form
Limitations:
1. Cannot not handle * and / operations within brackets. Eg: x + x( 10 +  5x/4 ). Also should contain '='
2. Cannot not handle multiplications of the form  ( a + b ) * ( c + d )
3. Cannot handle '+-','--' .. etc.,
'''
import re,sys
from collections import defaultdict

inputFile = open('equations.txt','r')
outputFile = open('solved_equations.txt','w+')

def readFromCMD():
	cmdInput = raw_input("Enter Equation: ")
	print"Canonical Form: ", inputMode(cmdInput)

def readFromFile():
	for each in inputFile:

		outputFile.write(each)
		out = inputMode(each)
		outputFile.write('Canonical Form: '+out)
		outputFile.write('------------------\n')

	inputFile.close()
	outputFile.close()

def inputMode(each):
	eq_Queue=[]

	if each.count('*') or each.count('/') or each.count('%') or each.count('-+') or \
	each.count('+-') > 0 or each.count('++') > 0 or each.count('--') > 0 or each.count('=') != 1 :
		return 'Incorrect Input\n'			 
	
	### '=' is equal to `- (`  pair so append `-(` instead of '='
	each = each.replace('=','-(')
	
	each = each.replace('((','(+(')
	### Break the equation at braces, +, - signs. 
	for eachSplit in  filter(None,re.split('(-)|(\+)|(\()|(\))',(each.replace(' ','')).strip())):			
		### 'a^k' is equal to `1a^k` so append `1` to the string. This makes the format uniform for further calculations
		if re.match(r'(^[a-zA-Z])',eachSplit):
			eq_Queue.append( ('1' + eachSplit) )
			continue
		if eachSplit:
			eq_Queue.append(eachSplit)
	eq_Queue.append(')')
	return (convertToCanonical(eq_Queue).replace('  ',' '))
	del eq_Queue
	eq_Queue=[]	

def convertToCanonical(equation):
	''' Remove braces first before evaluating the equation
	'''
	equation = filter(None,removeBraces(equation))
	eq_Dict=defaultdict(int)
	if equation[0:5] == 'ERROR':
		return equation

	### Braces are removed. Add/subtract terms in the equation appropirately. 
	### If braces were in the equation it is now of the form -- x + x( a + x ) = x + x*a + x*x
	for i in range(0,len(equation)):
		flag = False
		if equation[i] == '':
			continue

		### convert any term with '*' correct format. ie., ax^k. Eg: 20.1x * 10x^2 * abcxx * 2 = 400.1 abcx^5.0 
		if len(re.split('(\*+)',equation[i]) ) > 1:
			equation[i] = calculateMultiplicationCoefficients(equation[i])
			flag= True

		### Using Dictionary object for adding/subtracting terms. Eg: in '400.1 abcx^5.0 ' {'abcx^5.0' : 400.1}
		### any term which has key 'abcx^5.0' will increment/decerement the value
		if len(re.split('(^\d+\.*\d*)',equation[i])) > 2:		
			if flag == False:
				equation[i] = calculateMultiplicationCoefficients('1*'+equation[i])
			
			temp = re.split('(^\d+\.*\d*)',equation[i])[1:]
			if equation[i-1] == "-":
				temp[0] = float(temp[0]) * - 1

			temp[1] = reorderEquation(temp[1])
			eq_Dict[temp[1]] += float(temp[0])

	return sortEquation(eq_Dict)

def removeBraces(equation):
	''' Use simple stacks as always to simplify the braces and signs. Calling it a stack as I do append and pop operations.
		Using multiplication factor to handle muliplications like  2x( a +  xy ( x  + y )  ) 
	'''
	braces_C = 0	
	plus_Minus = []
	'''
	multiplicationFactor is a stack object which has the multiplication constants from nested braces
	Eg: 2x( a +  xy ( x  + y )  )
	For the above equation the multiplicationFactor is [ '1*', '1*2x' , '1*2x*xy' ]. Using push pop to multiply the appropraiate terms.
	'''
	multiplicationFactor = ['1*']
	for i in range(1,len(equation)):
		if equation[i].find('(') != -1:
			### when opening braches push to stack
			if equation[i-1] != '-' and equation[i-1] != '+':
				### If eq is  x - 2(  a + b ), add 2 to the mulitiplicationFactor Stack.
				multiplicationFactor.append( equation[i-1] )
				if i-2 < 0:
					plus_Minus.append('+')
				else:
					plus_Minus.append(equation[i-2])
			else:
				### If eq is  x - (  a + b ), it is still equivalent to x -  1*( a + b )
				multiplicationFactor.append( multiplicationFactor[-1] + '1*' )
				plus_Minus.append(equation[i-1])
			if len(plus_Minus[-1]) != 1:
				return 'ERROR: Input missing sign before brackets\n'	

			### Remove previous sign to avoid confusion i.e.,  x - (- a ) --> x - +a			
			braces_C += 1
			equation[i]=''
			equation[i-1]=''	
			continue

		if equation[i].find(')') != -1:
			if len(plus_Minus) == 0:
				return 'ERROR: Input has incorrect number of nested brackets\n'			
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
				
			### apply appropriate muliplication factor based on the nesting of braces
			if len(multiplicationFactor) > 1:
				equation[i] = multiplicationFactor[-1] + '*'+ equation[i] 

	equation.insert(0,'+')
	if braces_C != 0:
		return 'ERROR: Input has incorrect number of nested brackets\n'
	return equation

def calculateMultiplicationCoefficients(subEquation):
	temEq = re.split('\*',subEquation)
	newV = 1
	tempDict = defaultdict(int)
	charStack = []
	### convert any term with '*' correct format. ie., ax^k. Eg: 20.1x * 10x^2 * abcxx * 2 = 400.1 abcx^5.0
	### Parsing term by term and using regular expression to reconstruct the string.
	for each in re.split('\*',subEquation):

		if len(re.split('(^\d+\.*\d*)',each)) > 1:
			temp = re.split('(^\d+\.*\d*)',each)[1:]
			newV *= float(temp[0])

			for i in range(0, len(temp[1])):
				if temp[1][i].isalpha():
					if len(charStack) > 0:
						tempDict[charStack.pop()] += 1.0					
					charStack.append( temp[1][i] )				
					continue

				if temp[1][i] == '^':
					power= ""
					i += 1
					while i < len(temp[1]) and not temp[1][i].isalpha():	
						power += temp[1][i]
						i += 1
					tempDict[charStack.pop()] += float(power)
			
			if len(charStack) > 0 :
				tempDict[charStack.pop()] += 1.0
			
	subEquation = ""
	for key in tempDict.keys():
		if tempDict[key] != 1:
			subEquation += key + '^' + str(tempDict[key])
		else:
			subEquation += key
	return str(newV) + (reorderEquation(subEquation))

def reorderEquation(equation):
	''' Reordering the equation to a^k1b^k2...z^kN'''
	equation = filter(None,re.split('(\w\^\d+\.\d+)',equation))
	equation.sort()
	equation = ''.join(equation)	
	return equation


def sortEquation(eq_Dict):

	allKeys = [key for key in eq_Dict.keys()]
	allKeys.sort()
	if allKeys[0] == '':
		allKeys.append('')
		del allKeys[0]
	finalSolved_Equation = ""	

	### Formatting for clean looking output
	for key in allKeys:
		if eq_Dict[key] == 1.0:
			eq_Dict[key] = ''
		if eq_Dict[key] > 1.0 and len(finalSolved_Equation) > 0:
			eq_Dict[key] = ' + ' + str(eq_Dict[key])
		if 	eq_Dict[key] < 0 and len(finalSolved_Equation) > 0:
			eq_Dict[key] = ' - ' + str(eq_Dict[key]*-1)
		if eq_Dict[key] == 0:
			eq_Dict[key] = '0.0'
			continue
		finalSolved_Equation += str(eq_Dict[key]) + key +' '
	if len(finalSolved_Equation) == 0:
		return "0 = 0\n"
	return finalSolved_Equation +" = 0.0\n"

def main():
	while 1:
		C = input("Enter 1 for input from 'equtions.txt' file, 2 read from CMD, 3 for exit")
		if C == 1:
			readFromFile()			
		elif C == 2:
			readFromCMD()
		else:
			exit()
		

if __name__ == "__main__":
	main()
