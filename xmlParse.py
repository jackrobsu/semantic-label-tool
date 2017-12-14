#-*- coding:utf-8 -*-

import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement, ElementTree
import re


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
