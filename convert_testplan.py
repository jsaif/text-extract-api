#!/usr/bin/env python3
"""
Test Plan PDF to JSON Converter

This script demonstrates how to convert a test plan PDF document 
to structured JSON using the text-extract-api with the Extended Test Plan Schema.

Usage:
    python convert_testplan.py --file path/to/testplan.pdf [--output output.json]
"""

import argparse
import json
import time
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from client.cli import upload_file, get_task_result

def convert_testplan_to_json(pdf_file_path, output_file=None, model="llama3.1"):
    """
    Convert a test plan PDF to structured JSON using text-extract-api
    
    Args:
        pdf_file_path (str): Path to the test plan PDF file
        output_file (str, optional): Output JSON file path
        model (str): LLM model to use for conversion
    
    Returns:
        dict: Parsed JSON structure or None if failed
    """
    
    print(f"Converting test plan PDF: {pdf_file_path}")
    print(f"Using model: {model}")
    
    # Check if files exist
    if not os.path.exists(pdf_file_path):
        print(f"Error: PDF file not found: {pdf_file_path}")
        return None
    
    prompt_file = "examples/testplan-to-json-prompt.txt"
    if not os.path.exists(prompt_file):
        print(f"Error: Prompt file not found: {prompt_file}")
        return None
    
    try:
        # Step 1: Upload file and start OCR + LLM processing
        print("\n=== Step 1: Uploading file and starting processing ===")
        task_response = upload_file(
            file_path=pdf_file_path,
            strategy="ai_enhanced",  # Use AI-enhanced OCR strategy
            prompt_file=prompt_file,
            model=model,
            ocr_cache=True,
            storage_profile="default"
        )
        
        if not task_response or 'task_id' not in task_response:
            print("Error: Failed to upload file or get task ID")
            return None
        
        task_id = task_response['task_id']
        print(f"Task started with ID: {task_id}")
        
        # Step 2: Poll for results
        print("\n=== Step 2: Waiting for processing to complete ===")
        max_attempts = 60  # Maximum wait time: 60 * 10 = 10 minutes
        attempt = 0
        
        while attempt < max_attempts:
            print(f"Checking status... (attempt {attempt + 1}/{max_attempts})")
            
            result = get_task_result(task_id)
            
            if not result:
                print("Error: Failed to get task status")
                return None
            
            state = result.get('state', 'UNKNOWN')
            print(f"Task state: {state}")
            
            if state == 'SUCCESS':
                print("✅ Processing completed successfully!")
                
                # Extract the JSON result
                json_text = result.get('result', '')
                if not json_text:
                    print("Error: No result text returned")
                    return None
                
                # Step 3: Parse and validate JSON
                print("\n=== Step 3: Parsing JSON result ===")
                try:
                    # Try to extract JSON from the response
                    # Sometimes the LLM may include additional text
                    json_start = json_text.find('{')
                    json_end = json_text.rfind('}') + 1
                    
                    if json_start == -1 or json_end == 0:
                        print("Error: No valid JSON found in response")
                        print("Raw response:")
                        print(json_text[:500] + "..." if len(json_text) > 500 else json_text)
                        return None
                    
                    json_content = json_text[json_start:json_end]
                    parsed_json = json.loads(json_content)
                    
                    print("✅ JSON parsed successfully!")
                    print(f"Document title: {parsed_json.get('document_title', 'Unknown')}")
                    print(f"Number of sections: {len(parsed_json.get('sections', []))}")
                    
                    # Count test cases
                    total_testcases = 0
                    for section in parsed_json.get('sections', []):
                        total_testcases += len(section.get('testcases', []))
                        for subsection in section.get('subsections', []):
                            total_testcases += len(subsection.get('testcases', []))
                    
                    print(f"Total test cases found: {total_testcases}")
                    
                    # Step 4: Save to file
                    if output_file:
                        print(f"\n=== Step 4: Saving to {output_file} ===")
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(parsed_json, f, indent=2, ensure_ascii=False)
                        print(f"✅ JSON saved to: {output_file}")
                    
                    return parsed_json
                    
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON - {e}")
                    print("Raw response (first 1000 chars):")
                    print(json_text[:1000])
                    return None
            
            elif state == 'FAILURE':
                print("❌ Processing failed")
                error_info = result.get('status', 'Unknown error')
                print(f"Error details: {error_info}")
                return None
            
            elif state in ['PENDING', 'PROGRESS']:
                status = result.get('status', 'Processing...')
                if 'info' in result:
                    progress = result['info'].get('progress', 0)
                    elapsed = result['info'].get('elapsed_time', 0)
                    print(f"Progress: {progress}% - {status} (elapsed: {elapsed:.1f}s)")
                else:
                    print(f"Status: {status}")
                
                time.sleep(10)  # Wait 10 seconds before next check
                attempt += 1
            
            else:
                print(f"Unknown state: {state}")
                time.sleep(10)
                attempt += 1
        
        print("❌ Timeout: Processing took too long")
        return None
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Convert test plan PDF to structured JSON')
    parser.add_argument('--file', required=True, help='Path to the test plan PDF file')
    parser.add_argument('--output', help='Output JSON file path (optional)')
    parser.add_argument('--model', default='llama3.1', help='LLM model to use (default: llama3.1)')
    
    args = parser.parse_args()
    
    # Generate output filename if not provided
    if not args.output:
        pdf_path = Path(args.file)
        args.output = pdf_path.stem + '_testplan.json'
    
    print("🚀 Test Plan PDF to JSON Converter")
    print("=" * 50)
    
    result = convert_testplan_to_json(args.file, args.output, args.model)
    
    if result:
        print("\n🎉 Conversion completed successfully!")
        print(f"📄 Input: {args.file}")
        print(f"📋 Output: {args.output}")
        print(f"📊 Document: {result.get('document_title', 'Unknown')}")
    else:
        print("\n❌ Conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
