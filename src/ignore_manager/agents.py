from crewai import Agent
from ignore_manager.tools import DirectoryScanner, FileUpdater, ReviewReader, ExistingConfigReader

class FileAnalyzerAgent(Agent):
    def __init__(self):
        super().__init__(
            role='File Analyzer',
            goal='Analyze project structure and identify generated files to be ignored, considering existing rules.',
            backstory="""You are an expert software engineer with deep knowledge of various project structures, 
            build systems, and deployment best practices. You can look at a directory and immediately identify 
            which files are source code and which are generated artifacts that should be excluded from version control 
            and docker builds. You also respect existing configuration and only suggest changes when necessary.""",
            tools=[DirectoryScanner(), ExistingConfigReader()],
            verbose=True,
            allow_delegation=False
        )

class ConfigUpdaterAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Config Updater',
            goal='Update .gitignore and .dockerignore files based on the review.',
            backstory="""You are a DevOps engineer specializing in configuration management. 
            You take a list of files and rules and apply them to .gitignore and .dockerignore files 
            to ensure a clean and efficient repository and docker image.""",
            tools=[ReviewReader(), FileUpdater()],
            verbose=True,
            allow_delegation=False
        )
