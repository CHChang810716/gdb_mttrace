#/bin/bash
for i in {0..19}
do
    gdb --batch -q -x publish.gdb ./small_bug_program > /dev/null
    mkdir test_${i}
    mv *.log test_${i}
done
