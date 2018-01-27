import json
class TrieNode():
    def __init__(self):
        self.jsons = set()
        self.children = {}

class Trie():
    def __init__(self):
        self.root = TrieNode()
    def insertJsonObject(self, json_object):
        id_of_object = id(json_object)
        node = self.root
        self.insertKeyToNode(json_object, node, id_of_object)
        return id_of_object
    def insertKeyToNode(self, json_object, node, id_of_object):
        node.jsons.add(id_of_object)
        if not isinstance(json_object, dict):
            if json_object not in node.children:
                node.children[json_object] = TrieNode()
            node.children[json_object].jsons.add(id_of_object)
            #print('not instance', id_of_object)
            return
        for key, val in json_object.items():
            if key not in node.children:
                node.children[key] = TrieNode()
            self.insertKeyToNode(val, node.children[key], id_of_object)
        return
    def searchExampleJson(self, example_json):
        node = self.root
        tree_id_set = self.searchKeyFromNode(example_json, node)
        return tree_id_set

    def searchKeyFromNode(self, example_json, node):
        if not example_json:
            return node.jsons
        if not isinstance(example_json, dict):
            if example_json in node.children:
                return node.children[example_json].jsons
            return set()
        level_id_set = set()
        for key, val in example_json.items():
            #print(key, val, key not in node.children)
            if key not in node.children:
                return set()
            node_id_set = self.searchKeyFromNode(val, node.children[key])
            #print(key, val, 'node_id_set', node_id_set)
            if not node_id_set:
                return set()
            level_id_set = level_id_set & node_id_set if level_id_set else node_id_set
            #print(key, val, 'level_id_set', level_id_set)

        return level_id_set




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
    id2document, lists, documents = {}, [], []
    trie = Trie()
    for line in command_document:
        command, document = line[0], line[1]
        if command =='add':
            json_object = json.loads(document)
            if 'type' in json_object and json_object['type']== 'list':
                documents.append(document)
                lists.append(set(json_object['list']))
            else:
                id_of_object = trie.insertJsonObject(json_object)
                id2document[id_of_object] = document
                #print(command, trie.root.children['active'].children[True].jsons)

        elif command == 'get':
            example_json = json.loads(document)
            if 'type' in example_json and example_json['type'] == 'list':
                example_list = example_json['list']
                for i, list_object in enumerate(lists):
                    if findInList(example_list, list_object):
                        print(documents[i])
            else:
                get_id_set = trie.searchExampleJson(example_json)
                for object_id in get_id_set:
                    if object_id in id2document:
                        print(id2document[object_id])
                #print(command, document, get_id_set)

        elif command == 'delete':
            example_json = json.loads(document)
            if 'type' in example_json and example_json['type'] == 'list':
                new_lists = []
                new_documents = []
                for i, list_object in enumerate(lists):
                    example_list = example_json['list']
                    if not findInList(example_list, list_object):
                        new_lists.append(list_object)
                        new_documents.append(documents[i])

                lists = new_lists
                documents = new_documents
            else:
                delete_id_set = trie.searchExampleJson(example_json)
                for object_id in delete_id_set:
                    del id2document[object_id]
                #print(command, document, delete_id_set)

    return


def findInList(example_list, list_object):
    if not example_list:
        return True
    for ele in example_list:
        if ele not in list_object:
            return False
    return True



if __name__ == '__main__':
    handleQuery()
