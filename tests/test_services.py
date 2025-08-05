"""Tests for git-taz services module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from git import Repo

from src.git_taz.models import GitRepository
from src.git_taz.services import GitOperationsService
from src.git_taz.services.git_operations import CheckoutResult


class TestCheckoutResult:
    """Test CheckoutResult class."""

    def test_checkout_result_success(self):
        """Test successful checkout result."""
        result = CheckoutResult(True, "Success", "main")
        assert result.success is True
        assert result.message == "Success"
        assert result.target == "main"

    def test_checkout_result_failure(self):
        """Test failed checkout result."""
        result = CheckoutResult(False, "Failed")
        assert result.success is False
        assert result.message == "Failed"
        assert result.target is None


class TestGitOperationsService:
    """Test GitOperationsService class."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository."""
        repo = Mock(spec=GitRepository)
        repo.repo = Mock(spec=Repo)
        return repo

    @pytest.fixture
    def service(self, mock_repository):
        """Create a GitOperationsService instance."""
        with patch('src.git_taz.services.git_operations.GitToolsManager'):
            return GitOperationsService(mock_repository)

    def test_get_branches_with_repo(self, service, mock_repository):
        """Test getting branches when repository exists."""
        # Mock branches
        branch1 = Mock()
        branch1.name = "main"
        branch2 = Mock()
        branch2.name = "feature/test"
        
        mock_repository.repo.branches = [branch2, branch1]  # Unsorted order
        
        branches = service.get_branches()
        assert branches == ["feature/test", "main"]  # Should be sorted

    def test_get_branches_no_repo(self, service, mock_repository):
        """Test getting branches when no repository."""
        mock_repository.repo = None
        branches = service.get_branches()
        assert branches == []

    def test_get_tags_with_repo(self, service, mock_repository):
        """Test getting tags when repository exists."""
        # Mock tags
        tag1 = Mock()
        tag1.name = "v2.0.0"
        tag2 = Mock()
        tag2.name = "v1.0.0"
        
        mock_repository.repo.tags = [tag1, tag2]  # Unsorted order
        
        tags = service.get_tags()
        assert tags == ["v1.0.0", "v2.0.0"]  # Should be sorted

    def test_get_tags_no_repo(self, service, mock_repository):
        """Test getting tags when no repository."""
        mock_repository.repo = None
        tags = service.get_tags()
        assert tags == []

    def test_get_checkout_targets_branches(self, service):
        """Test getting checkout targets for branches."""
        with patch.object(service, 'get_branches', return_value=['main', 'develop']):
            targets = service.get_checkout_targets('branches')
            expected = [('main', 'main'), ('develop', 'develop')]
            assert targets == expected

    def test_get_checkout_targets_tags(self, service):
        """Test getting checkout targets for tags."""
        with patch.object(service, 'get_tags', return_value=['v1.0.0', 'v2.0.0']):
            targets = service.get_checkout_targets('tags')
            expected = [('v1.0.0', 'v1.0.0'), ('v2.0.0', 'v2.0.0')]
            assert targets == expected

    def test_checkout_success(self, service, mock_repository):
        """Test successful checkout."""
        mock_git = Mock()
        mock_repository.repo.git = mock_git
        
        result = service.checkout('main')
        
        mock_git.checkout.assert_called_once_with('main')
        assert result.success is True
        assert result.message == "Successfully checked out main"
        assert result.target == "main"

    def test_checkout_no_repo(self, service, mock_repository):
        """Test checkout when no repository."""
        mock_repository.repo = None
        
        result = service.checkout('main')
        
        assert result.success is False
        assert result.message == "No repository loaded"

    def test_checkout_failure(self, service, mock_repository):
        """Test checkout failure due to git error."""
        mock_git = Mock()
        mock_git.checkout.side_effect = Exception("Checkout failed")
        mock_repository.repo.git = mock_git
        
        result = service.checkout('nonexistent')
        
        assert result.success is False
        assert "Checkout failed: Checkout failed" in result.message

    def test_get_current_branch_success(self, service, mock_repository):
        """Test getting current branch successfully."""
        mock_branch = Mock()
        mock_branch.name = "main"
        mock_repository.repo.active_branch = mock_branch
        
        branch = service.get_current_branch()
        assert branch == "main"

    def test_get_current_branch_no_repo(self, service, mock_repository):
        """Test getting current branch when no repository."""
        mock_repository.repo = None
        
        branch = service.get_current_branch()
        assert branch is None

    def test_get_current_branch_failure(self, service, mock_repository):
        """Test getting current branch when git fails."""
        # Mock the active_branch property to raise an exception when accessed
        type(mock_repository.repo).active_branch = property(lambda x: (_ for _ in ()).throw(Exception("No active branch")))
        
        branch = service.get_current_branch()
        assert branch is None

    def test_git_operations_delegation(self, service):
        """Test that git operations are properly delegated to tools manager."""
        # Test that the service delegates to tools manager
        service.tools_manager.git_status.return_value = "status_result"
        service.tools_manager.git_log.return_value = "log_result"
        service.tools_manager.git_branches.return_value = "branches_result"
        service.tools_manager.git_diff.return_value = "diff_result"
        
        assert service.get_status() == "status_result"
        assert service.get_log() == "log_result"
        assert service.get_branches_info() == "branches_result"
        assert service.get_diff() == "diff_result"
        
        service.tools_manager.git_status.assert_called_once()
        service.tools_manager.git_log.assert_called_once()
        service.tools_manager.git_branches.assert_called_once()
        service.tools_manager.git_diff.assert_called_once()