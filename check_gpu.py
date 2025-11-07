# check_gpu.py
import torch

print(f"PyTorch version: {torch.__version__}")
print("-" * 30)

# The most important check
is_cuda_available = torch.cuda.is_available()
print(f"Is CUDA available? -> {is_cuda_available}")

if is_cuda_available:
    gpu_count = torch.cuda.device_count()
    print(f"Number of GPUs available: {gpu_count}")
    for i in range(gpu_count):
        print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    print(f"Current CUDA device: {torch.cuda.current_device()}")
    print(f"PyTorch built with CUDA version: {torch.version.cuda}")
else:
    print("\n[ERROR] PyTorch was not built with CUDA support.")
    print("This means it cannot see your NVIDIA GPU.")
    print("Please follow the re-installation steps.")