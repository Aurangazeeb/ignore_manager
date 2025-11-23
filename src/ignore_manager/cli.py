import os
import sys
import argparse
from dotenv import load_dotenv
from crewai import Crew, Process
from ignore_manager.agents import FileAnalyzerAgent, ConfigUpdaterAgent
from ignore_manager.tasks import create_analysis_task, create_update_task

def main():
    parser = argparse.ArgumentParser(description="CrewAI File Management Automation Tool")
    parser.add_argument("mode", choices=["analyze", "update"], help="Mode of operation: analyze or update")
    parser.add_argument("path", nargs="?", default=os.getcwd(), help="Path to the project directory (default: current directory)")
    parser.add_argument("--key", help="OpenAI API Key (overrides OPENAI_API_KEY env var)")
    parser.add_argument("-g", "--gitignore", action="store_true", help="Scan/Update only .gitignore")
    parser.add_argument("-d", "--dockerignore", action="store_true", help="Scan/Update only .dockerignore")
    
    args = parser.parse_args()

    # Determine files to ignore
    files_to_ignore = []
    if args.gitignore:
        files_to_ignore.append('.gitignore')
    if args.dockerignore:
        files_to_ignore.append('.dockerignore')
    
    # Default to both if neither is specified
    if not files_to_ignore:
        files_to_ignore = ['.gitignore', '.dockerignore']

    # Determine output filename
    if len(files_to_ignore) == 2:
        output_file = f"{args.path}/project_root_artifact_review.md"
    elif '.gitignore' in files_to_ignore:
        output_file = f"{args.path}/project_root_artifact_review_g.md"
    else:
        output_file = f"{args.path}/project_root_artifact_review_d.md"

    # Handle API Key
    api_key = args.key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OpenAI API Key is required. Set OPENAI_API_KEY env var or pass --key")
        return

    os.environ["OPENAI_API_KEY"] = api_key

    # Initialize Agents
    analyzer = FileAnalyzerAgent()
    updater = ConfigUpdaterAgent()

    if args.mode == "analyze":
        print(f"Analyzing {args.path} for {', '.join(files_to_ignore)}...")
        task = create_analysis_task(analyzer, args.path, files_to_ignore, output_file)
        crew = Crew(
            agents=[analyzer],
            tasks=[task],
            verbose=True,
            process=Process.sequential
        )
        result = crew.kickoff()
        print(f"\nAnalysis complete. Check {output_file}")

    elif args.mode == "update":
        review_file_path = os.path.join(args.path, output_file)
        if not os.path.exists(review_file_path):
             print(f"Error: Review file not found at {review_file_path}. Run 'analyze' first.")
             return

        print(f"Updating configuration in {args.path} based on {output_file}...")
        task = create_update_task(updater, review_file_path, files_to_ignore)
        crew = Crew(
            agents=[updater],
            tasks=[task],
            verbose=True,
            process=Process.sequential
        )
        result = crew.kickoff()
        print("\nUpdate complete.")

if __name__ == "__main__":
    main()
