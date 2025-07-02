# GPU Acceleration Setup Guide for Text-Extract-API

## Overview
Your text-extract-api project can benefit significantly from GPU acceleration, especially for:
- **EasyOCR**: OCR processing can be 3-10x faster with GPU
- **Docling**: Document processing acceleration
- **Image processing**: Faster PDF to image conversion

## Current System Status
Based on the GPU check, you're running in a virtualized environment without dedicated GPU access.

## GPU Acceleration Benefits

### EasyOCR GPU Support
- **Speed**: 3-10x faster text extraction
- **Batch processing**: Process multiple images simultaneously
- **Memory efficiency**: Better handling of large documents

### Docling GPU Support
- **Document parsing**: Faster PDF processing
- **Layout analysis**: Accelerated document structure detection

## Setup Instructions

### 1. NVIDIA GPU Setup (Recommended)

#### Prerequisites
```bash
# Check for NVIDIA GPU
nvidia-smi

# Install CUDA Toolkit (Windows)
# Download from: https://developer.nvidia.com/cuda-downloads
```

#### Python Dependencies with GPU Support
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install TensorFlow with GPU support
pip install tensorflow[and-cuda]

# EasyOCR already supports GPU automatically when available
pip install easyocr

# For additional acceleration
pip install opencv-python-headless
pip install pillow-simd  # Faster image processing
```

### 2. AMD GPU Setup (ROCm)

#### For AMD GPUs on Linux
```bash
# Install ROCm
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.4.2
```

### 3. Apple Silicon (M1/M2/M3)

#### For macOS with Apple Silicon
```bash
# Install PyTorch with Metal Performance Shaders
pip install torch torchvision torchaudio
```

## Configuration

### Environment Variables
Create a `.env` file with GPU settings:
```env
# GPU Configuration
USE_GPU=true
GPU_MEMORY_FRACTION=0.8
EASYOCR_GPU=true
BATCH_SIZE=16

# CUDA specific
CUDA_VISIBLE_DEVICES=0
```

### Docker GPU Support
Update your docker-compose files to use GPU:

```yaml
# docker-compose.gpu.yml
version: '3.8'
services:
  text-extract-api:
    build:
      context: .
      dockerfile: dev.gpu.Dockerfile
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - USE_GPU=true
      - NVIDIA_VISIBLE_DEVICES=all
```

## Testing GPU Setup

### Quick Test Commands
```bash
# Test basic GPU detection
python check_gpu.py

# Test EasyOCR with GPU
python test_easyocr_gpu.py

# Benchmark GPU vs CPU performance
python benchmark_gpu.py
```

### Performance Monitoring
```bash
# Monitor GPU usage during processing
nvidia-smi -l 1

# Check GPU memory usage
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

## Troubleshooting

### Common Issues

1. **CUDA Version Mismatch**
   ```bash
   # Check CUDA version
   nvcc --version
   nvidia-smi
   ```

2. **Memory Issues**
   - Reduce batch size in configuration
   - Clear GPU memory between processes
   - Monitor GPU memory usage

3. **Driver Issues**
   - Update NVIDIA drivers
   - Restart after driver installation
   - Check Windows GPU scheduling

### Virtual Machine Limitations
- GPU passthrough required for VM GPU access
- Consider cloud GPU instances (AWS, GCP, Azure)
- Use Docker with GPU support for development

## Cloud GPU Options

### AWS EC2 GPU Instances
- p3.2xlarge (V100)
- g4dn.xlarge (T4)
- g5.xlarge (A10G)

### Google Cloud Platform
- n1-standard with Tesla K80/P4/V100
- Compute Engine with GPU

### Azure
- NC series (Tesla K80/P40/V100)
- ND series (Tesla P40/V100)

## Next Steps

1. **Current Environment**: Continue with CPU-based processing
2. **GPU Hardware**: Install when dedicated GPU becomes available
3. **Cloud GPU**: Consider for heavy processing workloads
4. **Testing**: Use provided scripts to benchmark performance

Run `python check_gpu.py` to verify current capabilities and `check_gpu.bat` for Windows-specific GPU detection.
