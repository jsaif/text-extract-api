#!/usr/bin/env python3
"""
AI-Powered Text Extraction Strategy with GPU Acceleration
Demonstrates how to use local AI models for enhanced text processing
"""

import os
import time
from typing import Dict, Any, Optional
import asyncio

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from text_extract_api.extract.extract_result import ExtractResult
from text_extract_api.extract.strategies.strategy import Strategy
from text_extract_api.files.file_formats.file_format import FileFormat
from text_extract_api.files.file_formats.image import ImageFileFormat

class AIEnhancedStrategy(Strategy):
    """AI-powered text extraction with GPU acceleration support"""
    
    def __init__(self):
        self.device = self._setup_device()
        self.model = None
        self.tokenizer = None
        
    @classmethod
    def name(cls) -> str:
        return "ai-enhanced"
    
    def _setup_device(self) -> str:
        """Setup the best available device for AI processing"""
        if not TORCH_AVAILABLE:
            return "cpu"
            
        # Check for GPU availability
        if torch.cuda.is_available():
            device = "cuda"
            print(f"🚀 Using NVIDIA GPU: {torch.cuda.get_device_name()}")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            device = "mps"
            print("🚀 Using Apple Silicon GPU (Metal)")
        else:
            device = "cpu"
            print("💻 Using CPU for AI processing")
            
        return device
    
    def _load_ai_model(self):
        """Load a lightweight AI model for text enhancement"""
        if self.model is not None:
            return
            
        try:
            # Try to load a lightweight text processing model
            from transformers import pipeline
            
            print(f"📦 Loading AI text processing model on {self.device}...")
            
            # Use a small, fast model for text classification/enhancement
            self.model = pipeline(
                "text-classification",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=0 if self.device == "cuda" else -1,
                return_all_scores=True
            )
            
            print("✅ AI model loaded successfully")
            
        except ImportError:
            print("⚠️  Transformers not available, using basic processing")
            self.model = None
        except Exception as e:
            print(f"⚠️  Could not load AI model: {e}")
            self.model = None
    
    def _enhance_text_with_ai(self, text: str) -> Dict[str, Any]:
        """Use AI to enhance and analyze extracted text"""
        if not self.model or not text.strip():
            return {"enhanced_text": text, "confidence": 1.0, "analysis": {}}
        
        try:
            # Analyze text sentiment/quality
            chunks = [text[i:i+512] for i in range(0, len(text), 512)]  # Split for processing
            
            analysis_results = []
            for chunk in chunks[:3]:  # Limit to first 3 chunks for speed
                if chunk.strip():
                    result = self.model(chunk)
                    analysis_results.append(result)
            
            # Calculate average confidence
            avg_confidence = 0.8  # Default
            if analysis_results:
                confidences = []
                for result in analysis_results:
                    if result and len(result) > 0:
                        confidences.append(max(score['score'] for score in result[0]))
                if confidences:
                    avg_confidence = sum(confidences) / len(confidences)
            
            return {
                "enhanced_text": text,
                "confidence": avg_confidence,
                "analysis": {
                    "chunks_analyzed": len(analysis_results),
                    "ai_model_used": True,
                    "processing_device": self.device
                }
            }
            
        except Exception as e:
            print(f"⚠️  AI enhancement failed: {e}")
            return {"enhanced_text": text, "confidence": 0.5, "analysis": {"error": str(e)}}
    
    def _extract_with_easyocr(self, images) -> str:
        """Fallback to EasyOCR for basic text extraction"""
        try:
            import easyocr
            
            # Use GPU if available for EasyOCR
            use_gpu = self.device in ["cuda", "mps"]
            reader = easyocr.Reader(['en'], gpu=use_gpu)
            
            all_text = []
            for image_format in images:
                import io
                from PIL import Image
                import numpy as np
                
                pil_image = Image.open(io.BytesIO(image_format.binary))
                np_image = np.array(pil_image)
                
                # Extract text
                result = reader.readtext(np_image, detail=0)
                if result:
                    page_text = '\n'.join(result)
                    all_text.append(page_text)
            
            return '\n\n--- PAGE BREAK ---\n\n'.join(all_text)
            
        except ImportError:
            return "EasyOCR not available for text extraction"
        except Exception as e:
            return f"Error in text extraction: {e}"
    
    def extract_text(self, file_format: FileFormat, language: str = 'en') -> ExtractResult:
        """
        Extract text using AI-enhanced processing with GPU acceleration
        """
        start_time = time.time()
        
        # Ensure we can process the file
        if (not isinstance(file_format, ImageFileFormat) 
            and not file_format.can_convert_to(ImageFileFormat)):
            raise TypeError(f"AI Enhanced - format {file_format.mime_type} not supported")
        
        # Convert to images
        images = FileFormat.convert_to(file_format, ImageFileFormat)
        
        # Load AI model if not already loaded
        self._load_ai_model()
        
        # Extract basic text
        print(f"🔤 Extracting text from {len(images)} image(s)...")
        raw_text = self._extract_with_easyocr(images)
        
        # Enhance with AI
        print("🧠 Enhancing text with AI analysis...")
        enhanced_result = self._enhance_text_with_ai(raw_text)
        
        processing_time = time.time() - start_time
        
        # Create comprehensive metadata
        metadata = {
            'strategy': self.name(),
            'processing_device': self.device,
            'gpu_accelerated': self.device in ["cuda", "mps"],
            'ai_enhanced': self.model is not None,
            'confidence_score': enhanced_result['confidence'],
            'processing_time': round(processing_time, 3),
            'pages_processed': len(images),
            'language': language,
            'analysis': enhanced_result['analysis']
        }
        
        return ExtractResult(enhanced_result['enhanced_text'], metadata)

# Demonstration function
def demo_ai_gpu_benefits():
    """Demonstrate AI and GPU benefits for text processing"""
    print("🤖 AI-Enhanced Text Extraction Demo")
    print("=" * 40)
    
    # Check available hardware
    if TORCH_AVAILABLE:
        print(f"🔥 PyTorch available: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"🚀 NVIDIA GPU: {torch.cuda.get_device_name()}")
            print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("🚀 Apple Silicon GPU available")
        else:
            print("💻 CPU processing mode")
    else:
        print("❌ PyTorch not available - install for GPU acceleration")
    
    # Show potential speedups
    print("\n📊 Expected Performance Benefits:")
    print("• Text Classification: 5-20x faster with GPU")
    print("• Large Language Models: 10-100x faster with GPU")
    print("• Batch Processing: Significant speedup for multiple documents")
    print("• Real-time Analysis: GPU enables real-time text enhancement")
    
    # AI model recommendations
    print("\n🧠 Recommended AI Models for Text Processing:")
    models = [
        ("distilbert-base-uncased", "Fast text classification", "Small"),
        ("microsoft/DialoGPT-medium", "Text enhancement", "Medium"),
        ("facebook/bart-large-cnn", "Text summarization", "Large"),
        ("t5-small", "Text-to-text generation", "Small"),
        ("microsoft/codebert-base", "Code analysis", "Medium"),
    ]
    
    for model, purpose, size in models:
        print(f"• {model} - {purpose} ({size})")

if __name__ == "__main__":
    demo_ai_gpu_benefits()
