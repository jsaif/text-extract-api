# Test Plan PDF to JSON Conversion Guide

This guide shows you how to convert test plan PDF documents to structured JSON using the text-extract-api with the Extended Test Plan Schema.

## Prerequisites

1. **Ollama installed and running** with a model like `llama3.1`
2. **Text-extract-api running** (FastAPI server + Celery workers)
3. **Redis running** for caching

## Quick Start

### Method 1: Using the CLI Tool (Recommended)

```bash
# Basic conversion
python client/cli.py ocr_upload \
  --file examples/your-testplan.pdf \
  --prompt_file examples/testplan-to-json-prompt.txt \
  --model llama3.1 \
  --strategy ai_enhanced \
  --ocr_cache true

# Get the task result (replace TASK_ID with the returned task ID)
python client/cli.py get_result --task_id YOUR_TASK_ID
```

### Method 2: Using the Custom Converter Script

```bash
# Convert with automatic output naming
python convert_testplan.py --file examples/your-testplan.pdf

# Convert with custom output file
python convert_testplan.py --file examples/your-testplan.pdf --output my_testplan.json

# Use different model
python convert_testplan.py --file examples/your-testplan.pdf --model llama3.2-vision
```

## Step-by-Step Process

### 1. Prepare Your Environment

Make sure all services are running:

```bash
# Start Redis (if not running)
redis-server

# Start Ollama (if not running) 
ollama serve

# Pull required model
ollama pull llama3.1

# Start the text-extract-api
python -m uvicorn text_extract_api.main:app --reload

# Start Celery worker (in another terminal)
celery -A text_extract_api.celery_app worker --loglevel=info
```

### 2. Place Your Test Plan PDF

Put your test plan PDF file in a location accessible to the script:

```bash
# Example structure
examples/
  ├── your-testplan.pdf
  ├── testplan-to-json-prompt.txt
  └── ...
```

### 3. Run the Conversion

```bash
python convert_testplan.py --file examples/your-testplan.pdf
```

### 4. Monitor Progress

The script will show progress updates:

```
🚀 Test Plan PDF to JSON Converter
==================================================
Converting test plan PDF: examples/your-testplan.pdf
Using model: llama3.1

=== Step 1: Uploading file and starting processing ===
Task started with ID: abc123-def456-ghi789

=== Step 2: Waiting for processing to complete ===
Checking status... (attempt 1/60)
Task state: PROGRESS
Progress: 30% - Extracting text from file (elapsed: 15.2s)

Checking status... (attempt 2/60)
Task state: PROGRESS  
Progress: 75% - Processing LLM (elapsed: 45.8s)

Checking status... (attempt 3/60)
Task state: SUCCESS
✅ Processing completed successfully!

=== Step 3: Parsing JSON result ===
✅ JSON parsed successfully!
Document title: JDI-CCL:CloudProvider:EdgeInfraEdge&Peering:DX-VC-CAR
Number of sections: 13
Total test cases found: 42

=== Step 4: Saving to your-testplan_testplan.json ===
✅ JSON saved to: your-testplan_testplan.json

🎉 Conversion completed successfully!
📄 Input: examples/your-testplan.pdf
📋 Output: your-testplan_testplan.json
📊 Document: JDI-CCL:CloudProvider:EdgeInfraEdge&Peering:DX-VC-CAR
```

## Expected Output Structure

The generated JSON will follow your Extended Test Plan Schema:

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
      "content": "The goal of this test plan is to validate...",
      "section_type": "textual"
    },
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

## Troubleshooting

### Common Issues

1. **"Task failed" or timeout errors**
   - Check if Ollama is running: `ollama list`
   - Verify the model is available: `ollama pull llama3.1`
   - Check Celery worker logs for errors

2. **"No valid JSON found in response"**
   - The LLM might need a different prompt
   - Try with a different model (llama3.2-vision for better document understanding)
   - Check if the PDF OCR was successful

3. **Missing test cases or sections**
   - Complex documents might need multiple passes
   - Consider using `easyocr_gpu` strategy for better OCR
   - Adjust the prompt to be more specific about the document structure

### Performance Tips

1. **Use GPU acceleration** if available:
   ```bash
   # Use GPU-enabled OCR strategy
   --strategy easyocr_gpu
   ```

2. **Enable caching** for repeated processing:
   ```bash
   --ocr_cache true
   ```

3. **For large documents**, consider splitting into sections first

## Advanced Usage

### Custom Schema Modifications

To modify the schema for specific test plan formats:

1. Edit `Extended_TestPlan_JSON_Schema.json`
2. Update the prompt in `examples/testplan-to-json-prompt.txt`
3. Test with a sample document

### Batch Processing

```bash
# Process multiple files
for pdf in examples/*.pdf; do
    python convert_testplan.py --file "$pdf"
done
```

### Integration with CI/CD

```bash
# Automated test plan processing in CI
python convert_testplan.py --file testplan.pdf --output artifacts/testplan.json
```

## API Endpoints Used

The conversion process uses these text-extract-api endpoints:

- `POST /ocr` - Upload and process document
- `GET /ocr/result/{task_id}` - Get processing status and results
- `GET /storage/list` - List processed files (optional)

## Schema Validation

To validate the generated JSON against the schema:

```bash
# Install jsonschema if not already installed
pip install jsonschema

# Validate the output
python -c "
import json
import jsonschema

# Load schema and JSON
with open('Extended_TestPlan_JSON_Schema.json') as f:
    schema = json.load(f)

with open('your-testplan_testplan.json') as f:
    data = json.load(f)

# Validate
try:
    jsonschema.validate(data, schema)
    print('✅ JSON is valid according to schema')
except jsonschema.exceptions.ValidationError as e:
    print(f'❌ Validation error: {e}')
"
```

This complete workflow allows you to convert any test plan PDF into a structured JSON format that follows your Extended Test Plan Schema!
