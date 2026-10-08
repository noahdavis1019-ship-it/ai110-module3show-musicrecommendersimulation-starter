# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How real recommenders work

Big platforms like Spotify and YouTube mix two ideas. **Collaborative filtering** looks at behavior across many users: if people who like the songs you like also play song X, you probably will too. It uses signals like plays, skips, likes, saves, playlist adds and replays. **Content-based filtering** looks at the songs themselves: genre, mood, tempo, energy, acousticness, even audio embeddings. Real systems blend both, then rank millions of candidates in stages. My version is a small **content-based** recommender. It has no other users, so it can only compare song attributes to one listener's stated taste. It prioritizes genre first, mood second, and then how close the song's energy is to what the listener wants.

### Features used

**`Song`**: `id`, `title`, `artist`, `genre`, `mood`, `energy` (0 to 1), `tempo_bpm`, `valence` (0 to 1), `danceability` (0 to 1), `acousticness` (0 to 1)

**`UserProfile`**: `favorite_genre`, `favorite_mood`, `target_energy` (0 to 1), `likes_acoustic` (True/False)

The dictionary version of a profile used by `main.py` looks like:

```python
{"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
```

### Algorithm Recipe

**Scoring Rule (one song):**

| Check | Points |
|---|---|
| Genre matches `favorite_genre` | +2.0 |
| Mood matches `favorite_mood` | +1.0 |
| Energy closeness | +1.5 x (1 - abs(song.energy - target_energy)) |
| Acoustic fit | +0.5 x acousticness if the user likes acoustic, otherwise +0.5 x (1 - acousticness) |

Max possible score is 5.0. Energy uses *closeness*, not "higher is better", so a chill listener with target 0.3 is rewarded for a 0.3 song and penalized for a 0.9 song.

**Ranking Rule (whole list):** score every song in the catalog with the Scoring Rule, sort from highest to lowest, return the top `k`. We need both rules because a score only says how good *one* song is; the ranking turns those numbers into an ordered list and decides what actually gets shown.

### Data flow

```
User prefs (genre, mood, energy, likes_acoustic)
        |
        v
For each song in data/songs.csv  -->  score_song()  -->  (score, reasons)
        |
        v
Sort all songs by score (high to low)  -->  Top K recommendations with reasons
```

### Expected biases

- Genre is worth the most points, so this system may over-prioritize genre and bury a great song that matches the user's mood and energy but has a different genre label.
- Genre and mood are exact string matches. "indie pop" gets no credit for a "pop" fan.
- The catalog is tiny (20 songs), and most genres only have one song, so some users will get weak matches no matter what.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



