#!/usr/bin/python2
import numpy as np
import glob
import os

import matplotlib.pyplot as plt

def search4Word(string,word): #Search for word in string
	string = string.split()
	for i in range(len(string)):
		if string[i] == word:
			return i

	return -1

def isCommentLine(string): #Is string pcr comment line

	if string != "":
		if string[0] == "!":
			return True
		else:
			return False
	else: 

		return False

def pcrFileSearch(fileName,search, looking4AtomData, atomName):

	file = open(fileName,'r')
	file = file.read()
	lines= file.split('\n')

	result = []

	if looking4AtomData == 0:
		for i in range(len(lines)):
			if isCommentLine(lines[i]):		
				index = search4Word(lines[i],search) -1 # minus 1 for ! char in list
				#print("index ",index)
				if index >= 0: #search4Word returns -1 if word not found
					result.append(lines[i+1].split()[index])
					break
	else:
		for i in range(len(lines)):
			if lines[i] != '':
				if lines[i][0:5] == "!Atom": #Look for atom line, continue sarching next lines for the atom specified
					index = search4Word(lines[i],search) # minus 1 for ! char in list, search for word we are looking for in line get position
					for x in range(i+1,len(lines)):
						if lines[x][0:len(atomName)] == atomName: #Once Atom is found look for the data in index position and add to result
							result.append(lines[x].split()[index])
							break



	return result





####################################################################

# Plots info from a series of pcr files such as a, b, c
#Folders containing seperate pcr files must have same name folowed by
#parameter that differentiates it from other refinments in series, E.G 
# doping percentage or temperature Cs0.05, Cs0.075 or MAPbI3_100, MAPbI3_150
#pcr files should either have same name or named the same as the folder containg it
#atom details not yet supported.
#Splits lines into list of words according to white space to sort.

####################################################################



#Directory
directory = "/home/jake/Documents/PhD/Experiments_To_Be_Sorted/ESRF_ID22/"
partialName = "MA"
pcrName = "Cs(0_025)MA(0_975)PbI3.pcr"

#Settings
filenameIsFolderName = 0 # 0 = no, 1 = yes

looking4AtomData = 0 # 0 = no, 1 = yes, Is the data to be plotted assosiated to a specific atom in pcr
atomName = "Pb2"

searchWord = 'a'



folderSpecifer = []
searchData = []


#Look for all directories starting with folder name partialName
for file in glob.glob(directory+partialName+"*"):

	#if this is a directory
	if os.path.isdir(file):

		#add folder name to folderSpecifier and remove drectory and begining of folder name
		folderSpecifer.append(file.replace(directory+partialName,''))
		#look in pcr for specified data and add it to searchData list
		if filenameIsFolderName == 0:
			searchData.append(pcrFileSearch(file+'/'+pcrName,searchWord,looking4AtomData,atomName))
		else:
			searchData.append(pcrFileSearch(file+'/'+file.replace(directory,''),searchWord,looking4AtomData,atomName))

npFolder = np.array(folderSpecifer)
npSearch = np.array(searchData)

npData = np.column_stack((npFolder,npSearch))
plt.xlabel(searchWord)
plt.plot(npFolder,npSearch,'k.')
plt.show()

				
