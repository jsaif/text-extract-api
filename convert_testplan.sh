#!/bin/bash

# Simple Test Plan Conversion Script
# This script shows how to convert a test plan PDF to JSON using the existing CLI

echo "🚀 Converting Test Plan PDF to Structured JSON"
echo "=============================================="

# Configuration
TESTPLAN_PDF="examples/your-testplan.pdf"  # Change this to your PDF path
PROMPT_FILE="examples/testplan-to-json-prompt.txt"
MODEL="llama3.1"
STRATEGY="ai_enhanced"
OUTPUT_DIR="converted_testplans"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check if PDF file exists
if [ ! -f "$TESTPLAN_PDF" ]; then
    echo "❌ Error: PDF file not found: $TESTPLAN_PDF"
    echo "Please update TESTPLAN_PDF variable with the correct path"
    exit 1
fi

# Check if prompt file exists
if [ ! -f "$PROMPT_FILE" ]; then
    echo "❌ Error: Prompt file not found: $PROMPT_FILE"
    exit 1
fi

echo "📄 Input file: $TESTPLAN_PDF"
echo "🎯 Strategy: $STRATEGY"
echo "🤖 Model: $MODEL"
echo ""

# Step 1: Upload and process the PDF
echo "=== Step 1: Uploading and processing PDF ==="
UPLOAD_RESULT=$(python client/cli.py ocr_upload \
    --file "$TESTPLAN_PDF" \
    --prompt_file "$PROMPT_FILE" \
    --model "$MODEL" \
    --strategy "$STRATEGY" \
    --ocr_cache true \
    --storage_profile default 2>&1)

echo "$UPLOAD_RESULT"

# Extract task ID from the output
TASK_ID=$(echo "$UPLOAD_RESULT" | grep -o '"task_id": "[^"]*"' | cut -d'"' -f4)

if [ -z "$TASK_ID" ]; then
    echo "❌ Error: Could not extract task ID from upload response"
    exit 1
fi

echo "✅ Task started with ID: $TASK_ID"
echo ""

# Step 2: Wait for completion and get result
echo "=== Step 2: Waiting for processing to complete ==="
MAX_ATTEMPTS=60
ATTEMPT=1

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    echo "Checking status... (attempt $ATTEMPT/$MAX_ATTEMPTS)"
    
    RESULT=$(python client/cli.py get_result --task_id "$TASK_ID" 2>&1)
    
    # Check if the task completed successfully
    if echo "$RESULT" | grep -q '"state": "SUCCESS"'; then
        echo "✅ Processing completed successfully!"
        
        # Extract the JSON result and save to file
        OUTPUT_FILE="$OUTPUT_DIR/$(basename "$TESTPLAN_PDF" .pdf)_testplan.json"
        
        # Extract JSON from the result (between first { and last })
        echo "$RESULT" | sed -n '/{/,/}/p' | python -m json.tool > "$OUTPUT_FILE" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo "✅ JSON saved to: $OUTPUT_FILE"
            echo ""
            echo "=== Conversion Summary ==="
            
            # Display basic info about the converted document
            TITLE=$(python -c "
import json
try:
    with open('$OUTPUT_FILE') as f:
        data = json.load(f)
    print('Document Title:', data.get('document_title', 'Unknown'))
    print('Sections:', len(data.get('sections', [])))
    total_tests = sum(len(s.get('testcases', [])) for s in data.get('sections', []))
    print('Test Cases:', total_tests)
except:
    print('Could not parse JSON file')
            " 2>/dev/null)
            
            echo "$TITLE"
            echo ""
            echo "🎉 Conversion completed successfully!"
            exit 0
        else
            echo "❌ Error: Failed to parse JSON result"
            echo "Raw result:"
            echo "$RESULT"
            exit 1
        fi
    fi
    
    # Check if task failed
    if echo "$RESULT" | grep -q '"state": "FAILURE"'; then
        echo "❌ Processing failed"
        echo "Error details:"
        echo "$RESULT"
        exit 1
    fi
    
    # Show progress if available
    PROGRESS=$(echo "$RESULT" | grep -o '"progress": [0-9]*' | cut -d' ' -f2)
    STATUS=$(echo "$RESULT" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$PROGRESS" ] && [ -n "$STATUS" ]; then
        echo "Progress: ${PROGRESS}% - $STATUS"
    else
        echo "Status: Processing..."
    fi
    
    sleep 10
    ATTEMPT=$((ATTEMPT + 1))
done

echo "❌ Timeout: Processing took too long"
exit 1
