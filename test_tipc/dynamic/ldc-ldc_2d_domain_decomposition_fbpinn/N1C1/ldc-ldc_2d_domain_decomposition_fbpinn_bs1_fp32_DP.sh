model_item=ldc-ldc_2d_domain_decomposition_fbpinn_bs1_fp32_DP
bs_item=1
fp_item=fp32
run_mode=DP
device_num=N1C1
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple
# copy files
\cp test_tipc/dynamic/ldc-ldc_2d_domain_decomposition_fbpinn/benchmark_common/prepare.sh ./
\cp test_tipc/dynamic/ldc-ldc_2d_domain_decomposition_fbpinn/benchmark_common/run_benchmark.sh ./
\cp test_tipc/dynamic/ldc-ldc_2d_domain_decomposition_fbpinn/N1C1/ldc-ldc_2d_domain_decomposition_fbpinn_bs1_fp32_DP.sh ./
\cp test_tipc/dynamic/ldc-ldc_2d_domain_decomposition_fbpinn/benchmark_common/analysis_log.py ./
# prepare
bash prepare.sh
# run
to_static=False bash run_benchmark.sh ${model_item} ${bs_item} ${fp_item} ${run_mode} ${device_num} 2>&1;
sleep 10;