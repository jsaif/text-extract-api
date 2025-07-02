@echo off
echo Setting up GPU-accelerated AI extensions for VS Code...
echo ======================================================

echo.
echo 🔍 Checking VS Code installation...
where code >nul 2>nul
if %errorlevel% == 0 (
    echo ✅ VS Code found
    code --version
) else (
    echo ❌ VS Code not found in PATH
    echo Please install VS Code and add it to PATH
    pause
    exit /b 1
)

echo.
echo 🤖 Installing AI-powered VS Code extensions...

echo.
echo Installing Continue (Local AI Assistant)...
code --install-extension Continue.continue

echo Installing Ollama for VS Code...
code --install-extension ms-vscode.ollama

echo Installing GitHub Copilot Chat...
code --install-extension GitHub.copilot-chat

echo Installing GitHub Copilot...
code --install-extension GitHub.copilot

echo Installing TabNine...
code --install-extension TabNine.tabnine-vscode

echo Installing IntelliCode...
code --install-extension VisualStudioExptTeam.vscodeintellicode

echo Installing Python support...
code --install-extension ms-python.python

echo Installing Jupyter support...
code --install-extension ms-toolsai.jupyter

echo.
echo 🧠 Checking for Ollama (Local AI models)...
where ollama >nul 2>nul
if %errorlevel% == 0 (
    echo ✅ Ollama found
    ollama --version
    
    echo.
    echo 📦 Installing recommended AI models...
    echo Installing CodeLlama (7B) - Best for code generation...
    ollama pull codellama:7b
    
    echo Installing DeepSeek Coder (1.3B) - Fast autocomplete...
    ollama pull deepseek-coder:1.3b
    
    echo Installing DeepSeek Coder (6.7B) - Better accuracy...
    ollama pull deepseek-coder:6.7b
    
    echo.
    echo 🚀 Starting Ollama server...
    start /b ollama serve
    timeout /t 3 /nobreak >nul
    
    echo.
    echo 🧪 Testing Ollama connection...
    ollama list
    
) else (
    echo ❌ Ollama not found
    echo.
    echo 💡 To install Ollama:
    echo 1. Download from: https://ollama.ai/
    echo 2. Install and restart terminal
    echo 3. Run this script again
)

echo.
echo 🐍 Checking Python AI libraries...
python -c "import torch; print(f'PyTorch: {torch.__version__}')" 2>nul || echo "❌ PyTorch not installed"
python -c "import transformers; print(f'Transformers: {transformers.__version__}')" 2>nul || echo "❌ Transformers not installed"
python -c "import easyocr; print(f'EasyOCR: {easyocr.__version__}')" 2>nul || echo "❌ EasyOCR not installed"

echo.
echo 📁 Creating Continue configuration...
if not exist "%USERPROFILE%\.continue" mkdir "%USERPROFILE%\.continue"

echo {                                                                     > "%USERPROFILE%\.continue\config.json"
echo   "models": [                                                        >> "%USERPROFILE%\.continue\config.json"
echo     {                                                                >> "%USERPROFILE%\.continue\config.json"
echo       "title": "CodeLlama",                                          >> "%USERPROFILE%\.continue\config.json"
echo       "provider": "ollama",                                          >> "%USERPROFILE%\.continue\config.json"
echo       "model": "codellama:7b",                                       >> "%USERPROFILE%\.continue\config.json"
echo       "apiBase": "http://localhost:11434"                           >> "%USERPROFILE%\.continue\config.json"
echo     },                                                               >> "%USERPROFILE%\.continue\config.json"
echo     {                                                                >> "%USERPROFILE%\.continue\config.json"
echo       "title": "DeepSeek Coder",                                     >> "%USERPROFILE%\.continue\config.json"
echo       "provider": "ollama",                                          >> "%USERPROFILE%\.continue\config.json"
echo       "model": "deepseek-coder:6.7b",                               >> "%USERPROFILE%\.continue\config.json"
echo       "apiBase": "http://localhost:11434"                           >> "%USERPROFILE%\.continue\config.json"
echo     }                                                                >> "%USERPROFILE%\.continue\config.json"
echo   ],                                                                 >> "%USERPROFILE%\.continue\config.json"
echo   "tabAutocompleteModel": {                                          >> "%USERPROFILE%\.continue\config.json"
echo     "title": "Fast Autocomplete",                                    >> "%USERPROFILE%\.continue\config.json"
echo     "provider": "ollama",                                            >> "%USERPROFILE%\.continue\config.json"
echo     "model": "deepseek-coder:1.3b",                                  >> "%USERPROFILE%\.continue\config.json"
echo     "apiBase": "http://localhost:11434"                             >> "%USERPROFILE%\.continue\config.json"
echo   }                                                                  >> "%USERPROFILE%\.continue\config.json"
echo }                                                                    >> "%USERPROFILE%\.continue\config.json"

echo ✅ Continue configuration created

echo.
echo 🎉 AI Extension Setup Complete!
echo ================================

echo.
echo 📋 What was installed:
echo ✅ Continue - Local AI assistant with GPU support
echo ✅ Ollama - Local LLM server integration
echo ✅ GitHub Copilot - AI pair programming
echo ✅ TabNine - AI code completions
echo ✅ IntelliCode - AI-enhanced IntelliSense
echo ✅ Python & Jupyter support

echo.
echo 🚀 Next steps:
echo 1. Restart VS Code to activate extensions
echo 2. Open a Python file to test AI features
echo 3. Use Ctrl+I (Continue) for AI assistance
echo 4. Use Ctrl+Shift+P and search "Continue" for commands
echo 5. Configure GitHub Copilot if you have a subscription

echo.
echo 💡 Pro tips:
echo • Use Continue for code generation and explanations
echo • Try "Explain this code" in Continue chat
echo • Use Tab for AI completions
echo • Install GPU drivers for 5-100x speed boost

echo.
echo 🔗 Useful resources:
echo • Continue docs: https://continue.dev/docs
echo • Ollama models: https://ollama.ai/library
echo • GPU setup guide: GPU_SETUP_GUIDE.md

echo.
pause
