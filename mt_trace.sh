#/bin/bash -x
target=$1
output_dir_prefix=mttrace_${target}
for i in {0..4}
do
    gdb --batch -q -x publish.gdb ./${target} > /dev/null
    mkdir ${output_dir_prefix}_${i}
    mv *.log ${output_dir_prefix}_${i}
done
