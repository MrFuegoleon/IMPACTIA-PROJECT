from scrapegraphai.graphs import SmartScraperGraph

# Define the configuration for the SmartScraperGraph
graph_config = {
    "llm": {
        "model": "ollama/mistral",
        "temperature": 0,
        "format": "json",  # Ollama needs the format to be specified explicitly
        "base_url": "http://localhost:11434",  # set Ollama URL
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "base_url": "http://localhost:11434",  # set Ollama URL
    },
    "verbose": True,
}

# Create an instance of SmartScraperGraph
smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the projects with their descriptions",
    source="https://perinim.github.io/projects",  # URL to scrape data from
    config=graph_config
)

try:
    # Run the SmartScraperGraph to get the result
    result = smart_scraper_graph.run()
    print(result)
except ValueError as e:
    # Catch and print any ValueErrors, which may include the 404 error
    print(f"An error occurred: {e}")
except Exception as e:
    # Catch and print any other exceptions
    print(f"An unexpected error occurred: {e}")

# Additional step to pull the model if it's not found
# This is hypothetical and depends on your specific setup
def pull_model(model_name):
    import subprocess
    try:
        subprocess.run(['ollama-cli', 'pull', model_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull the model {model_name}: {e}")

# Check if the model needs to be pulled
pull_model('ollama/nomic-embed-text')
