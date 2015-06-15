#!/usr/bin/python
import linecache
import collections
from operator import itemgetter
import sys, subprocess, os
from ddmin import *
from collections import defaultdict
TEST_TIMES = 0
TARGET = "bug_program"
def test_output_check( out, err, ans_p ):
    if(len(err) > 0 ):
        return "FAIL"
    else:
        m = defaultdict(lambda: 0, {})
        ans = open(ans_p, 'r')
        for line in ans.readlines():
            m[line]+=1
        for line in out.split():
            if(line == '\n'):
                pass
            m[line+'\n']-=1
        for key,value in m.iteritems():
            if(value != 0 ):
                #print out
                #print "================"
                #os.system("cat " + ans_p)
                return "FAIL"
    return "PASS"

def test_one ( path ):
    global TEST_TIMES
    f = open(path, 'r')
    p = subprocess.Popen(
            ["./" + TARGET], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            stdin = f)
    TEST_TIMES += 1
    out, err = p.communicate()
    f.close()
    #print "out"
    #print out
    return test_output_check(out, err, path)
def build_temporary_test_file(charset):
    global LOG
    test_file_name = 'dd_test_tmp'
    f = open(test_file_name, 'w+')
    for key, value in charset:
        f.write( value )
    f.flush()
    f.seek(0)
    LOG.write(">>>>TEST CONTENT START<<<<\n")
    for line in f:
        LOG.write(line)
    LOG.write(">>>>>TEST CONTENT END<<<<<\n")
    f.close()
    return test_file_name
def get_file_content(path):
    with open(path, 'r') as f:
        content = f.read()
    f.close()
    return content
FAIL_CASE = ""
def test_set(char_set):
    global FAIL_CASE
    global LOG
    LOG.write("==============TEST START==============\n")
    if char_set == [] : 
        res = "PASS"
    else:
        fname = build_temporary_test_file( char_set )
        res = test_one ( fname )
        #print res
        if res == "FAIL" :
            FAIL_CASE = get_file_content(fname)
    LOG.write("TEST RESULT : " + res + "\n")
    LOG.write("==============TEST END================\n")
    return res
