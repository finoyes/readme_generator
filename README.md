# ✨ Snippet2README - AI-Powered README Generator

Transform minimal project descriptions into comprehensive, professional README files using AI.

## 🎯 Overview

**Snippet2README** is an intelligent CLI tool that takes a simple one-sentence project description and generates a complete, well-structured README.md file. Perfect for developers who want to save time on documentation while maintaining professional standards.

### The Problem
Writing good README files is time-consuming. You want to focus on coding, not formatting documentation.

### The Solution
Describe your project in one sentence → Get a production-ready README in seconds.

## ✨ Features

- 🤖 **AI-Powered Generation** - Uses OpenAI GPT-4o-mini for intelligent content creation
- 💬 **Interactive CLI** - User-friendly prompts guide you through the process
- 🔍 **Smart File Scanning** - Automatically detects your tech stack from project files
- 📝 **Professional Structure** - Generates Title, Description, Features, Installation, Usage, and more
- 🎨 **Clean Markdown** - Output is properly formatted and ready to commit
- ⚙️ **Flexible Usage** - Use interactively or programmatically in your scripts
- 🔐 **Secure** - API keys stored safely in .env files
- 🚀 **Fast & Cheap** - Uses efficient gpt-4o-mini model

## 🛠 Tech Stack

- **Python 3.8+**
- **OpenAI API** (GPT-4o-mini)
- **Libraries:**
  - `openai` - API integration
  - `python-dotenv` - Environment management
  - `inquirer` - Interactive CLI prompts

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/snippet2readme.git
cd snippet2readme
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

> **Get your API key:** Visit [OpenAI API Keys](https://platform.openai.com/api-keys)

## 🚀 Usage

### Interactive Mode (Recommended)

Simply run the script and follow the prompts:

```bash
python snippet2readme.py
```

You'll be asked:
- Project name
- One-sentence description
- Primary programming language
- License type
- Whether to scan project files

**Example:**

```
✨ Snippet2README - AI-Powered README Generator
============================================================

? What is your project name? AmazonPriceScraper
? Describe your project in one sentence: A Python script that scrapes Amazon prices and saves them to CSV
? What is the primary programming language? Python
? What license do you want to use? MIT
? Scan current directory for project files? Yes

🤖 Generating README with gpt-4o-mini...
✅ README.md generated successfully!
📄 Saved to: README.md
```

### Command-Line Mode

For automation or scripts:

```bash
python snippet2readme.py \
  --name "TaskTrackerPro" \
  --description "A productivity app for students with deadline alerts" \
  --language "Python" \
  --license "MIT"
```

### Programmatic Usage

Use it as a Python module in your own scripts:

```python
from snippet2readme import ReadmeGenerator

generator = ReadmeGenerator()

readme = generator.generate_readme(
    description="A task tracker for students",
    project_name="StudentTaskFlow",
    language="Python",
    license_type="MIT"
)

generator.save_readme(readme, directory=".")
```

## 📖 Example Output

**Input:**
```
Description: "A Python script that scrapes Amazon prices and saves them to CSV"
Project Name: "AmazonPriceScraper"
```

**Output:** A complete README with:
- Professional title and description
- Feature list (Custom deadline alerts, Semester-based sorting, etc.)
- Installation instructions
- Usage examples with code blocks
- Configuration details
- License information

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | *Required* |
| `MODEL_NAME` | OpenAI model to use | `gpt-4o-mini` |

### Custom System Prompt

Edit the `_get_system_prompt()` method in [snippet2readme.py](snippet2readme.py) to customize the AI's behavior and output structure.

## 🎓 Resume-Worthy Skills Demonstrated

This project showcases:
- ✅ **AI Integration** - Working with external APIs (OpenAI)
- ✅ **CLI Development** - Creating user-friendly command-line tools
- ✅ **File I/O & Automation** - Scanning directories and generating files
- ✅ **API Security** - Safe handling of API keys with environment variables
- ✅ **JSON Processing** - Working with API responses
- ✅ **Developer Tools** - Creating utilities that provide immediate value

## 🔮 Future Enhancements

- [ ] Support for Ollama (local, free AI models)
- [ ] Template customization system
- [ ] Multi-language README generation (Spanish, French, etc.)
- [ ] GitHub integration (auto-commit generated README)
- [ ] Web interface version
- [ ] Analysis of existing code files to extract features automatically
- [ ] Support for generating other documentation (CONTRIBUTING.md, CODE_OF_CONDUCT.md)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the GPT API
- The Python community for excellent libraries
- All developers who believe good documentation matters

---

**Made with ❤️ by developers, for developers**

*Stop spending hours on README files. Let AI do the heavy lifting while you focus on code.*
