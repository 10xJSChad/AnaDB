#AnaDB
#Made for use in my own personal projects
#Not intended to be a full-featured database and shouldn't be treated as such
#This is just for me to search & update lists with more convenience
#Example on usage below

#from AnaDB import AnaDatabase
#urgovaan = AnaDatabase("Urgovaan")
#urgovaan.create("creatures", ["name", "hp", "dmg"])
#urgovaan.enter("creatures", ["Orc", 100, 20])
#urgovaan.getWhere("creatures", "name=Orc")
#urgovaan.getWhere("creatures", "hp>50", "select=name,dmg")
#urgovaan.update("creatures", "name=Orc", "name,hp,dmg", "Orc 2.0", 200, 40)
#urgovaan.removeWhere("creatures", "dmg<50")
#urgovaan.save()
#urgovaan.load()

import os
import pickle

class AnaDatabase:
 def __init__(self, name):
  self.name = name
  self.tables = []
  self.columns = []
  self.entries = []

 def findTableIndex(self, tableName):
  for i in range(0, len(self.tables)):
   if self.tables[i].lower() == tableName.lower(): return i
  return False

 def findColumnIndex(self, tableName, columnName):
  index = self.findTableIndex(tableName)
  for x in range(0, len(self.columns[index])):
   if (self.columns[index][x].lower() == columnName.lower()): return x + 1

 def create(self, tableName, tableColumns):
  self.tables.append(tableName)
  self.columns.append(tableColumns)

 def enter(self, tableName, entryInput):
  index = self.findTableIndex(tableName)
  toEnter = [index]
  for x in entryInput: toEnter.append(x)
  self.entries.append(toEnter)

 def getOperator(self, conditions):
  operators = ["=",">", "<", "#"]
  for x in conditions:
   for y in operators:
    if x == y: return y

 def checkCondition(self, x, y, operator):
  if operator == ">":
   return(int(x) > int(y))
  if operator == "=":
   if isinstance(x, str): return(str(x) == str(y)) 
   if isinstance(x, int): return(int(x) == int(y)) 
  if operator == "#":
   if isinstance(x, str): return(str(x) != str(y)) 
   if isinstance(x, int): return(int(x) != int(y))    
  if operator == "<":
   return(int(x) < int(y))     

 def loopThroughTable(self, tableName):
  index = self.findTableIndex(tableName)
  toReturn = []
  for x in self.entries:
   if x[0] == index: toReturn.append(x)
  return toReturn

 def getWhere(self, tableName, conditions, *args):
  conditionsSplit = conditions.split(",")
  returnList = []; x = ""; y = ""; operator = ""
  tempEntries = self.loopThroughTable(tableName)
  if len(conditionsSplit) == 1:
   operator = self.getOperator(conditionsSplit[0])
   arguments = conditions.split(operator) 
   for entry in tempEntries:
    x = (entry[self.findColumnIndex(tableName, arguments[0])])
    y = arguments[1]
    if self.checkCondition(x, y, operator): returnList.append(entry)
  else:
   for entry in tempEntries:
    for x in conditionsSplit:
     operator = self.getOperator(x)
     arguments = x.split(operator)
     x = (entry[self.findColumnIndex(tableName, arguments[0])])
     y = arguments[1]
     if not self.checkCondition(x, y, operator): add = False
    
  if len(args) == 1:
   conditionsSplit = args[0].split("=")
   if conditionsSplit[0] == "select":
    newReturnList = []; indexes = []
    conditionsSplit = conditionsSplit[1].split(",")
    for x in conditionsSplit: indexes.append(self.findColumnIndex(tableName, x))
    for x in returnList:
     tempList = []
     for i in range(0, len(indexes)):
      tempList.append(x[indexes[i]])     
     newReturnList.append(tempList)
   returnList = newReturnList
  return(returnList)

 def update(self, tableName, conditions, arguments, *args):
  toReplace = (self.getWhere(tableName, conditions))
  toReplaceWith = []; indexes = []
  argumentsSplit = arguments.split(",")
  for x in argumentsSplit: indexes.append(self.findColumnIndex(tableName, x))
  for x in toReplace:
   for i in range(0, len(indexes)):
    x[indexes[i]] = args[i]
   toReplaceWith.append(x)
  for i in range(0, len(toReplace)):
   for y in range(0, len(self.entries)):
    if toReplace[i] == self.entries[y]: self.entries[y] = toReplaceWith[i]
    
 def removeWhere(self, tableName, conditions, *args):
  toRemove = self.getWhere(tableName, conditions)
  for x in toRemove:
   for i in range(0, len(self.entries)): 
    if x == self.entries[i]: self.entries.pop(i); break

 def save(self):
  if not os.path.exists(str(self.name)):
   os.makedirs(str(self.name))
  with open(str(self.name) + "/" 'tables.ana', 'wb') as f:
   pickle.dump(self.tables, f)
  with open(str(self.name) + "/" 'columns.ana', 'wb') as f:
   pickle.dump(self.columns, f)
  with open(str(self.name) + "/" 'entries.ana', 'wb') as f:
   pickle.dump(self.entries, f)      

 def load(self):
  with open(str(self.name) + "/" 'tables.ana', 'rb') as f:
   self.tables = pickle.load(f) 
  with open(str(self.name) + "/" 'columns.ana', 'rb') as f:
   self.columns = pickle.load(f) 
  with open(str(self.name) + "/" 'entries.ana', 'rb') as f:
   self.entries = pickle.load(f)