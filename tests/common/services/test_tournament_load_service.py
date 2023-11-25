import pytest
from unittest.mock import patch
from bnl.common.services.tournament_load_service import tournament_load_service


class TestLoadTournamentService:
    @patch('requests.get')
    def test_load_success(self, mock_get):
        mock_get.side_effect = [
            MockResponse(200, 'tournament'),
            MockResponse(200, 'tournament_games'),
            MockResponse(200, 'team_info'),
        ]
        tournament_load_service.process_tournament(1)
