import os
import sys
import pandas as pd

os.chdir(os.path.dirname(__file__))

class Node():
    def __init__(self, value = None):
        self.Value = set([value]) if value is not None else set()
        self.Next = None

    def GetDeepNode(self):
        node = self
        while node.Next is not None:
            node = node.Next
        return node

def GenerateGroupNodes(nodeList):
    newNode = Node()
    for node in nodeList:
        node.Next = newNode
        newNode.Value = newNode.Value.union(node.Value)

fileName = 'input/contacts.json'

train_df = pd.read_json(fileName)


train_df['Id'] = train_df['Id'].astype(str)

nodeList = {id: Node(id) for id in train_df['Id']}

for feature in ['Email', 'Phone', 'OrderId']:
    for _, group in train_df[ train_df[feature] != ''].groupby(feature):
        if len(group) == 1:
            continue
        featureNodes = { nodeList[id].GetDeepNode() for id in group['Id']}
        GenerateGroupNodes(featureNodes)
    

train_df['NewId'] =  [ '-'.join( sorted(nodeList[id].GetDeepNode().Value, key = int)) for id in train_df['Id']]
train_df['ContactsSum'] = train_df.groupby('NewId')['Contacts'].transform(sum).astype(str)
train_df['result'] = train_df['NewId'] + ', ' + train_df['ContactsSum']
submit_df = train_df[ ['Id', 'result']].copy()
submit_df.columns = ['ticket_id','ticket_trace/contact']

fileName = 'MySubmit.csv'
submit_df.to_csv(fileName, index=False)


