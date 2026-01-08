"""
Example usage of the Snippet2README generator as a Python module.
"""

from snippet2readme import ReadmeGenerator

def example_programmatic_usage():
    """Example: Using the generator programmatically."""
    
    # Initialize the generator with Ollama (no API key needed)
    generator = ReadmeGenerator(provider="ollama", model="llama3")
    
    # Generate a README
    readme = generator.generate_readme(
        description="A Python script that scrapes Amazon prices and saves them to CSV",
        project_name="AmazonPriceScraper",
        language="Python",
        license_type="MIT",
        scan_files=True,
        directory="."
    )
    
    # Save to file
    filepath = generator.save_readme(readme, directory=".", filename="EXAMPLE_README.md")
    
    print(f"README generated and saved to: {filepath}")
    print("\nContent preview:")
    print(readme[:300] + "...")


if __name__ == "__main__":
    example_programmatic_usage()
