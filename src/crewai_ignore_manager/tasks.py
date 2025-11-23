from crewai import Task
from crewai_ignore_manager.agents import FileAnalyzerAgent, ConfigUpdaterAgent

def create_analysis_task(agent, directory_path):
    return Task(
        description=f"""Scan the directory at {directory_path}. 
        Identify all files and directories. 
        Read the existing .gitignore and .dockerignore files if they exist.
        Determine which files are generated files or development artifacts that should be ignored in production.
        Compare your findings with the existing rules.
        Create a markdown file named 'project_root_artifact_review.md' in the current directory.
        The file should list the recommended rules for .gitignore and .dockerignore with a justification for each.
        If a rule already exists, note it but don't duplicate it in the final update list unless necessary for clarity.
        Format the file as follows:
        
        # Project Root Artifact Review
        
        ## Recommended .gitignore rules
        - [ ] rule1 # justification (New/Existing)
        - [ ] rule2 # justification (New/Existing)
        
        ## Recommended .dockerignore rules
        - [ ] rule1 # justification (New/Existing)
        - [ ] rule2 # justification (New/Existing)
        """,
        expected_output="A markdown file named 'project_root_artifact_review.md' containing recommended ignore rules.",
        agent=agent,
        output_file=f"{directory_path}/project_root_artifact_review.md"
    )

def create_update_task(agent, review_file_path):
    return Task(
        description=f"""Read the review file at {review_file_path}.
        Extract the rules that are marked as recommended (you can assume all listed rules are recommended for now, 
        unless the user has explicitly unchecked them, but for this automation we assume the file is the source of truth).
        Add the rules to .gitignore and .dockerignore files in the same directory as the review file.
        Ensure you don't duplicate existing rules if possible, but appending is acceptable.
        """,
        expected_output="Updated .gitignore and .dockerignore files.",
        agent=agent
    )
