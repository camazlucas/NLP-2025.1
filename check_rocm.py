import torch
print(f"\n🔍 PyTorch: {torch.__version__}")
print(f"🔍 GPU: {torch.cuda.is_available()}")
print(f"🔍 Nome da GPU: {torch.cuda.get_device_name(0)}")

# Nova forma de verificar ROCm a partir do PyTorch 2.0+
print(f"🔍 Backend GPU: {'ROCm' if torch.version.hip else 'CUDA'}")
print(f"🔍 Versão HIP: {torch.version.hip}\n")