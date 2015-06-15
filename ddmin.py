import os
from split import split
from listsets import listminus
import subprocess
LOG = open("dd.log", 'w')

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

def ddmin(circumstances, test, target):
    global LOG
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""
    
    assert test([]) == PASS
    assert test(circumstances) == FAIL

    n = 2
    while len(circumstances) >= 2:
        subsets = split(circumstances, n)
        assert len(subsets) == n

        some_complement_is_failing = 0
        for subset in subsets:
            complement = listminus(circumstances, subset)

            if test(complement) == FAIL:
                circumstances = complement
                n = max(n - 1, 2)
                some_complement_is_failing = 1
                break
            else:
                if test(complement) == FAIL:
                    LOG.write("undeterministic event detect")
                    os.system("mv dd_test_tmp undeterministic_input.dat")
                    p = subprocess.Popen(["bash", 'mt_trace.sh', target], stdin=subprocess.PIPE)
                    p.communicate()
                    exit(0)

        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))

    return circumstances
