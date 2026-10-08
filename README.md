# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

**VibeFinder 1.0** is a content-based music recommender written in Python. It loads a 20-song catalog from `data/songs.csv`, scores every song against a listener's taste profile (genre, mood, target energy, acoustic preference), ranks the catalog, and prints the top 5 with a plain-language reason for every point awarded.

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

Default "pop/happy" profile (`python -m src.main`):

```
==================================================
Profile: High-Energy Pop
Prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
==================================================
1. Sunrise City by Neon Echo - Score: 4.88
   Because: genre match (+2.0), mood match (+1.0), energy close to target (+1.47), acoustic fit (+0.41)
2. Gym Hero by Max Pulse - Score: 3.78
   Because: genre match (+2.0), energy close to target (+1.30), acoustic fit (+0.47)
3. Rooftop Lights by Indigo Parade - Score: 2.77
   Because: mood match (+1.0), energy close to target (+1.44), acoustic fit (+0.33)
4. Concrete Crown by Blockwise - Score: 1.91
   Because: energy close to target (+1.47), acoustic fit (+0.44)
5. Ritmo de Noche by Calle Luna - Score: 1.83
   Because: energy close to target (+1.43), acoustic fit (+0.40)
```

Output for all six profiles is in the [model card](model_card.md#7-evaluation).

---

## Experiments You Tried

**Weight shift (energy x2, genre x0.5).** I temporarily changed `GENRE_POINTS` from 2.0 to 1.0 and `ENERGY_POINTS` from 1.5 to 3.0 at the top of `recommender.py`, then changed them back. Sunrise City stayed #1, but Rooftop Lights (indie pop, happy) jumped over Gym Hero (pop, intense). That felt *more* accurate: a happy pop listener probably wants Rooftop Lights over a gym track. For the Sad but Hyped profile the change made the top two nearly tie, so it got different but not clearly better.

```
==================================================
Profile: High-Energy Pop (EXPERIMENT: genre 1.0, energy 3.0)
Prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
==================================================
1. Sunrise City by Neon Echo - Score: 5.35
   Because: genre match (+1.0), mood match (+1.0), energy close to target (+2.94), acoustic fit (+0.41)
2. Rooftop Lights by Indigo Parade - Score: 4.21
   Because: mood match (+1.0), energy close to target (+2.88), acoustic fit (+0.33)
3. Gym Hero by Max Pulse - Score: 4.08
   Because: genre match (+1.0), energy close to target (+2.61), acoustic fit (+0.47)
4. Concrete Crown by Blockwise - Score: 3.38
   Because: energy close to target (+2.94), acoustic fit (+0.44)
5. Ritmo de Noche by Calle Luna - Score: 3.25
   Because: energy close to target (+2.85), acoustic fit (+0.40)
```

---

## Limitations and Risks

- Tiny catalog (20 songs). Most genres have exactly one song, so a lot of users only get one real match.
- Genre and mood are exact string matches. "indie pop" earns zero genre points for a "pop" fan, and a genre that is not in the catalog (k-pop) gets nothing at all.
- Genre is the heaviest weight, so one label can outweigh everything else. The `sad_but_hyped` user gets a slow, quiet song at #1 because it matches genre and mood even though it misses energy badly.
- No lyrics, language, artist familiarity or listening history.

More detail is in the [model card](model_card.md).

---

## Reflection

Read the full write-up in the [**Model Card**](model_card.md).

Building this showed me that a recommendation is just a score plus a sort. Every song gets judged by the same few rules, and the "personalization" comes entirely from which features you pick and how much each one is worth. Small weight changes reshuffled the list in ways that felt meaningful, which is a little unsettling: the system can feel smart while only knowing four facts about me.

Bias shows up in quiet places. The weights I chose decide whose taste counts most, and the catalog decides who gets served at all. A listener whose genre is missing from the data gets generic high-energy filler, and nothing in the output tells them the system simply has nothing for them. In a real app with millions of users, the same problem would push people toward whatever is already popular or well-labeled.
