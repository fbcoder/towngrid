#!/usr/bin/env python
class SimpleQueue:
	def __init__(self,lst):
		self.list = lst
	
	def giveItem(self):
		if len(self.list) != 0:
			item = self.list.pop(0)
			self.list.append(item)
			return item
		return None
		
	def add(self,item):
		self.list.append(item)		
