# AI Interactions Log

> Stretch features attempted: Challenge 2 (multiple scoring modes), Challenge 3 (diversity penalty), Challenge 4 (visual summary table).

---

## Agentic Workflow (SF8)

**What task did you give the agent?**

Add a diversity penalty to the ranking step and a formatted terminal table, without breaking the existing scoring function or the starter tests.

**Prompts used:**

- "In recommender.py, add an optional diversity step after ranking. Build the top k greedily: before picking each song, subtract 1.0 if its artist is already in the list and 0.5 if its genre is. Add the penalty to the reasons list so the user sees it. Keep recommend_songs' return format the same."
- "Format the recommendations in main.py as an ASCII table with rank, title, artist, score and reasons. Wrap long reasons instead of cutting them off. No extra libraries."

**What did the agent generate or change?**

- `src/recommender.py`: added `apply_diversity_penalty()` and a `diversity` flag on `recommend_songs()`.
- `src/main.py`: added `format_table()` using `textwrap`, plus `--diversity`, `--mode`, `--profile` and `-k` flags.
- `tests/test_recommender.py`: added a test that Focus Flow ranks lower with diversity on.

**What did you verify or fix manually?**

- Checked by hand that the lofi list changes the way the rule says it should: LoRoom's second song (Focus Flow) loses 1.5 points (repeat artist + repeat genre) and drops from #3 to #4.
- Confirmed the penalty is only applied once per song and that the default output (diversity off) is unchanged.
- Fixed the starter import (`from recommender import ...`) so `python -m src.main` works from the repo root.

---

## Design Pattern (SF10)

**Which design pattern did you use?**

Strategy pattern, in a lightweight form.

**How did AI help you brainstorm or implement it?**

I asked for a way to switch between "Genre-First," "Mood-First" and "Energy-Focused" ranking without copying the scoring function three times. The AI suggested either a class per strategy or a table of weights. Since every mode uses the same rules and only the weights differ, I went with the weight table because it is simpler and easier to test.

**How does the pattern appear in your final code?**

`SCORING_MODES` in `src/recommender.py` maps each mode name to its weights. `score_song(user_prefs, song, mode)` looks up the weights for the chosen mode, `Recommender(songs, mode=...)` and `recommend_songs(..., mode=...)` pass it through, and `python -m src.main --mode energy_focused` switches it from the CLI. Adding a new mode is one new dictionary entry.
