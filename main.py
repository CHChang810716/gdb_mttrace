#!/usr/bin/env python
# $Id: ddmin.py,v 2.2 2005/05/12 22:01:18 zeller Exp $
from functools import partial
import sys,getopt
from build_test_db import *
import test2 as Test
import os
from ddmin import *

def main():
    global LOG
    try:
        (options,sysids)=getopt.getopt(sys.argv[1:],'')
    except getopt.error,e:
        print "Usage error: "+e
        print "please give input"
        sys.exit(1)
    db = build_db(sysids[0])
    ddmin(db, Test.test_set, Test.TARGET)
    print "simplify input : "
    print Test.FAIL_CASE
    print "total test times : ", Test.TEST_TIMES
    LOG.close()
    os.remove('dd_test_tmp')

if __name__ == "__main__":
    main()
