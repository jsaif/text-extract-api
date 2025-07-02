#!/usr/bin/env python3
"""
EasyOCR GPU Performance Test
Tests EasyOCR performance with and without GPU acceleration
"""

import time
import io
import numpy as np
from PIL import Image
import easyocr
import os

def create_test_image():
    """Create a test image with text for OCR testing"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a white image
    img = Image.new('RGB', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    text = """
    GPU Acceleration Test Document
    
    This is a sample document to test EasyOCR
    performance with GPU acceleration enabled.
    
    The quick brown fox jumps over the lazy dog.
    1234567890 !@#$%^&*()
    
    Testing multiple lines and various text elements
    to measure OCR processing speed and accuracy.
    """
    
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw text on image
    draw.multiline_text((50, 50), text, font=font, fill='black', spacing=10)
    
    return img

def test_easyocr_performance(use_gpu=True):
    """Test EasyOCR performance"""
    print(f"\n=== Testing EasyOCR ({'GPU' if use_gpu else 'CPU'} mode) ===")
    
    try:
        # Initialize EasyOCR reader
        start_init = time.time()
        reader = easyocr.Reader(['en'], gpu=use_gpu)
        init_time = time.time() - start_init
        print(f"Initialization time: {init_time:.2f} seconds")
        
        # Create test image
        test_img = create_test_image()
        img_array = np.array(test_img)
        
        # Warm-up run
        reader.readtext(img_array, detail=0)
        
        # Performance test
        num_runs = 5
        total_time = 0
        
        print(f"Running {num_runs} OCR tests...")
        for i in range(num_runs):
            start_time = time.time()
            result = reader.readtext(img_array, detail=0)
            end_time = time.time()
            run_time = end_time - start_time
            total_time += run_time
            print(f"  Run {i+1}: {run_time:.3f} seconds")
        
        avg_time = total_time / num_runs
        print(f"Average OCR time: {avg_time:.3f} seconds")
        print(f"Text extracted: {len(result)} lines")
        
        # Show first few lines of extracted text
        if result:
            print("Sample extracted text:")
            for i, text in enumerate(result[:3]):
                print(f"  {i+1}: {text}")
        
        return avg_time, len(result)
        
    except Exception as e:
        print(f"Error during {('GPU' if use_gpu else 'CPU')} test: {e}")
        return None, None

def check_gpu_availability():
    """Check if GPU is available for EasyOCR"""
    print("=== GPU Availability Check ===")
    
    # Check CUDA
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"PyTorch CUDA available: {cuda_available}")
        if cuda_available:
            print(f"CUDA devices: {torch.cuda.device_count()}")
            print(f"Current device: {torch.cuda.current_device()}")
            print(f"Device name: {torch.cuda.get_device_name()}")
    except ImportError:
        print("PyTorch not installed")
    
    # Check TensorFlow
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        print(f"TensorFlow GPU devices: {len(gpus)}")
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"  GPU {i}: {gpu}")
    except ImportError:
        print("TensorFlow not installed")

def main():
    """Main function to run GPU performance tests"""
    print("🚀 EasyOCR GPU Performance Test")
    print("=" * 50)
    
    check_gpu_availability()
    
    # Test CPU performance
    cpu_time, cpu_results = test_easyocr_performance(use_gpu=False)
    
    # Test GPU performance (if available)
    gpu_time, gpu_results = test_easyocr_performance(use_gpu=True)
    
    # Compare results
    print("\n" + "=" * 50)
    print("📊 Performance Comparison")
    print("=" * 50)
    
    if cpu_time and gpu_time:
        speedup = cpu_time / gpu_time
        print(f"CPU average time:  {cpu_time:.3f} seconds")
        print(f"GPU average time:  {gpu_time:.3f} seconds")
        print(f"GPU speedup:       {speedup:.2f}x faster")
        
        if speedup > 1.5:
            print("✅ Significant GPU acceleration detected!")
        elif speedup > 1.1:
            print("✅ Moderate GPU acceleration detected")
        else:
            print("⚠️  Limited or no GPU acceleration")
    else:
        print("❌ Could not complete performance comparison")
        if cpu_time:
            print(f"CPU time: {cpu_time:.3f} seconds")
        if gpu_time:
            print(f"GPU time: {gpu_time:.3f} seconds")
    
    print("\nTest complete!")

if __name__ == "__main__":
    main()
