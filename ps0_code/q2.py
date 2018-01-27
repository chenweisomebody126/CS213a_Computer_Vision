import json

def readStdin():
    command_document = []
    while True:
        try:
            line = raw_input()
            command_document.append(line.split(' ', 1))
        except:
            break
    return command_document

def handleQuery():
    command_document = readStdin()
    documents= []
    for line in command_document:
        command, document = line[0], line[1]
        if command =='add':
            documents.append(document)
        elif command == 'get':
            example_json = json.loads(document)
            if 'type' in example_json and example_json['type'] == 'list':
                example_list = example_json['list']
                for i in range(len(documents)):
                    list_object= json.loads(documents[i])['list']
                    if findInList(example_list, list_object):
                        print(documents[i])
            else:
                for i in range(len(documents)):
                    json_object = json.loads(documents[i])
                    if findExample(example_json, json_object):
                        print(documents[i])
        elif command == 'delete':
            new_documents = []
            example_json = json.loads(document)
            if 'type' in example_json and example_json['type'] == 'list':
                for i in range(len(documents)):
                    example_list = example_json['list']
                    list_object = json.loads(documents[i])['list']
                    if not findInList(example_list, list_object):
                        new_documents.append(documents[i])
                documents = new_documents
            else:
                for i in range(len(documents)):
                    json_object = json.loads(documents[i])
                    if not findExample(example_json, json_object):
                        new_documents.append(documents[i])
                documents = new_documents
    return

def findExample(example_json, json_object):
    if not example_json:
        return True
    for tag, val in example_json.items():
        if tag not in json_object:
            return False
        if isinstance(val, dict):
            if not findExample(val, json_object[tag]):
                return False
        else:
            if val != json_object[tag]:
                return False
    return True
def findInList(example_list, list_object):
    if not example_list:
        return True
    for ele in example_list:
        if ele not in list_object:
            return False
    return True

handleQuery()
