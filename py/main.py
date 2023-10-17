import pandas as pd
import numpy as np
import re

filePath = '/content/drive/MyDrive/COLAB_FILES/037.txt'
loadedData = open(filePath).read().split('\n')

woodDataframe = pd.DataFrame(
    {'Type':[],'Description':[],'Length':[],'Mark':[]}
)

woodDataframe = pd.DataFrame({'Type':[],'Description':[],'Length':[],'Mark':[]})

for i in loadedData:
  rowArray = i.split(';')
  newRow = {'Type':rowArray[0],'Description':rowArray[1],'Length':rowArray[2],'Mark':rowArray[3]}
  woodDataframe = woodDataframe.append(newRow, ignore_index=True)

  woodDataframe['TypeDesk'] = woodDataframe['Type'] + ' ' + woodDataframe['Description']
woodDataframe['Length'] = woodDataframe['Length'].astype(int)
woodDataframe = woodDataframe.sort_values(by='Length', ascending=False)
woodDataframe

woodTypes=woodDataframe['TypeDesk'].unique()

woodDB ={}



receivedData = {
  'companyName': 'ECK',
  'projectName': 'ECK 022 048 3',
  'woodCrossSections': [],
  'woodDescriptions': [],
  'woodDetails': []
};

for i in range(len(woodTypes)):
 processingWoodDF = woodDataframe[woodDataframe['TypeDesk'] == woodTypes[i]]
 woodDB[woodTypes[i]]=processingWoodDF

 def woodCutter(woodArray):
  counter=0
  woodArrayLength=woodArray.Length.tolist().copy()
  woodArrayLengthCopy=woodArrayLength.copy()
  woodArrayMark=woodArray.Mark.tolist().copy()
  woodArrayMarkCopy=woodArrayMark.copy()

  woodArray=[]


  while len(woodArrayLength)>0:
    cutLength = 6000
    lCounter =[]
    woodArrayLength=woodArrayLengthCopy.copy()
    woodArrayMark=woodArrayMarkCopy.copy()

    for i in range(len(woodArrayLength)):
      if 6000<woodArrayLength[i]:
        woodArrayLengthCopy.remove(woodArrayLength[i])
        woodArrayMarkCopy.remove(woodArrayMark[i])
        lCounter.append((woodArrayMark[i] +';'+ str(woodArrayLength[i])).split(';'))
        break
      elif cutLength>=woodArrayLength[i]:
        cutLength=cutLength-woodArrayLength[i]
        woodArrayLengthCopy.remove(woodArrayLength[i])
        woodArrayMarkCopy.remove(woodArrayMark[i])
        lCounter.append((woodArrayMark[i] +';'+ str(woodArrayLength[i])).split(';'))

    counter=counter+1
    woodArray.append(lCounter)
  del woodArray[len(woodArray)-1]

  return woodArray


def cutterAll(types, bd):
  resultCount = {}
  for i in types:
    receivedData['woodCrossSections'].append(i)
    receivedData['woodDescriptions'].append(i)
    result = woodCutter(bd[i])
    receivedData['woodDetails'].append(result)
    resultCount[i]=len(result)

  return resultCount

allWoods = cutterAll(woodTypes, woodDB)

#для вывода общего количетсва
pd.DataFrame(list(allWoods.items()),columns = ['TypeDesk','Counts'])

#для вывода информации для раскроя
receivedData

pd.DataFrame(list(allWoods.items()),columns = ['TypeDesk','Counts'])