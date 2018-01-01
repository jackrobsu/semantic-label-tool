#-*- coding:utf-8 -*-

import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import re
import traceback


def extractXML(verb):
    tree = ET.ElementTree(file='./frames/' + verb + '.xml')
    treeRoot = tree.getroot()
    verbItem = []
    for roleset in treeRoot.iterfind('predicate/roleset'):
        verbItem.append(roleset)
    for roleset in verbItem:
        searchRst = ''
        rolesetAttr = roleset.attrib
        labelTitle = re.findall(r'.*\.(.*)', rolesetAttr['id'])
        searchRst += rolesetAttr['id'] + ' ' + rolesetAttr['name'] + '\n'
        for role in roleset.iterfind('roles/role'):
            roleAttr = role.attrib
            searchRst += '    ' + roleAttr['n'] + ' ' + \
                roleAttr['f'] + ' ' + roleAttr['descr'] + '\n'
            searchRst += '\n'
            print(searchRst)


def extractXMLData(filename):
    try:
        tree = ET.ElementTree(file=filename)
        treeRoot = tree.getroot()
        sentences = []
        for sentence in treeRoot.iter("sentence"):
            sentences.append(sentence)
        
        variables = []
        for variable in treeRoot.iter("variables"):
            for items in variable :
                item = items.attrib
                # print(item['name'])
                v = item['name']
                r = None
                for ref in items :
                    r = ref.text
                if r is not None :
                    variables.append((v,r))
        verbs = []
        for Verb in treeRoot.iter("verb") :
            for verb in Verb :
                v = verb.tag
                # print(verb.tag)
                roles = []
                W = v
                for role in verb.iterfind("thematicRoles"):
                    # print(role.tag)
                    for Arg in role :
                        args = []
                        
                        for arg in Arg :
                            # print(arg.tag)
                            # print(arg.text)
                            # if arg.tag == "role" :
                            #     args.append(arg.text)
                            # elif arg.tag == "content" :
                            #     args.append(arg.tag)
                            args.append(arg.text)
                        roles.append(args)
                for word in verb.iter("wordInSentence") :
                    W = word.text
                verbs.append((W,roles,verb.attrib,v))
        # print(verbs)

        conjunctions = []

        for Conjunction in treeRoot.iter("conjunction") :
            for conjunction in Conjunction :
                v = conjunction.tag
                roles = []
                for item in conjunction :
                    roles.append(item.text)
                conjunctions.append((v,roles,conjunction.attrib))

        # print(conjunctions)

        translates = []

        for translate in treeRoot.iter("translate") :
            translates.append(translate.text)

        # print(translates)

        results = {}
        results['verbs'] = verbs
        results['variables'] = variables
        results['conjunctions'] = conjunctions
        results['sentences'] = sentences
        results['translates'] = translates
        return results

    except Exception :
        traceback.print_exc()
        return None
    
if __name__ == "__main__" :
    print(extractXMLData("result/32c7dd219ea12a810e94aa221cb1e583c458e366a2e692ca92829f095c07459420e33d19.xml"))