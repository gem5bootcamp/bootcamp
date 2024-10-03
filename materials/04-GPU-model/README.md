## Note on running GPU FS

You need not use docker to run simulations in GPUFS mode. We will be simulating AMD's latest GPU, MI200, in FS mode.
However, you do need docker support for compiling GPUFS applications.  To do so:

```sh
docker pull ghcr.io/gem5/gpu-fs:latest
```

# If you haven't built m5ops yet, then build here

```sh
cd /workspaces/2024/gem5/util/m5
scons build/x86/out/m5
```

# To compile square for MI200

```sh
cd /workspaces/2024/gem5-resources/src/gpu/square
cp /workspaces/2024/materials/04-GPU-model/Makefile ./
docker run --rm -v /workspaces/2024:/workspaces/2024 -w ${PWD} ghcr.io/gem5/gpu-fs:latest make
```

# To run square in FS mode

```sh
cd /workspaces/2024
```
```sh
/usr/local/bin/gem5-vega gem5/configs/example/gpufs/mi200.py --kernel ./vmlinux-gpu-ml-isca --disk-image ./x86-ubuntu-gpu-ml-isca --app ./gem5-resources/src/gpu/square/bin/square --no-kvm-perf
```

# MFMA example
```sh
cd /workspaces/2024/
cp -r materials/04-GPU-model/mfma_fp32/ gem5-resources/src/gpu/mfma_fp32
cd gem5-resources/src/gpu/mfma_fp32
docker run --rm -v /workspaces/2024:/workspaces/2024 -w ${PWD} ghcr.io/gem5/gpu-fs:latest make
cd /workspaces/2024/
/usr/local/bin/gem5-vega -d mfma-outdyn gem5/configs/example/gpufs/mi200.py --reg-alloc-policy=dynamic --kernel ./vmlinux-gpu-ml-isca --disk-image ./x86-ubuntu-gpu-ml-isca --app ./gem5-resources/src/gpu/mfma_fp32/mfma_fp32_32x32x2fp32 --no-kvm-perf
/usr/local/bin/gem5-vega -d mfma-outsimple gem5/configs/example/gpufs/mi200.py --reg-alloc-policy=simple --kernel ./vmlinux-gpu-ml-isca --disk-image ./x86-ubuntu-gpu-ml-isca --app ./gem5-resources/src/gpu/mfma_fp32/mfma_fp32_32x32x2fp32 --no-kvm-perf
```

# To create a checkpoint (assuming m5_checkpoint_addr() is already included in the application), we need to recompile square so that it creates a checkpoint
```sh
cp materials/04-GPU-model/square-cpt/square.cpp gem5-resources/src/gpu/square/
```
```sh
cp materials/04-GPU-model/mi200.py gem5/configs/example/gpufs/
```
```sh
cd gem5-resources/src/gpu/square
```
```sh
docker run --rm -v /workspaces/2024:/workspaces/2024 -w ${PWD} ghcr.io/gem5/gpu-fs:latest make clean
docker run --rm -v /workspaces/2024:/workspaces/2024 -w ${PWD} ghcr.io/gem5/gpu-fs:latest make
```

# To create checkpoint

```sh
cd /workspaces/2024
```
```sh
/usr/local/bin/gem5-vega -d createckpt gem5/configs/example/gpufs/mi200.py --kernel ./vmlinux-gpu-ml-isca --disk-image ./x86-ubuntu-gpu-ml-isca --app ./gem5-resources/src/gpu/square/bin/square --no-kvm-perf --checkpoint-dir ./gpuckpt
```

# To restore from checkpoint
```sh
/usr/local/bin/gem5-vega -d restoreckpt gem5/configs/example/gpufs/mi200.py --kernel ./vmlinux-gpu-ml-isca --disk-image ./x86-ubuntu-gpu-ml-isca --app ./gem5-resources/src/gpu/square/bin/square --no-kvm-perf --restore-dir ./gpuckpt
```

# PyTorch example
```sh
cd /workspaces/2024/
/usr/local/bin/gem5-vega -d pytorch-out gem5/configs/example/gpufs/mi200.py --disk-image ./x86-ubuntu-gpu-ml-isca --kernel ./vmlinux-gpu-ml-isca --no-kvm-perf --app materials/04-GPU-model/pytorch/pytorch_test.py
```
# util in gem5 -- for PyTorch example
```sh
cd gem5/util/term
make
```
# open new terminal
```sh
cd /workspaces/2024/gem5/
./util/term/m5term 7000
```
# run MNIST
```sh
cd /workspaces/2024/
/usr/local/bin/gem5-vega -d mnist-out gem5/configs/example/gpufs/mi200.py --disk-image ./x86-ubuntu-gpu-ml-isca --kernel ./vmlinux-gpu-ml-isca --no-kvm-perf --app materials/04-GPU-model/pytorch/MNIST/test_1batch/pytorch_qs_mnist.py
```

# NanoGPT
# adding files to disk image
```sh
mkdir mnt
mount -o loop,offset=$((2048*512)) ./x86-ubuntu-gpu-ml-isca mnt
cp -r materials/04-GPU-model/pytorch/nanoGPT/nanoGPT-ff/ mnt/root/
umount mnt
/usr/local/bin/gem5-vega -d tutorial_nanogpt --debug-flags=GPUCommandProc gem5/configs/example/gpufs/mi200.py --disk-image ./x86-ubuntu-gpu-ml-isca --kernel ./vmlinux-gpu-ml-isca --app materials/04-GPU-model/pytorch/nanoGPT/train-ff.sh --skip-until-gpu-kernel=8 --exit-after-gpu-kernel=9 --no-kvm-perf
```

# Runnning GPUSE
```sh
docker pull ghcr.io/gem5/gcn-gpu:v24-0
cd gem5-resources/src/gpu/square
docker run --rm -v ${PWD}:${PWD} -w ${PWD} ghcr.io/gem5/gcn-gpu:v24-0 make
cd gem5
docker run --rm --volume $(pwd):$(pwd) -w $(pwd) ghcr.io/gem5/gcn-gpu:v24-0 scons build/VEGA_X86/gem5.opt -j <num cores>
docker run --rm --volume $(pwd):$(pwd) -w $(pwd) ghcr.io/gem5/gcn-gpu:v24-0 gem5/build/VEGA_X86/gem5.opt gem5/configs/example/apu_se.py -n 3  --gpu --gfx-version=gfx900 -c gem5-resources/src/gpu/square/bin/square
```
