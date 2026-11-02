"""RPS-001 in a real browser: play one round, then play again."""

import pytest
from playwright.sync_api import Page, expect

import app as web

pytestmark = pytest.mark.e2e


def test_round_and_replay_in_real_browser(page: Page, live_server, monkeypatch):
    """A real click shows the correct result, and a second click starts a new round.

    Only the computer's random choice is fixed; the real rules and HTTP run.
    """
    monkeypatch.setattr(web.random, "choice", lambda _moves: "scissors")
    page.goto(live_server)
    expect(page.get_by_role("status")).to_have_count(0)

    page.get_by_role("button", name="Rock", exact=True).click()
    choices = page.get_by_label("This round’s choices")
    expect(choices).to_contain_text("Rock")
    expect(choices).to_contain_text("Scissors")
    expect(page.locator('[data-outcome="win"]')).to_contain_text("You win!")

    page.get_by_role("button", name="Paper", exact=True).click()
    expect(choices).to_contain_text("Paper")
    expect(choices).to_contain_text("Scissors")
    expect(page.locator('[data-outcome="lose"]')).to_contain_text("Computer wins")
