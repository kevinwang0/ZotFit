# class node for implementing linked list style things 

class Node:
	def __init__(self, data):
		self.data = data
		self.next = None

	def getData(self):
		return self.data

	def getNext(self):
		return self.next

	def setData(self, data):
		self.data = data

	def setNext(self, nxt):
		self.next = nxt

def hello():
	print("hello")