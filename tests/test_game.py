"""RPS-001 rules: nine literal outcomes plus one real request/result check."""

# pytest injects fixtures by their function names.
# pylint: disable=redefined-outer-name

import pytest

import app as web
from game import determine_winner


@pytest.mark.unit
@pytest.mark.parametrize(
    ("player", "computer", "expected"),
    [
        ("rock", "rock", "tie"),
        ("rock", "paper", "lose"),
        ("rock", "scissors", "win"),
        ("paper", "rock", "win"),
        ("paper", "paper", "tie"),
        ("paper", "scissors", "lose"),
        ("scissors", "rock", "lose"),
        ("scissors", "paper", "win"),
        ("scissors", "scissors", "tie"),
    ],
)
def test_determine_winner_matches_spec(player, computer, expected):
    """Each matchup returns the expected result from the player's perspective."""
    assert determine_winner(player, computer) == expected


@pytest.fixture
def client():
    """A Flask test client for the real app."""
    web.app.config.update(TESTING=True)
    return web.app.test_client()


@pytest.mark.integration
def test_submitted_losing_round_uses_real_rules(client, monkeypatch):
    """Rock against paper shows both choices and 'Computer wins'.

    Only the computer's random choice is fixed; the real rule function runs.
    """
    monkeypatch.setattr(web.random, "choice", lambda _moves: "paper")
    response = client.post("/", data={"move": "rock"})
    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "You chose" in page and "Computer chose" in page
    assert "Rock" in page and "Paper" in page
    assert "Computer wins" in page
    assert 'data-outcome="lose"' in page
    assert "game rules not built yet" not in page
