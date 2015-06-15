#!/usr/bin/python
def build_db(path):
    fo = open(path, 'r')
    m = [] 
    i = 1
    for line in fo.readlines():
        m.append((i, line))
        i+=1
    fo.close()
    return m
