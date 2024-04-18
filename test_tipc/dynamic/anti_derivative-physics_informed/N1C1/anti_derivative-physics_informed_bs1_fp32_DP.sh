model_item=anti_derivative-physics_informed
bs_item=1
fp_item=fp32
run_mode=DP
device_num=N1C1
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple
# copy files
\cp test_tipc/dynamic/anti_derivative-physics_informed/benchmark_common/prepare.sh ./
\cp test_tipc/dynamic/anti_derivative-physics_informed/benchmark_common/run_benchmark.sh ./
\cp test_tipc/dynamic/anti_derivative-physics_informed/N1C1/anti_derivative-physics_informed_bs1_fp32_DP.sh ./
\cp test_tipc/dynamic/anti_derivative-physics_informed/benchmark_common/analysis_log.py ./
# prepare
bash prepare.sh
# run
to_static=False bash run_benchmark.sh ${model_item} ${bs_item} ${fp_item} ${run_mode} ${device_num} 2>&1;
sleep 10;
