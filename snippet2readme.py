#!/usr/bin/env python3
"""
Snippet2README - AI-Powered README Generator
Transforms minimal project descriptions into comprehensive README files.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
import inquirer
from openai import OpenAI
import ollama
from dotenv import load_dotenv


class ReadmeGenerator:
    """Main class for generating README files using AI."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini", provider: str = "ollama"):
        """
        Initialize the README generator.
        
        Args:
            api_key: OpenAI API key (if None, loads from environment) - only needed for OpenAI
            model: Model to use (default: gpt-4o-mini for OpenAI, llama3 for Ollama)
            provider: AI provider to use - "openai" or "ollama" (default: ollama)
        """
        load_dotenv()
        self.provider = provider or os.getenv("AI_PROVIDER", "ollama")
        self.model = model or os.getenv("MODEL_NAME", "llama3" if self.provider == "ollama" else "gpt-4o-mini")
        
        if self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "OpenAI API key not found. Please set OPENAI_API_KEY in .env file "
                    "or pass it as an argument."
                )
            self.client = OpenAI(api_key=self.api_key)
        elif self.provider == "ollama":
            self.client = None  # Ollama doesn't need a client object like OpenAI
        else:
            raise ValueError(f"Unsupported provider: {self.provider}. Use 'openai' or 'ollama'.")
        
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Return the system prompt that defines AI behavior."""
        return """You are a Senior Technical Writer specializing in creating professional GitHub README files.

Your task is to transform minimal project descriptions into comprehensive, well-structured README.md files.

REQUIREMENTS:
- Write in clear, professional Markdown
- Use appropriate emoji icons sparingly and tastefully
- Include these sections: Title, Description, Features, Tech Stack, Installation, Usage, Configuration (if needed), License
- Make the content engaging and informative
- Assume best practices for the technology stack
- Include code blocks with proper syntax highlighting
- Add badges if appropriate (build status, license, version)
- Keep the tone professional but approachable

STRUCTURE:
1. Title with project name (use # header)
2. Brief description (2-3 sentences)
3. Features (bulleted list, 5-8 key features)
4. Tech Stack (technologies used)
5. Installation (step-by-step)
6. Usage (with examples)
7. Configuration (if applicable)
8. Contributing (optional, brief)
9. License

OUTPUT:
- Return ONLY the Markdown content
- No additional commentary or explanations
- Ready to save as README.md"""

    def scan_project_files(self, directory: str = ".") -> dict:
        """
        Scan the project directory to gather context about the project.
        
        Args:
            directory: Path to the project directory
            
        Returns:
            Dictionary containing project information
        """
        project_path = Path(directory)
        info = {
            "files": [],
            "has_requirements": False,
            "has_package_json": False,
            "has_dockerfile": False,
            "has_tests": False,
            "language": "Unknown"
        }
        
        # Common file patterns to look for
        patterns = {
            "*.py": "Python",
            "*.js": "JavaScript",
            "*.ts": "TypeScript",
            "*.java": "Java",
            "*.go": "Go",
            "*.rs": "Rust",
            "*.dart": "Dart/Flutter"
        }
        
        try:
            # Get list of files (non-recursive for top level)
            for item in project_path.iterdir():
                if item.is_file():
                    info["files"].append(item.name)
                    
                    # Check for specific files
                    if item.name == "requirements.txt":
                        info["has_requirements"] = True
                        info["language"] = "Python"
                    elif item.name == "package.json":
                        info["has_package_json"] = True
                        info["language"] = "JavaScript/TypeScript"
                    elif item.name == "Dockerfile":
                        info["has_dockerfile"] = True
                    elif "test" in item.name.lower():
                        info["has_tests"] = True
                    
                    # Detect language from file extensions
                    for pattern, lang in patterns.items():
                        if item.match(pattern) and info["language"] == "Unknown":
                            info["language"] = lang
        
        except Exception as e:
            print(f"Warning: Could not scan directory: {e}")
        
        return info

    def generate_readme(
        self, 
        description: str, 
        project_name: str,
        language: Optional[str] = None,
        license_type: str = "MIT",
        scan_files: bool = True,
        directory: str = "."
    ) -> str:
        """
        Generate a README file using AI.
        
        Args:
            description: Minimal project description
            project_name: Name of the project
            language: Programming language (optional)
            license_type: License type (default: MIT)
            scan_files: Whether to scan project files for context
            directory: Project directory to scan
            
        Returns:
            Generated README content as Markdown string
        """
        # Scan project files if requested
        project_info = {}
        if scan_files:
            project_info = self.scan_project_files(directory)
            if language is None and project_info["language"] != "Unknown":
                language = project_info["language"]
        
        # Build the user prompt
        user_prompt = f"""Create a professional README.md for this project:

Project Name: {project_name}
Description: {description}
Primary Language: {language or 'Not specified'}
License: {license_type}
"""
        
        # Add file context if available
        if project_info and project_info["files"]:
            user_prompt += f"\nProject Files Found: {', '.join(project_info['files'][:10])}"
            if project_info["has_requirements"]:
                user_prompt += "\n- Uses requirements.txt for Python dependencies"
            if project_info["has_package_json"]:
                user_prompt += "\n- Uses package.json for Node.js dependencies"
            if project_info["has_dockerfile"]:
                user_prompt += "\n- Includes Docker support"
            if project_info["has_tests"]:
                user_prompt += "\n- Has test files"
        
        try:
            # Call AI API based on provider
            print(f"\n🤖 Generating README with {self.provider}/{self.model}...")
            
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                readme_content = response.choices[0].message.content
            
            elif self.provider == "ollama":
                response = ollama.chat(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    options={
                        "temperature": 0.7,
                    }
                )
                readme_content = response['message']['content']
            
            # Ensure it's clean Markdown
            readme_content = readme_content.strip()
            
            return readme_content
            
        except Exception as e:
            raise Exception(f"Failed to generate README: {str(e)}")

    def save_readme(self, content: str, directory: str = ".", filename: str = "README.md") -> str:
        """
        Save the generated README to a file.
        
        Args:
            content: README content to save
            directory: Directory to save the file in
            filename: Name of the file (default: README.md)
            
        Returns:
            Path to the saved file
        """
        filepath = Path(directory) / filename
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return str(filepath)
        except Exception as e:
            raise Exception(f"Failed to save README: {str(e)}")


def interactive_mode():
    """Run the generator in interactive CLI mode."""
    print("=" * 60)
    print("✨ Snippet2README - AI-Powered README Generator")
    print("=" * 60)
    print()
    
    # Questions for the user
    questions = [
        inquirer.List(
            'provider',
            message="Which AI provider do you want to use?",
            choices=['ollama', 'openai'],
            default='ollama',
        ),
        inquirer.Text(
            'project_name',
            message="What is your project name?",
            validate=lambda _, x: len(x) > 0,
        ),
        inquirer.Text(
            'description',
            message="Describe your project in one sentence",
            validate=lambda _, x: len(x) > 10,
        ),
        inquirer.List(
            'language',
            message="What is the primary programming language?",
            choices=['Python', 'JavaScript', 'TypeScript', 'Java', 'Go', 'Rust', 'Dart/Flutter', 'Other'],
        ),
        inquirer.List(
            'license',
            message="What license do you want to use?",
            choices=['MIT', 'Apache-2.0', 'GPL-3.0', 'BSD-3-Clause', 'Unlicense'],
            default='MIT',
        ),
        inquirer.Confirm(
            'scan_files',
            message="Scan current directory for project files?",
            default=True,
        ),
    ]
    
    try:
        answers = inquirer.prompt(questions)
        
        if not answers:
            print("\n❌ Operation cancelled.")
            return
        
        # Initialize generator with selected provider
        generator = ReadmeGenerator(provider=answers['provider'])
        
        # Generate README
        readme_content = generator.generate_readme(
            description=answers['description'],
            project_name=answers['project_name'],
            language=answers['language'],
            license_type=answers['license'],
            scan_files=answers['scan_files'],
            directory="."
        )
        
        # Save README
        filepath = generator.save_readme(readme_content, directory=".")
        
        print(f"\n✅ README.md generated successfully!")
        print(f"📄 Saved to: {filepath}")
        print(f"\n📊 Preview:")
        print("-" * 60)
        print(readme_content[:500] + "..." if len(readme_content) > 500 else readme_content)
        print("-" * 60)
        
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Snippet2README - Transform minimal descriptions into comprehensive READMEs"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode (default)"
    )
    parser.add_argument(
        "-n", "--name",
        type=str,
        help="Project name"
    )
    parser.add_argument(
        "-d", "--description",
        type=str,
        help="Project description"
    )
    parser.add_argument(
        "-l", "--language",
        type=str,
        help="Primary programming language"
    )
    parser.add_argument(
        "--license",
        type=str,
        default="MIT",
        help="License type (default: MIT)"
    )
    parser.add_argument(
        "--no-scan",
        action="store_true",
        help="Don't scan project files"
    )
    
    args = parser.parse_args()
    
    # If no arguments or interactive flag, use interactive mode
    if args.interactive or (not args.name and not args.description):
        interactive_mode()
    else:
        # Command-line mode
        if not args.name or not args.description:
            parser.error("--name and --description are required in non-interactive mode")
        
        try:
            generator = ReadmeGenerator()
            
            readme_content = generator.generate_readme(
                description=args.description,
                project_name=args.name,
                language=args.language,
                license_type=args.license,
                scan_files=not args.no_scan,
                directory="."
            )
            
            filepath = generator.save_readme(readme_content, directory=".")
            
            print(f"✅ README.md generated successfully!")
            print(f"📄 Saved to: {filepath}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
