#-*- coding:utf-8 -*-
import os
import re


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


# while True:
#    print(searchVerb(input()))
