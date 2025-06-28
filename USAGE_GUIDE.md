# 📖 TEXT-EXTRACT-API Usage Guide

Your TEXT-EXTRACT-API is now running and ready to use! Here are all the ways you can interact with it:

## 🚀 Quick Start (30 seconds)

**Before you begin, make sure Redis is running:**

1. **Start Redis** (choose one):
   ```powershell
   # Easy way - double-click this file:
   .\start_redis.bat
   
   # OR manual way:
   docker run -d --name redis-text-extract -p 6379:6379 --restart always redis
   ```

2. **Start the API server**:
   ```powershell
   # Easy way - double-click this file:
   .\start_server.bat
   
   # OR manual way:
   .\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Open your browser** to: **http://localhost:8000/docs**

4. **Upload a test file** and see the magic happen!

---

## 🌐 Web Interface (Easiest Way)

### 1. Open the API Documentation
Visit: **http://localhost:8000/docs**

This gives you an interactive web interface where you can:
- Upload files directly through your browser
- Test different API endpoints
- See real-time results
- No command line needed!

### 2. Try the Interactive Demo
1. Go to http://localhost:8000/docs
2. Click on **POST /ocr/upload**
3. Click **"Try it out"**
4. Upload a file (PDF, image, Word doc, etc.)
5. Click **"Execute"**
6. See the extracted text immediately!

## 💻 Command Line Interface (CLI)

Open a new PowerShell window and navigate to your project:

```powershell
cd "c:\Users\Jubi\text-extract-api"
```

### Basic OCR (Extract Text to Markdown)

```powershell
# Extract text from a PDF
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-invoice.pdf

# Extract text from an image
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file your-image.jpg

# Extract with caching (faster for repeated processing)
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-invoice.pdf --ocr_cache
```

### Advanced AI Processing

```powershell
# Remove personal information from documents
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-mri.pdf --prompt_file examples\example-mri-remove-pii.txt

# Convert document to structured JSON
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-mri.pdf --prompt_file examples\example-mri-2-json-prompt.txt

# Process with specific OCR strategy (case-insensitive)
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file your-document.pdf --strategy easyocr
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file your-document.pdf --strategy llama_vision
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file your-document.pdf --strategy minicpm_v
```

### Multiple Languages

```powershell
# Process document in multiple languages
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file your-document.pdf --language en,es,fr
```

## 🔧 API Endpoints (for Developers)

If you're building your own application, use these HTTP endpoints:

### Upload and Process File
```http
POST http://localhost:8000/ocr/upload
Content-Type: multipart/form-data

# Upload file with form data
```

### Get Processing Results
```http
GET http://localhost:8000/ocr/result/{task_id}
```

### Check Available Models
```http
GET http://localhost:8000/llm/models
```

### Clear Cache
```http
POST http://localhost:8000/ocr/clear_cache
```

## 📁 File Formats Supported

✅ **Documents**: PDF, DOCX, PPTX, TXT
✅ **Images**: JPG, PNG, TIFF, BMP, GIF
✅ **Scanned Documents**: Any image-based PDF
✅ **Screenshots**: Any image format

## 📁 File Organization

### Where to Place Your Documents

#### **1. Examples Folder (Recommended for Testing)**
```
c:\Users\Jubi\text-extract-api\examples\
```
- Place test documents alongside existing examples
- Use relative paths: `--file examples\your-document.pdf`
- Includes sample prompt files

#### **2. Documents Folder (For Regular Use)**
```
c:\Users\Jubi\text-extract-api\documents\
```
- Organize your documents by type or project
- Keep your files separate from examples
- Use relative paths: `--file documents\your-document.pdf`

#### **3. Absolute Paths (Any Location)**
```powershell
# Process files from anywhere on your computer
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file "C:\Users\YourName\Desktop\network-test.pdf" --strategy llama_vision
```

### **For Network Testing Documents:**
```powershell
# Copy your network test document to the examples folder
copy "C:\path\to\your\network-test.pdf" "c:\Users\Jubi\text-extract-api\examples\"

# Then process it with the custom network prompt
cd "c:\Users\Jubi\text-extract-api"
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\network-test.pdf --strategy llama_vision --prompt_file examples\network-testing-prompt.txt

# The CLI will show a task ID, then processing progress, and finally results
# Results are also saved to: .\storage\extracted-filename.md
```

## 🎯 Common Use Cases

### 1. **Invoice Processing**
```powershell
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file invoice.pdf --prompt_file custom-prompts\extract-invoice-data.txt
```

### 2. **Medical Records**
```powershell
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file medical-report.pdf --prompt_file examples\example-mri-remove-pii.txt
```

### 3. **Receipt Scanning**
```powershell
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file receipt.jpg --strategy easyocr
```

### 4. **Document Digitization**
```powershell
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file scanned-document.pdf --ocr_cache
```

### 5. **Network Testing Reports**
```powershell
# Extract structured network test data with technical accuracy
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file network-test-report.pdf --strategy llama_vision --prompt_file examples\network-testing-prompt.txt

# Quick extraction for simple network documents
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file network-config.pdf --strategy easyocr
```

## 🔍 Check System Status

```powershell
# Verify all components are running
.\.venv\Scripts\python.exe system_status.py
```

## 📊 Output Options

### Save Results to File
```powershell
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file document.pdf --storage_profile default --storage_filename "extracted-{file_name}.md"
```

### Get Results in Different Formats
- **Markdown**: Default output format
- **JSON**: Use `--prompt_file` with JSON formatting prompts
- **Plain Text**: Process through custom prompts

## 🚀 Quick Start Examples

### Example 1: Extract Text from Invoice
```powershell
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-invoice.pdf
```

### Example 2: Process Medical Document (Remove PII)
```powershell
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-mri.pdf --prompt_file examples\example-mri-remove-pii.txt
```

### Example 3: Convert to Structured JSON
```powershell
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-mri.pdf --prompt_file examples\example-mri-2-json-prompt.txt
```

## 🛠️ Advanced Configuration

### Custom Prompts
Create your own prompt files in the `examples` folder:

```text
# my-custom-prompt.txt
Extract only the following information from this document:
- Names
- Dates
- Amounts
- Phone numbers

Format the output as JSON.
```

Then use it:
```powershell
.\.venv\Scripts\python.exe client\cli.py ocr_upload --file document.pdf --prompt_file my-custom-prompt.txt
```

## 📈 Performance Tips

1. **Use caching** with `--ocr_cache` for faster repeated processing
2. **Choose the right strategy**:
   - `easyocr`: Fastest, good for English
   - `llama_vision`: Most accurate, slower
   - `minicpm_v`: Good balance
3. **Process in batches** for multiple files
4. **Use appropriate image resolution** (higher = more accurate but slower)

## 🔧 Troubleshooting

### Common Issues and Solutions

#### "Redis Connection Error" or "getaddrinfo failed"
✅ **FIXED** - The Redis hostname configuration has been updated to use localhost instead of Docker hostnames.

This error means Redis is not running or not accessible:

```
redis.exceptions.ConnectionError: Error 11001 connecting to redis:6379. getaddrinfo failed.
```

**Fix Steps:**
1. **Easy Start - Use the batch file**:
   ```powershell
   # Double-click or run in PowerShell:
   .\start_redis.bat
   ```

2. **Manual Redis setup**:
   ```powershell
   # Start Docker Desktop first, then:
   docker run -d --name redis-text-extract -p 6379:6379 --restart always redis
   ```

3. **Check if Redis is running**:
   ```powershell
   docker ps  # Should show redis container
   # OR test connection:
   .\.venv\Scripts\python.exe test_redis.py
   ```

4. **If Docker is not available**, install Redis for Windows:
   - Download from: https://github.com/microsoftarchive/redis/releases
   - Or use Windows Subsystem for Linux (WSL)

**Note**: The configuration files have been updated to use `localhost:6379` instead of `redis:6379` for Windows compatibility.

#### "Internal Server Error" during processing
This usually indicates a server-side issue during document processing:

**Quick Fixes:**
1. **Check server logs** - Look at your FastAPI terminal for detailed error messages
2. **Try a simpler approach first**:
   ```powershell
   # Test without custom prompt
   .\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\example-invoice.pdf --strategy easyocr
   
   # If that works, try your document with easyocr
   .\.venv\Scripts\python.exe client\cli.py ocr_upload --file examples\EVO_Fundamentals_V1.2.pdf --strategy easyocr
   ```
3. **Check Ollama connection**:
   ```powershell
   ollama list  # Verify models are available
   curl http://localhost:11434/api/tags  # Test Ollama API
   ```
4. **Restart services**:
   ```powershell
   # Restart Ollama
   ollama serve
   
   # Restart FastAPI (Ctrl+C then restart)
   .\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### "Bad Request: Unknown strategy" or "Validation Error"
✅ **FIXED** - Strategy validation has been improved:
- Strategy names are now case-insensitive
- Leading/trailing spaces are automatically trimmed
- Duplicate strategies are prevented

**Available strategies**: `easyocr`, `llama_vision`, `minicpm_v`, `docling`, `remote`

#### "TypeError: DoclingStrategy.name() missing 1 required positional argument"
✅ **FIXED** - This strategy loading issue has been resolved in the codebase.

#### General Troubleshooting Steps:
1. **Check system status**: `.\.venv\Scripts\python.exe system_status.py`
2. **Verify services are running**: Redis, Ollama, FastAPI
3. **Check file permissions**: Make sure files are accessible
4. **Restart services** if needed:
   ```powershell
   # Restart FastAPI
   cd "c:\Users\Jubi\text-extract-api"
   .\.venv\Scripts\python.exe -m uvicorn text_extract_api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### If OCR processing fails:
- Try different strategies: `--strategy easyocr`, `--strategy llama_vision`
- Check file format is supported
- Verify Ollama models are downloaded: `ollama list`
- Ensure Redis is running: `docker ps`

#### If uploads fail:
- Check file size (large files may take longer)
- Verify file isn't corrupted
- Try with example files first
- Check API logs for detailed error messages

---

## 🎉 You're Ready to Go!

Start with the web interface at **http://localhost:8000/docs** - it's the easiest way to get familiar with the API!

Try uploading one of the example files first to see how it works.
