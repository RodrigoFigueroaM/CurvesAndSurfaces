#!/usr/bin/env python
import json

class BSplineLookupTable(object):
	"""docstring for BSplineLookupTable"""
	def __init__(self, *arg):
		super(BSplineLookupTable, self).__init__(*arg)
		self.arg = arg
		self.__BasisFuntionLookUpTable = { }
		with open('BsplineDictionary.json', 'r') as f:
			self.__BasisFuntionLookUpTable = json.load(f)
		

	def addItem(self, key = None , value = None):
		# if key not in self.__BasisFuntionLookUpTable:
		self.__BasisFuntionLookUpTable[key] = value

	def save(self):
		with open('BsplineDictionary.json', 'w') as f:
			json.dump(self.__BasisFuntionLookUpTable, f)
		
	def finalize(self):	 
		with open('BsplineDictionary.json', 'w') as f:
			json.dump(self.__BasisFuntionLookUpTable, f)

	def __getitem__(self, key):
		return self.__BasisFuntionLookUpTable[key]

	