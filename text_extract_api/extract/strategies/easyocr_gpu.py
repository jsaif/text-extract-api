#!/usr/bin/env python3
"""
GPU-optimized EasyOCR Strategy
Enhanced version with GPU acceleration support
"""

import io
import numpy as np
from PIL import Image
import easyocr
import os
from typing import List, Optional

from extract.extract_result import ExtractResult
from text_extract_api.extract.strategies.strategy import Strategy
from text_extract_api.files.file_formats.file_format import FileFormat
from text_extract_api.files.file_formats.image import ImageFileFormat


class EasyOCRGPUStrategy(Strategy):
    """GPU-optimized EasyOCR Strategy with batch processing"""
    
    def __init__(self):
        self._reader = None
        self._use_gpu = self._detect_gpu_support()
        
    @classmethod
    def name(cls) -> str:
        return "easyocr-gpu"

    def _detect_gpu_support(self) -> bool:
        """Auto-detect if GPU support is available"""
        gpu_available = False
        
        # Check environment variable first
        if os.getenv('USE_GPU', '').lower() in ['true', '1', 'yes']:
            return True
        elif os.getenv('USE_GPU', '').lower() in ['false', '0', 'no']:
            return False
            
        # Auto-detect CUDA support
        try:
            import torch
            if torch.cuda.is_available():
                gpu_available = True
        except ImportError:
            pass
            
        # Check TensorFlow GPU support
        try:
            import tensorflow as tf
            gpus = tf.config.list_physical_devices('GPU')
            if gpus:
                gpu_available = True
        except ImportError:
            pass
            
        return gpu_available

    def _get_reader(self, language: str = 'en') -> easyocr.Reader:
        """Get or create EasyOCR reader with GPU support"""
        if self._reader is None:
            languages = language.split(',') if ',' in language else [language]
            
            print(f"Initializing EasyOCR with GPU={self._use_gpu}, languages={languages}")
            
            try:
                self._reader = easyocr.Reader(
                    languages, 
                    gpu=self._use_gpu,
                    download_enabled=True
                )
            except Exception as e:
                print(f"Failed to initialize GPU reader, falling back to CPU: {e}")
                self._reader = easyocr.Reader(languages, gpu=False)
                self._use_gpu = False
                
        return self._reader

    def _process_image_batch(self, images: List[np.ndarray], batch_size: int = 4) -> List[List[str]]:
        """Process multiple images in batches for better GPU utilization"""
        if not self._use_gpu or len(images) <= 1:
            # Process individually for CPU or single images
            return [self._reader.readtext(img, detail=0) for img in images]
        
        results = []
        for i in range(0, len(images), batch_size):
            batch = images[i:i + batch_size]
            batch_results = []
            
            for img in batch:
                try:
                    result = self._reader.readtext(img, detail=0)
                    batch_results.append(result)
                except Exception as e:
                    print(f"Error processing image in batch: {e}")
                    batch_results.append([])
                    
            results.extend(batch_results)
            
        return results

    def extract_text(self, file_format: FileFormat, language: str = 'en') -> ExtractResult:
        """
        Extract text using GPU-optimized EasyOCR with batch processing
        """

        # Ensure we can actually convert the input file to ImageFileFormat
        if (
            not isinstance(file_format, ImageFileFormat) 
            and not file_format.can_convert_to(ImageFileFormat)
        ):
            raise TypeError(
                f"EasyOCR GPU - format {file_format.mime_type} is not supported"
            )

        # Convert the input file to a list of ImageFileFormat objects
        images = FileFormat.convert_to(file_format, ImageFileFormat)

        # Get the EasyOCR Reader with GPU support
        reader = self._get_reader(language)

        # Convert all images to numpy arrays
        np_images = []
        for image_format in images:
            # Convert the in-memory bytes to a PIL Image
            pil_image = Image.open(io.BytesIO(image_format.binary))
            
            # Convert PIL image to numpy array for EasyOCR
            np_image = np.array(pil_image)
            np_images.append(np_image)

        # Get batch size from environment or use default
        batch_size = int(os.getenv('GPU_BATCH_SIZE', '4'))
        
        # Process images in batches for better GPU utilization
        print(f"Processing {len(np_images)} images with batch size {batch_size}")
        
        if len(np_images) > 1 and self._use_gpu:
            ocr_results = self._process_image_batch(np_images, batch_size)
        else:
            # Process individually
            ocr_results = []
            for np_image in np_images:
                result = reader.readtext(np_image, detail=0)
                ocr_results.append(result)

        # Combine all text results
        all_extracted_text = []
        for result in ocr_results:
            if result:  # Only add non-empty results
                page_text = '\n'.join(result)
                all_extracted_text.append(page_text)

        # Join all pages with page separators
        final_text = '\n\n--- PAGE BREAK ---\n\n'.join(all_extracted_text)
        
        # Create metadata with GPU info
        metadata = {
            'strategy': self.name(),
            'gpu_used': self._use_gpu,
            'language': language,
            'pages_processed': len(images),
            'batch_size': batch_size if self._use_gpu else 1,
            'total_text_blocks': sum(len(result) for result in ocr_results)
        }

        return ExtractResult(final_text, metadata)

    def cleanup(self):
        """Clean up GPU resources"""
        if self._reader is not None:
            # Clear GPU memory if using GPU
            if self._use_gpu:
                try:
                    import torch
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                except ImportError:
                    pass
            self._reader = None
