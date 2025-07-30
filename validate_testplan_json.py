#!/usr/bin/env python3
"""
JSON Schema Validator for Test Plan Documents

This script validates generated test plan JSON files against the Extended Test Plan Schema.

Usage:
    python validate_testplan_json.py --json path/to/testplan.json [--schema path/to/schema.json]
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("❌ Error: jsonschema library not installed")
    print("Install it with: pip install jsonschema")
    sys.exit(1)

def validate_testplan_json(json_file, schema_file="Extended_TestPlan_JSON_Schema.json"):
    """
    Validate a test plan JSON file against the schema
    
    Args:
        json_file (str): Path to the JSON file to validate
        schema_file (str): Path to the schema file
    
    Returns:
        bool: True if valid, False otherwise
    """
    
    print(f"Validating JSON file: {json_file}")
    print(f"Using schema: {schema_file}")
    print("=" * 50)
    
    # Load schema
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        print("✅ Schema loaded successfully")
    except FileNotFoundError:
        print(f"❌ Error: Schema file not found: {schema_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in schema file - {e}")
        return False
    
    # Load JSON file to validate
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("✅ JSON file loaded successfully")
    except FileNotFoundError:
        print(f"❌ Error: JSON file not found: {json_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in file - {e}")
        return False
    
    # Validate against schema
    try:
        jsonschema.validate(data, schema)
        print("✅ JSON is valid according to the schema!")
        
        # Print summary statistics
        print("\n" + "=" * 50)
        print("📊 Document Summary:")
        print("=" * 50)
        
        print(f"Document ID: {data.get('document_id', 'Not specified')}")
        print(f"Title: {data.get('document_title', 'Not specified')}")
        print(f"Version: {data.get('version', 'Not specified')}")
        print(f"Generated on: {data.get('generated_on', 'Not specified')}")
        print(f"Last updated by: {data.get('last_updated_by', 'Not specified')}")
        
        sections = data.get('sections', [])
        print(f"\nSections: {len(sections)}")
        
        # Count test cases
        total_testcases = 0
        for section in sections:
            section_testcases = len(section.get('testcases', []))
            total_testcases += section_testcases
            
            # Count testcases in subsections
            for subsection in section.get('subsections', []):
                subsection_testcases = len(subsection.get('testcases', []))
                total_testcases += subsection_testcases
        
        print(f"Total test cases: {total_testcases}")
        
        # Count execution list entries
        execution_list = data.get('execution_list', [])
        print(f"Execution list entries: {len(execution_list)}")
        
        # Show section breakdown
        if sections:
            print(f"\n📋 Section Breakdown:")
            for i, section in enumerate(sections[:10]):  # Show first 10 sections
                section_num = section.get('section_number', f'Section {i+1}')
                section_title = section.get('section_title', 'Untitled')
                testcase_count = len(section.get('testcases', []))
                subsection_count = len(section.get('subsections', []))
                
                print(f"  {section_num}: {section_title}")
                if testcase_count > 0:
                    print(f"    └─ Test cases: {testcase_count}")
                if subsection_count > 0:
                    print(f"    └─ Subsections: {subsection_count}")
            
            if len(sections) > 10:
                print(f"  ... and {len(sections) - 10} more sections")
        
        return True
        
    except jsonschema.exceptions.ValidationError as e:
        print("❌ JSON validation failed!")
        print(f"\nValidation Error: {e.message}")
        print(f"Failed at path: {' -> '.join(str(p) for p in e.absolute_path)}")
        
        if e.context:
            print("\nAdditional context:")
            for context_error in e.context:
                print(f"  - {context_error.message}")
        
        return False
    
    except jsonschema.exceptions.SchemaError as e:
        print(f"❌ Schema error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Validate test plan JSON against schema')
    parser.add_argument('--json', required=True, help='Path to the JSON file to validate')
    parser.add_argument('--schema', default='Extended_TestPlan_JSON_Schema.json', 
                       help='Path to the schema file (default: Extended_TestPlan_JSON_Schema.json)')
    
    args = parser.parse_args()
    
    print("🔍 Test Plan JSON Validator")
    print("=" * 50)
    
    is_valid = validate_testplan_json(args.json, args.schema)
    
    if is_valid:
        print(f"\n🎉 Validation successful! The JSON file is valid.")
        sys.exit(0)
    else:
        print(f"\n❌ Validation failed! Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
