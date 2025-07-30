# Complete Test Plan PDF to JSON Conversion Workflow

This document demonstrates the complete process of converting a test plan PDF to structured JSON using your text-extract-api with the Extended Test Plan Schema.

## 🚀 Complete Workflow Example

### Step 1: Setup and Prerequisites

```bash
# Install additional dependencies
pip install jsonschema

# Make sure your services are running
# 1. Redis
redis-server

# 2. Ollama with required model
ollama serve
ollama pull llama3.1

# 3. Text-extract-api FastAPI server
python -m uvicorn text_extract_api.main:app --reload --host 0.0.0.0 --port 8000

# 4. Celery worker (in another terminal)
celery -A text_extract_api.celery_app worker --loglevel=info
```

### Step 2: Prepare Your Test Plan PDF

Place your test plan PDF in the examples directory:
```bash
# Example file structure
examples/
├── your-testplan.pdf              # Your input PDF
├── testplan-to-json-prompt.txt    # Created prompt file
└── ...
```

### Step 3: Run the Conversion

#### Option A: Using the Custom Python Script (Recommended)
```bash
# Simple conversion
python convert_testplan.py --file examples/your-testplan.pdf

# With custom output file
python convert_testplan.py --file examples/your-testplan.pdf --output my_testplan.json

# Using different model
python convert_testplan.py --file examples/your-testplan.pdf --model llama3.2-vision
```

#### Option B: Using PowerShell Script (Windows)
```powershell
# Update the PDF path in the script first
$TESTPLAN_PDF = "examples\your-actual-testplan.pdf"

# Run the conversion
.\convert_testplan.ps1
```

#### Option C: Using the CLI Directly
```bash
# Step 1: Upload and process
python client/cli.py ocr_upload \
  --file examples/your-testplan.pdf \
  --prompt_file examples/testplan-to-json-prompt.txt \
  --model llama3.1 \
  --strategy ai_enhanced \
  --ocr_cache true

# Step 2: Get result (replace with actual task_id)
python client/cli.py get_result --task_id YOUR_TASK_ID_HERE
```

### Step 4: Validate the Generated JSON

```bash
# Validate against the schema
python validate_testplan_json.py --json converted_testplans/your-testplan_testplan.json

# You should see output like:
# ✅ JSON is valid according to the schema!
# 📊 Document Summary:
# Document ID: TPI-134163
# Title: JDI-CCL:CloudProvider:EdgeInfraEdge&Peering:DX-VC-CAR
# Sections: 13
# Total test cases: 42
```

## 📋 Example Output Structure

Your converted JSON will follow this structure:

```json
{
  "document_id": "TPI-134163",
  "document_title": "JDI-CCL:CloudProvider:EdgeInfraEdge&Peering:DX-VC-CAR",
  "version": "23.4R2-S3",
  "generated_on": "2025-01-30",
  "last_updated_by": "avodnala@juniper.net",
  "last_updated": "2025-02-21T08:45:56.420484-08:00",
  "sections": [
    {
      "section_number": "1",
      "section_title": "Introduction",
      "content": "The goal of this test plan is to validate the 23.4R2-S3 JUNOS software release...",
      "section_type": "textual"
    },
    {
      "section_number": "8",
      "section_title": "Testcases: VC-CAR",
      "section_type": "testcase_group",
      "content": "This Section covers all the planned test case...",
      "subsections": [
        {
          "section_number": "8.1",
          "section_title": "Functional Tests",
          "section_type": "testcase_group",
          "testcases": [
            {
              "testcase_id": "Tc8.1-1",
              "title": "Baseline Statistics",
              "test_objective": "Baseline system statistics during normal operation",
              "test_setup": "Standard lab topology as described in the test plan",
              "test_nodes": ["VC-CAR (DUT)"],
              "test_procedure": [
                "Disable GRES and determine if there is any change to the system resources noted above"
              ],
              "verifications": [
                "show chassis routing-engine"
              ],
              "expected_results": [
                "compare the configuration and verify if anything has changed"
              ],
              "platforms": ["MX304"],
              "source_of_requirement": "undefined"
            }
          ]
        }
      ]
    }
  ],
  "execution_list": [
    {
      "testcase": "8.1-1",
      "platform": "MX-304-VC-CAR",
      "status": "pending"
    }
  ]
}
```

## 🔧 Configuration Options

### OCR Strategies
- `ai_enhanced` - Best for complex documents with mixed content
- `easyocr` - Fast OCR for simple documents
- `easyocr_gpu` - GPU-accelerated OCR for better performance
- `ollama` - Use Ollama vision models directly

### Models
- `llama3.1` - Good general performance
- `llama3.2-vision` - Better for document understanding
- `minicpm-v` - Alternative vision model

### Prompt Customization
Edit `examples/testplan-to-json-prompt.txt` to:
- Add specific instructions for your document format
- Include domain-specific terminology
- Adjust extraction priorities

## 🚨 Troubleshooting

### Common Issues and Solutions

1. **"Task failed" errors**
   ```bash
   # Check Ollama status
   ollama list
   ollama ps
   
   # Check if model is available
   ollama pull llama3.1
   ```

2. **"No valid JSON found"**
   ```bash
   # Try different model
   python convert_testplan.py --file your.pdf --model llama3.2-vision
   
   # Check OCR quality first
   python client/cli.py ocr_upload --file your.pdf --strategy easyocr --model ""
   ```

3. **Missing sections or test cases**
   ```bash
   # Use more specific prompt
   # Edit examples/testplan-to-json-prompt.txt
   # Add instructions like: "Pay special attention to section 8 test cases"
   ```

4. **Validation errors**
   ```bash
   # Check specific validation error
   python validate_testplan_json.py --json your_file.json
   
   # Common fixes:
   # - Ensure required fields are present
   # - Check array vs string types
   # - Verify section numbering format
   ```

## 📈 Performance Tips

1. **Use GPU acceleration**:
   ```bash
   --strategy easyocr_gpu
   ```

2. **Enable caching for repeated processing**:
   ```bash
   --ocr_cache true
   ```

3. **For large documents (>50 pages)**:
   - Consider splitting into smaller sections
   - Use `docling` strategy for better structure detection
   - Increase timeout in conversion scripts

4. **Optimize prompts**:
   - Be specific about what to extract
   - Include examples in the prompt
   - Use consistent terminology

## 🔄 Batch Processing Example

```bash
#!/bin/bash
# Process multiple test plans

INPUT_DIR="input_testplans"
OUTPUT_DIR="converted_testplans"

mkdir -p "$OUTPUT_DIR"

for pdf in "$INPUT_DIR"/*.pdf; do
    if [ -f "$pdf" ]; then
        echo "Processing: $(basename "$pdf")"
        python convert_testplan.py --file "$pdf" --output "$OUTPUT_DIR/$(basename "$pdf" .pdf)_testplan.json"
        
        # Validate the result
        if [ -f "$OUTPUT_DIR/$(basename "$pdf" .pdf)_testplan.json" ]; then
            python validate_testplan_json.py --json "$OUTPUT_DIR/$(basename "$pdf" .pdf)_testplan.json"
        fi
        
        echo "---"
    fi
done

echo "Batch processing complete!"
```

## 🎯 Next Steps

1. **Customize the schema** for your specific test plan formats
2. **Integrate with your CI/CD pipeline** for automated processing
3. **Build a web interface** for easier document uploads
4. **Add post-processing scripts** for specific data transformations
5. **Create templates** for different types of test plans

This complete workflow gives you everything needed to convert test plan PDFs into structured, validated JSON that follows your Extended Test Plan Schema!
