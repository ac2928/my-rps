# Rock, Paper, Scissors

## RPS-001: Play a round

**Purpose:** one person plays a quick round against the computer.

- Choose rock, paper, or scissors. The computer chooses one move for that round.
- Display both choices and the result: **You win!**, **Computer wins**, or **It’s a tie**.
- Choosing again starts an independent round. No score or saved history.
- Keep the supplied interface and server. Name/color changes can wait until the rules work.

### Expected results

Results are from the **player’s perspective**. `determine_winner(player, computer)` in `game.py` returns `win`, `lose`, or `tie`. Inputs are the lowercase moves below; the supplied server rejects other choices.

| Player | Computer | Expected return |
| --- | --- | --- |
| rock | rock | tie |
| rock | paper | lose |
| rock | scissors | win |
| paper | rock | win |
| paper | paper | tie |
| paper | scissors | lose |
| scissors | rock | lose |
| scissors | paper | win |
| scissors | scissors | tie |

### Agreed plan

- My prediction: I choose rock and the computer chooses paper, so I lose. Paper beats rock by covering it. This matches the expected-results table above.
- Scope: implement only determine_winner(player, computer) in game.py, returning win, lose, or tie from the player's perspective. Keep the supplied server, page, and styles. No scoring, saved history, accounts, new framework, or AI API.
- Valid losing round (positive case): player rock, computer paper returns lose, and the page shows both choices and "Computer wins".
- Rejected input (negative case): a missing or unsupported move such as lizard returns HTTP 400 with "Choose Rock, Paper, or Scissors to play.", and the rule function is not called.
- Checks: follow the Checks table below: nine unit cases in tests/test_game.py, one real request/result integration test (only the computer's choice fixed), reuse the supplied invalid-input tests, and one browser round plus replay in tests/e2e/test_round.py. Run the full .venv/bin/python check.py.
- Help received: Claude (chat assistant) explained the steps; I made the predictions and edits.

### Checks

Before coding, agree this small test plan with AI:

| Level | Cases and evidence |
| --- | --- |
| Unit — positive | All nine literal expected results above, including valid losses and ties. |
| Integration — positive | A submitted round uses the real rule function and displays both choices and the correct result. Fix the computer choice for the test. |
| Integration — negative | Reuse supplied missing/unsupported-move tests: HTTP 400 and a helpful explanation, without calling the rules. A crash is not the intended result. |
| E2E — positive | Add a real-browser round and replay in tests/e2e/test_round.py using the supplied live_server/page fixtures. Fix only the computer choice; use real rules and real HTTP. |

Use `unit`, `integration`, and `e2e` pytest markers. Run `.venv/bin/python check.py` for Black, Pylint, fast tests, and browser checks; then review the diff. Keep shared settings and meaningful assertions intact. The student still plays, inspects a rule and its test, and gives feedback. Browser automation does not establish every aspect of usability or application performance.


### Work record

- Issue: https://github.com/ac2928/my-rps/issues/1
- Pull request / CI: add actual URLs when they exist.
- Implementation: [game.py](game.py). determine_winner uses a BEATS dictionary: the same move is a tie, beating the computer's move is a win, otherwise it is a loss.
- Tests: [tests/test_game.py](tests/test_game.py) has the nine unit outcomes and one integration test (rock vs paper with only the computer's choice fixed shows both choices and "Computer wins"). [tests/e2e/test_round.py](tests/e2e/test_round.py) plays rock then paper in Chromium with the computer fixed to scissors: "You win!", then a new round showing "Computer wins". The supplied invalid-input tests in tests/test_shell.py still pass (HTTP 400 with a helpful message).
- Checks: full .venv/bin/python check.py on 2026-11-02: PASS Black, PASS Pylint, PASS pytest non-browser checks, PASS pytest real Chromium browser. The first run failed Black and Pylint only because the two new test files were missing a final newline; I fixed that with Black and reran.
- Test explanation: This test is checking if rock vs paper will return "lose". If the code got the rule backwards and said rock beats paper, it would return "win" instead, and the test would fail.
- Browser observation: I picked rock and the computer picked scissors; it said "You win!" because rock beats scissors. Tab and Enter worked to choose a move, and clicking again started a new round.