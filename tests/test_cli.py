"""Tests for git-taz CLI module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys

from src.git_taz.cli import CheckoutCLI
from src.git_taz.services.git_operations import CheckoutResult


class TestCheckoutCLI:
    """Test CheckoutCLI class."""

    @pytest.fixture
    def mock_service(self):
        """Create a mock GitOperationsService."""
        service = Mock()
        service.get_branches.return_value = ['main', 'develop', 'feature/test']
        service.get_tags.return_value = ['v1.0.0', 'v2.0.0']
        service.get_current_branch.return_value = 'main'
        return service

    @pytest.fixture
    def cli_instance(self, mock_service):
        """Create a CheckoutCLI instance with mocked dependencies."""
        with patch('src.git_taz.cli.checkout_cli.GitRepository') as mock_repo_class:
            with patch('src.git_taz.cli.checkout_cli.GitOperationsService') as mock_service_class:
                mock_repo = Mock()
                mock_repo_class.from_path.return_value = mock_repo
                mock_service_class.return_value = mock_service
                
                cli = CheckoutCLI(".")
                cli.git_operations = mock_service
                return cli

    def test_init_success(self):
        """Test successful CLI initialization."""
        with patch('src.git_taz.cli.checkout_cli.GitRepository') as mock_repo_class:
            with patch('src.git_taz.cli.checkout_cli.GitOperationsService') as mock_service_class:
                mock_repo = Mock()
                mock_service = Mock()
                mock_repo_class.from_path.return_value = mock_repo
                mock_service_class.return_value = mock_service
                
                cli = CheckoutCLI(".")
                
                mock_repo_class.from_path.assert_called_once_with(".")
                mock_service_class.assert_called_once_with(mock_repo)
                assert cli.repository == mock_repo
                assert cli.git_operations == mock_service

    def test_init_failure(self):
        """Test CLI initialization failure."""
        with patch('src.git_taz.cli.checkout_cli.GitRepository') as mock_repo_class:
            mock_repo_class.from_path.side_effect = Exception("Repository not found")
            
            with pytest.raises(SystemExit) as excinfo:
                with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                    CheckoutCLI("nonexistent")
            
            assert excinfo.value.code == 1

    def test_list_branches(self, cli_instance, mock_service, capsys):
        """Test listing branches."""
        cli_instance.list_branches()
        
        captured = capsys.readouterr()
        output_lines = captured.out.strip().split('\n')
        
        assert "Branches:" in output_lines[0]
        assert "* main" in captured.out  # Current branch marked
        assert "  develop" in captured.out
        assert "  feature/test" in captured.out

    def test_list_tags(self, cli_instance, mock_service, capsys):
        """Test listing tags."""
        cli_instance.list_tags()
        
        captured = capsys.readouterr()
        output_lines = captured.out.strip().split('\n')
        
        assert "Tags:" in output_lines[0]
        assert "  v1.0.0" in captured.out
        assert "  v2.0.0" in captured.out

    def test_checkout_direct_success(self, cli_instance, mock_service, capsys):
        """Test direct checkout success."""
        success_result = CheckoutResult(True, "Successfully checked out main", "main")
        mock_service.checkout.return_value = success_result
        
        cli_instance.checkout_direct("main")
        
        mock_service.checkout.assert_called_once_with("main")
        captured = capsys.readouterr()
        assert "Successfully checked out main" in captured.out

    def test_checkout_direct_failure(self, cli_instance, mock_service):
        """Test direct checkout failure."""
        failure_result = CheckoutResult(False, "Branch not found")
        mock_service.checkout.return_value = failure_result
        
        with pytest.raises(SystemExit) as excinfo:
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                cli_instance.checkout_direct("nonexistent")
        
        assert excinfo.value.code == 1
        mock_service.checkout.assert_called_once_with("nonexistent")

    @patch('builtins.input', side_effect=['1', 'q'])  # Choose branches, then quit
    def test_checkout_interactive_branches(self, mock_input, cli_instance, mock_service, capsys):
        """Test interactive checkout selecting branches."""
        cli_instance.checkout_interactive()
        
        captured = capsys.readouterr()
        assert "Select checkout target type:" in captured.out
        assert "1. Branches" in captured.out
        assert "2. Tags" in captured.out
        assert "Available branches:" in captured.out

    @patch('builtins.input', side_effect=['2', 'q'])  # Choose tags, then quit
    def test_checkout_interactive_tags(self, mock_input, cli_instance, mock_service, capsys):
        """Test interactive checkout selecting tags."""
        cli_instance.checkout_interactive()
        
        captured = capsys.readouterr()
        assert "Select checkout target type:" in captured.out
        assert "Available tags:" in captured.out

    @patch('builtins.input', side_effect=['3'])  # Invalid choice
    def test_checkout_interactive_invalid_choice(self, mock_input, cli_instance, capsys):
        """Test interactive checkout with invalid choice."""
        cli_instance.checkout_interactive()
        
        captured = capsys.readouterr()
        assert "Invalid choice." in captured.out

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_checkout_interactive_keyboard_interrupt(self, mock_input, cli_instance, capsys):
        """Test interactive checkout with keyboard interrupt."""
        cli_instance.checkout_interactive()
        
        captured = capsys.readouterr()
        assert "Cancelled." in captured.out

    @patch('builtins.input', side_effect=['1', '1'])  # Choose branches, then first branch
    def test_checkout_from_list_branches_success(self, mock_input, cli_instance, mock_service, capsys):
        """Test checkout from branches list - success."""
        success_result = CheckoutResult(True, "Successfully checked out main", "main")
        mock_service.checkout.return_value = success_result
        
        cli_instance._checkout_from_list("branches")
        
        mock_service.checkout.assert_called_once_with("main")
        captured = capsys.readouterr()
        assert "Available branches:" in captured.out
        assert "1. main" in captured.out

    @patch('builtins.input', side_effect=['q'])  # Quit
    def test_checkout_from_list_quit(self, mock_input, cli_instance, mock_service, capsys):
        """Test checkout from list with quit."""
        cli_instance._checkout_from_list("branches")
        
        mock_service.checkout.assert_not_called()

    @patch('builtins.input', side_effect=['99'])  # Invalid number
    def test_checkout_from_list_invalid_selection(self, mock_input, cli_instance, mock_service, capsys):
        """Test checkout from list with invalid selection."""
        cli_instance._checkout_from_list("branches")
        
        captured = capsys.readouterr()
        assert "Invalid selection." in captured.out
        mock_service.checkout.assert_not_called()

    @patch('builtins.input', side_effect=['abc'])  # Invalid input
    def test_checkout_from_list_invalid_input(self, mock_input, cli_instance, mock_service, capsys):
        """Test checkout from list with invalid input."""
        cli_instance._checkout_from_list("branches")
        
        captured = capsys.readouterr()
        assert "Invalid input." in captured.out
        mock_service.checkout.assert_not_called()

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    def test_checkout_from_list_keyboard_interrupt(self, mock_input, cli_instance, capsys):
        """Test checkout from list with keyboard interrupt."""
        cli_instance._checkout_from_list("branches")
        
        captured = capsys.readouterr()
        assert "Cancelled." in captured.out

    def test_checkout_from_list_no_targets(self, cli_instance, mock_service, capsys):
        """Test checkout from list when no targets available."""
        mock_service.get_branches.return_value = []
        
        cli_instance._checkout_from_list("branches")
        
        captured = capsys.readouterr()
        assert "No branches found." in captured.out

    @patch('builtins.input', side_effect=['q'])  # Quit
    def test_checkout_from_list_tags(self, mock_input, cli_instance, mock_service, capsys):
        """Test checkout from tags list."""
        cli_instance._checkout_from_list("tags")
        
        captured = capsys.readouterr()
        assert "Available tags:" in captured.out
        assert "1. v1.0.0" in captured.out
        assert "2. v2.0.0" in captured.out