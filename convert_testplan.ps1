# PowerShell Script for Test Plan PDF to JSON Conversion
# This script shows how to convert a test plan PDF to JSON using the existing CLI

Write-Host "🚀 Converting Test Plan PDF to Structured JSON" -ForegroundColor Green
Write-Host "=============================================="

# Configuration
$TESTPLAN_PDF = "examples\your-testplan.pdf"  # Change this to your PDF path
$PROMPT_FILE = "examples\testplan-to-json-prompt.txt"
$MODEL = "llama3.1"
$STRATEGY = "ai_enhanced"
$OUTPUT_DIR = "converted_testplans"

# Create output directory
if (!(Test-Path $OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $OUTPUT_DIR
}

# Check if PDF file exists
if (!(Test-Path $TESTPLAN_PDF)) {
    Write-Host "❌ Error: PDF file not found: $TESTPLAN_PDF" -ForegroundColor Red
    Write-Host "Please update TESTPLAN_PDF variable with the correct path"
    exit 1
}

# Check if prompt file exists
if (!(Test-Path $PROMPT_FILE)) {
    Write-Host "❌ Error: Prompt file not found: $PROMPT_FILE" -ForegroundColor Red
    exit 1
}

Write-Host "📄 Input file: $TESTPLAN_PDF"
Write-Host "🎯 Strategy: $STRATEGY"
Write-Host "🤖 Model: $MODEL"
Write-Host ""

# Step 1: Upload and process the PDF
Write-Host "=== Step 1: Uploading and processing PDF ===" -ForegroundColor Yellow

$uploadArgs = @(
    "client\cli.py", "ocr_upload",
    "--file", $TESTPLAN_PDF,
    "--prompt_file", $PROMPT_FILE,
    "--model", $MODEL,
    "--strategy", $STRATEGY,
    "--ocr_cache", "true",
    "--storage_profile", "default"
)

try {
    $uploadResult = & python @uploadArgs 2>&1 | Out-String
    Write-Host $uploadResult
    
    # Extract task ID from the output
    if ($uploadResult -match '"task_id":\s*"([^"]+)"') {
        $TASK_ID = $Matches[1]
        Write-Host "✅ Task started with ID: $TASK_ID" -ForegroundColor Green
    } else {
        Write-Host "❌ Error: Could not extract task ID from upload response" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Error uploading file: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Wait for completion and get result
Write-Host "=== Step 2: Waiting for processing to complete ===" -ForegroundColor Yellow
$MAX_ATTEMPTS = 60
$ATTEMPT = 1

while ($ATTEMPT -le $MAX_ATTEMPTS) {
    Write-Host "Checking status... (attempt $ATTEMPT/$MAX_ATTEMPTS)"
    
    try {
        $result = & python "client\cli.py" "get_result" "--task_id" $TASK_ID 2>&1 | Out-String
        
        # Check if the task completed successfully
        if ($result -match '"state":\s*"SUCCESS"') {
            Write-Host "✅ Processing completed successfully!" -ForegroundColor Green
            
            # Extract the JSON result and save to file
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($TESTPLAN_PDF)
            $OUTPUT_FILE = Join-Path $OUTPUT_DIR "$baseName`_testplan.json"
            
            # Extract JSON from the result
            try {
                # Find JSON content between first { and last }
                $jsonStart = $result.IndexOf('{')
                $jsonEnd = $result.LastIndexOf('}')
                
                if ($jsonStart -ge 0 -and $jsonEnd -gt $jsonStart) {
                    $jsonContent = $result.Substring($jsonStart, $jsonEnd - $jsonStart + 1)
                    
                    # Validate and format JSON
                    $parsedJson = $jsonContent | ConvertFrom-Json
                    $formattedJson = $parsedJson | ConvertTo-Json -Depth 50
                    
                    $formattedJson | Out-File -FilePath $OUTPUT_FILE -Encoding UTF8
                    
                    Write-Host "✅ JSON saved to: $OUTPUT_FILE" -ForegroundColor Green
                    Write-Host ""
                    Write-Host "=== Conversion Summary ===" -ForegroundColor Cyan
                    
                    # Display basic info about the converted document
                    try {
                        $docData = Get-Content $OUTPUT_FILE | ConvertFrom-Json
                        Write-Host "Document Title: $($docData.document_title)"
                        Write-Host "Sections: $($docData.sections.Count)"
                        
                        $totalTests = 0
                        foreach ($section in $docData.sections) {
                            if ($section.testcases) {
                                $totalTests += $section.testcases.Count
                            }
                        }
                        Write-Host "Test Cases: $totalTests"
                        
                    } catch {
                        Write-Host "Document info: Available in $OUTPUT_FILE"
                    }
                    
                    Write-Host ""
                    Write-Host "🎉 Conversion completed successfully!" -ForegroundColor Green
                    exit 0
                } else {
                    throw "No valid JSON found in response"
                }
            } catch {
                Write-Host "❌ Error: Failed to parse JSON result - $_" -ForegroundColor Red
                Write-Host "Raw result (first 500 chars):"
                Write-Host $result.Substring(0, [Math]::Min(500, $result.Length))
                exit 1
            }
        }
        
        # Check if task failed
        if ($result -match '"state":\s*"FAILURE"') {
            Write-Host "❌ Processing failed" -ForegroundColor Red
            Write-Host "Error details:"
            Write-Host $result
            exit 1
        }
        
        # Show progress if available
        if ($result -match '"progress":\s*(\d+)') {
            $progress = $Matches[1]
        }
        if ($result -match '"status":\s*"([^"]+)"') {
            $status = $Matches[1]
        }
        
        if ($progress -and $status) {
            Write-Host "Progress: $progress% - $status"
        } else {
            Write-Host "Status: Processing..."
        }
        
    } catch {
        Write-Host "Error checking status: $_" -ForegroundColor Red
    }
    
    Start-Sleep 10
    $ATTEMPT++
}

Write-Host "❌ Timeout: Processing took too long" -ForegroundColor Red
exit 1
