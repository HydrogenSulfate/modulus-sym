model_item=chip_2d-chip_2d_solid_fluid_heat_transfer_heat_bs1_fp32_DP_dynamic.sh
bs_item=1
fp_item=fp32
run_mode=DP
device_num=N1C1
pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple
# prepare
bash prepare.sh
# run
\cp test_tipc/chip_2d-chip_2d_solid_fluid_heat_transfer_heat/benchmark_common/prepare.sh ./
\cp test_tipc/chip_2d-chip_2d_solid_fluid_heat_transfer_heat/benchmark_common/run_benchmark.sh ./
\cp test_tipc/chip_2d-chip_2d_solid_fluid_heat_transfer_heat/N1C1/chip_2d-chip_2d_solid_fluid_heat_transfer_heat_bs1_fp32_DP_dynamic.sh ./
\cp test_tipc/chip_2d-chip_2d_solid_fluid_heat_transfer_heat/benchmark_common/analysis_log.py ./
jit=0 prim=0 cinn=0 bash run_benchmark.sh ${model_item} ${bs_item} ${fp_item} ${run_mode} ${device_num} 2>&1;
sleep 10;
