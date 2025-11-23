import os
import sys
import argparse
from dotenv import load_dotenv
from crewai import Crew, Process
from crewai_ignore_manager.agents import FileAnalyzerAgent, ConfigUpdaterAgent
from crewai_ignore_manager.tasks import create_analysis_task, create_update_task

def main():
    parser = argparse.ArgumentParser(description="CrewAI File Management Automation Tool")
    parser.add_argument("mode", choices=["analyze", "update"], help="Mode of operation: analyze or update")
    parser.add_argument("path", nargs="?", default=os.getcwd(), help="Path to the project directory (default: current directory)")
    parser.add_argument("--key", help="OpenAI API Key (overrides OPENAI_API_KEY env var)")
    
    args = parser.parse_args()

    # Load environment variables from .env file if it exists
    load_dotenv()

    # Set API key if provided via CLI
    if args.key:
        os.environ["OPENAI_API_KEY"] = args.key
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is not set. Please set it in .env or pass it via --key.")
        sys.exit(1)

    directory_path = os.path.abspath(args.path)
    
    if args.mode == "analyze":
        print(f"Starting analysis on {directory_path}...")
        analyzer_agent = FileAnalyzerAgent()
        task = create_analysis_task(analyzer_agent, directory_path)
        crew = Crew(
            agents=[analyzer_agent],
            tasks=[task],
            verbose=True,
            process=Process.sequential
        )
        result = crew.kickoff()
        print("Analysis complete. Check project_root_artifact_review.md")

    elif args.mode == "update":
        print(f"Starting update based on review in {directory_path}...")
        updater_agent = ConfigUpdaterAgent()
        review_file_path = os.path.join(directory_path, "project_root_artifact_review.md")
        
        if not os.path.exists(review_file_path):
            print(f"Error: Review file not found at {review_file_path}. Run 'analyze' first.")
            sys.exit(1)
            
        task = create_update_task(updater_agent, review_file_path)
        crew = Crew(
            agents=[updater_agent],
            tasks=[task],
            verbose=True,
            process=Process.sequential
        )
        result = crew.kickoff()
        print("Update complete.")

if __name__ == "__main__":
    main()
