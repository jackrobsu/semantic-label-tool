#-*- coding:utf-8 -*-
import os
import re
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree


def searchVerb(verb):
    with open("./noreg.txt") as uf:
        urVerb = uf.readlines()
        urVerbTable = []
    for line in urVerb:
        urVerbTable.append(re.split(' ', line.strip()))
    result = set()

# 第三人称
    if(verb[-1] == 's'):
        mayVerb = verb[:-1]
        result.add(mayVerb)
        if(mayVerb[-1] == 'e'):
            mayVerb = mayVerb[:-1]
            result.add(mayVerb)
            if(mayVerb[-1] == 'i'):
                mayVerb = mayVerb[:-1] + 'y'
                result.add(mayVerb)
# 进行时
    if(verb[-3:] == 'ing'):
        mayVerb = verb[:-3]
        result.add(mayVerb)
        result.add(mayVerb + 'e')
        if(mayVerb[-2] == mayVerb[-1]):
            result.add(mayVerb[:-1])
        if(mayVerb[-1] == 'y'):
            result.add(mayVerb[:-1] + 'ie')
# 不规则动词过去式
    for item in urVerbTable:
        if(verb in item):
            result.add(item[0])
# 规则动词过去式
    if(verb[-2:] == 'ed'):
        result.add(verb[:-1])
        mayVerb = verb[:-2]
        result.add(mayVerb)
        if(mayVerb[-1] == mayVerb[-2]):
            result.add(mayVerb[:-1])
        if(mayVerb[-1] == 'i'):
            result.add(mayVerb[:-1] + 'y')
# 原型
    mayVerb = verb
    result.add(mayVerb)
    searchPool = os.listdir('./frames/')
    Realresult = set()
    for may in result:
        if(may + '.xml' in searchPool):
            Realresult.add(may)
    if (len(Realresult)):
        return Realresult
    return None

def extractXML(verb):
    tree = ET.ElementTree(file='./frames/' + verb + '.xml')
    treeRoot = tree.getroot()
    verbItem = []
    rst = []
    for roleset in treeRoot.iterfind('predicate/roleset'):
        verbItem.append(roleset)    
    for roleset in verbItem:
        word = {}
        searchRst = ''
        rolesetAttr = roleset.attrib
        labelTitle = re.findall(r'.*\.(.*)', rolesetAttr['id'])
        word['word'] = rolesetAttr['id']
        searchRst += rolesetAttr['id'] + ' ' + rolesetAttr['name'] + '\n'
        word['description'] = rolesetAttr['name']
        word['roles'] = []
        for role in roleset.iterfind('roles/role'):
            r = {}
            roleAttr = role.attrib
            r['num'] = roleAttr['n']
            r['descr'] = roleAttr['descr']
            r['role'] = roleAttr['f']
            searchRst += '    ' + roleAttr['n'] + ' ' + \
                roleAttr['f'] + ' ' + roleAttr['descr'] + '\n'
            searchRst += '\n'
            word['roles'].append(r)
            # print(searchRst)
            # rst.append(searchRst)
        rst.append(word)

    return rst

# while True:
#     print(searchVerb(input()))
