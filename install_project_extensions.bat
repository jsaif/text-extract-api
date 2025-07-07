@echo off
echo Installing VS Code Extensions for text-extract-api Project
echo =======================================================

echo.
echo 🔍 Analyzing your project...
echo   • FastAPI web framework
echo   • EasyOCR computer vision
echo   • Celery distributed tasks
echo   • Redis caching
echo   • Docker containers
echo   • AI/ML dependencies (transformers, ollama)
echo   • Python 3.10.11

echo.
echo 📦 Installing Essential Extensions...

echo.
echo 🐍 Python Development Extensions
code --install-extension ms-python.python
code --install-extension ms-python.pylint
code --install-extension ms-python.flake8
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort

echo.
echo 🚀 FastAPI/Web Development Extensions
code --install-extension ms-python.debugpy
code --install-extension ms-toolsai.jupyter
code --install-extension ms-vscode.vscode-json
code --install-extension ms-vscode.vscode-yaml
code --install-extension redhat.vscode-yaml

echo.
echo 🐳 Docker & Container Extensions
code --install-extension ms-vscode-remote.remote-containers
code --install-extension ms-azuretools.vscode-docker

echo.
echo 🤖 AI/ML Development Extensions
code --install-extension Continue.continue
code --install-extension ms-vscode.ollama
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat

echo.
echo 📊 Data & API Extensions
code --install-extension humao.rest-client
code --install-extension rangav.vscode-thunder-client
code --install-extension ms-vscode.vscode-json

echo.
echo 🔧 Development Tools
code --install-extension GitLens.gitlens
code --install-extension streetsidesoftware.code-spell-checker
code --install-extension ms-vscode.vscode-todo-highlight
code --install-extension aaron-bond.better-comments

echo.
echo 🎨 UI/UX Enhancement
code --install-extension PKief.material-icon-theme
code --install-extension Gruntfuggly.todo-tree
code --install-extension oderwat.indent-rainbow
code --install-extension ms-vscode.vscode-edge-devtools

echo.
echo 📋 Project-Specific Extensions
code --install-extension ms-vscode.powershell
code --install-extension ms-vscode.vscode-typescript-next
code --install-extension ms-vscode.hexeditor

echo.
echo ✅ Installation Complete!
echo.
echo 🎯 Key Extensions Installed:
echo   • Python development suite
echo   • FastAPI/web development tools
echo   • Docker container support
echo   • AI/ML development tools
echo   • API testing tools
echo   • Git integration
echo   • Code quality tools

echo.
echo 💡 Next Steps:
echo   1. Restart VS Code
echo   2. Open your project folder
echo   3. Configure Python interpreter
echo   4. Set up Continue extension for AI assistance
echo   5. Configure Docker integration

echo.
echo 🚀 Your text-extract-api project is now fully equipped!
pause
