import os
import pytest
from unittest.mock import patch, MagicMock
from ignore_manager.cli import main
from ignore_manager.tasks import create_analysis_task

@pytest.fixture # this fixture in plain english means that it will create a mock object for the Crew class
def mock_crew():
    '''
    This fixture creates a mock object for the Crew class.
    When this fixture is used in a test, it will replace the actual Crew class with a mock object.
    The mock object will return a MagicMock object when called which
    in plain english means that it will replace the actual Crew class with a mock object.
    '''
    with patch('ignore_manager.cli.Crew') as mock:
        yield mock

@pytest.fixture
def mock_create_analysis_task():
    with patch('ignore_manager.cli.create_analysis_task') as mock:
        yield mock

@pytest.fixture
def mock_env_key():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-dummy"}):
        yield

def test_analyze_default(mock_crew, mock_create_analysis_task, mock_env_key):
    """Test default analysis (both files)"""
    test_args = ["ignore-manager", "analyze", "tests/dummy_project/"]
    with patch('sys.argv', test_args):
        main()
        
    # Verify create_analysis_task was called with correct output file
    mock_create_analysis_task.assert_called_once()
    call_args = mock_create_analysis_task.call_args
    assert call_args[0][2] == ['.gitignore', '.dockerignore'] # files_to_ignore
    assert call_args[0][3].endswith("project_root_artifact_review.md") # output_file

def test_analyze_gitignore_only(mock_crew, mock_create_analysis_task, mock_env_key):
    """Test analysis with -g flag"""
    test_args = ["ignore-manager", "analyze", "tests/dummy_project/", "-g"]
    with patch('sys.argv', test_args):
        main()
        
    mock_create_analysis_task.assert_called_once()
    call_args = mock_create_analysis_task.call_args
    assert call_args[0][2] == ['.gitignore']
    assert call_args[0][3].endswith("project_root_artifact_review_g.md")

def test_analyze_dockerignore_only(mock_crew, mock_create_analysis_task, mock_env_key):
    """Test analysis with -d flag"""
    test_args = ["ignore-manager", "analyze", "tests/dummy_project/", "-d"]
    with patch('sys.argv', test_args):
        main()
        
    mock_create_analysis_task.assert_called_once()
    call_args = mock_create_analysis_task.call_args
    assert call_args[0][2] == ['.dockerignore']
    assert call_args[0][3].endswith("project_root_artifact_review_d.md")
