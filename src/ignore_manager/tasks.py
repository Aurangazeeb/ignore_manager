from crewai import Task
from ignore_manager.agents import FileAnalyzerAgent, ConfigUpdaterAgent

def create_analysis_task(agent, directory_path, files_to_ignore, output_file):
    description = f"""Scan the directory at {directory_path}. 
    Identify all files and directories. 
    Read the existing {', '.join(files_to_ignore)} files if they exist.
    Determine which files are generated files or development artifacts that should be ignored in production.
    Compare your findings with the existing rules.
    Create a markdown file named '{output_file}' in the current directory.
    The file should list the recommended rules for {', '.join(files_to_ignore)} with a justification for each.
    If a rule already exists, note it but don't duplicate it in the final update list unless necessary for clarity.
    Format the file as follows:
    
    # Project Root Artifact Review
    """

    if '.gitignore' in files_to_ignore:
        description += """
    ## Recommended .gitignore rules
        1. rule1 : justification - (New/Existing)
        2. rule2 : justification - (New/Existing)
        """

    if '.dockerignore' in files_to_ignore:
        description += """
    ## Recommended .dockerignore rules
        1. rule1 : justification - (New/Existing)
        2. rule2 : justification - (New/Existing)
    """
    description += """
        Note : DO NOT enclose file content in ```
    """

    return Task(
        description=description,
        expected_output=f"A markdown file named '{output_file}' containing recommended ignore rules.",
        agent=agent,
        output_file=output_file
    )

def create_update_task(agent, review_file_path, files_to_ignore):
    return Task(
        description=f"""Read the review file at {review_file_path}.
        Extract the rules that are marked as recommended (you can assume all listed rules are recommended for now, 
        unless the user has explicitly unchecked them, but for this automation we assume the file is the source of truth).
        Add the rules to {', '.join(files_to_ignore)} files in the same directory as the review file.
        Ensure you don't duplicate existing rules if possible, but appending is acceptable.
        """,
        expected_output=f"Updated {', '.join(files_to_ignore)} files.",
        agent=agent
    )
