import os
from crewai.tools import BaseTool

class DirectoryScanner(BaseTool):
    name: str = "Directory Scanner"
    description: str = "Scans a directory recursively and lists all files and folders, ignoring .git directory."

    def _run(self, directory_path: str) -> str:
        if not os.path.exists(directory_path):
            return f"Error: Directory {directory_path} does not exist."
        
        file_list = []
        for root, dirs, files in os.walk(directory_path):
            if '.git' in dirs:
                dirs.remove('.git')  # don't visit .git directories
            
            for name in files:
                file_list.append(os.path.join(root, name))
            for name in dirs:
                file_list.append(os.path.join(root, name))
                
        return "\n".join(file_list)

class FileUpdater(BaseTool):
    name: str = "File Updater"
    description: str = "Appends content to a file. Useful for updating .gitignore and .dockerignore."

    def _run(self, file_path: str, content: str) -> str:
        try:
            with open(file_path, 'a') as f:
                f.write(content + "\n")
            return f"Successfully updated {file_path}"
        except Exception as e:
            return f"Error updating file: {str(e)}"

class ReviewReader(BaseTool):
    name: str = "Review Reader"
    description: str = "Reads the content of the project_root_artifact_review.md file."

    def _run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"Error: File {file_path} does not exist."
        
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

class ExistingConfigReader(BaseTool):
    name: str = "Existing Config Reader"
    description: str = "Reads the content of existing .gitignore and .dockerignore files in the directory."

    def _run(self, directory_path: str) -> str:
        result = ""
        gitignore_path = os.path.join(directory_path, ".gitignore")
        dockerignore_path = os.path.join(directory_path, ".dockerignore")

        if os.path.exists(gitignore_path):
            try:
                with open(gitignore_path, 'r') as f:
                    result += f"--- .gitignore ---\n{f.read()}\n\n"
            except Exception as e:
                result += f"Error reading .gitignore: {str(e)}\n\n"
        else:
            result += ".gitignore does not exist.\n\n"

        if os.path.exists(dockerignore_path):
            try:
                with open(dockerignore_path, 'r') as f:
                    result += f"--- .dockerignore ---\n{f.read()}\n\n"
            except Exception as e:
                result += f"Error reading .dockerignore: {str(e)}\n\n"
        else:
            result += ".dockerignore does not exist.\n\n"
            
        return result
