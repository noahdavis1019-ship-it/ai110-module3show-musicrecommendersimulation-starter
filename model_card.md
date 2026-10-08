# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

**Goal / task:** Suggest the top 5 songs from a small catalog that best match one listener's stated taste (favorite genre, favorite mood, target energy, and whether they like acoustic sound).

- It assumes the user can describe their taste with one genre, one mood and one energy level.
- It is built for classroom exploration of how recommenders work, not for real users.

**Intended use:** learning, demos, and experimenting with how weights change rankings.

**Not intended for:** real music apps, users with mixed or changing tastes, judging the quality of an artist, or any decision that affects artists' income or exposure. It has no listening history, so it cannot learn.

---

## 3. How the Model Works

**Algorithm summary.** Every song is checked against the user's profile and earns points:

- Same genre as the user's favorite: +2 points.
- Same mood as the user's favorite: +1 point.
- Energy: up to +1.5 points. A song gets the full 1.5 when its energy equals the user's target, and fewer points the further away it is. Being *close* matters, not being high or low.
- Acoustic fit: up to +0.5. Acoustic fans get points for acoustic songs; everyone else gets points for produced, electronic sounds.

After every song has a score, the list is sorted from highest to lowest and the top 5 are shown, each with the reasons it earned its points.

**Changes from the starter:** implemented loading, scoring and ranking, added the acoustic fit check, and added six test profiles to `main.py`.

---

## 4. Data

- 20 songs in `data/songs.csv` (10 starter songs plus 10 I added).
- Features: genre, mood, energy, tempo, valence, danceability, acousticness.
- 17 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip hop, country, r&b, edm, classical, metal, reggae, latin, indie, gospel.
- 15 moods, including happy, chill, intense, sad, angry, nostalgic, romantic and euphoric.
- Lofi (3 songs) and pop (2 songs) are the only genres with more than one track. Most moods appear once.
- Missing: lyrics, language, release year, popularity, artist info, and any listening behavior. Tempo, valence and danceability are in the data but not used in the score yet.

---

## 5. Strengths

- Clear, single-genre profiles work well. Pop/happy gets Sunrise City, lofi/chill gets Library Rain, rock/intense gets Storm Runner. All three matched my intuition.
- Energy closeness does a good job filling the rest of the list. After the one rock song, the rock profile gets other high-energy tracks (Gym Hero, Bassline Riot, Ashes and Iron) instead of random picks.
- Every recommendation explains itself, so it is easy to see *why* a song ranked where it did.

---

## 6. Limitations and Bias

The biggest weakness I found is that genre is a gatekeeper. A genre match is worth 2 points, more than a perfect energy score, so a single label can beat everything else. In the Sad but Hyped test (indie, sad, energy 0.9), the #1 song was Empty Station, a quiet 0.33-energy track, because it matched genre and mood, while four songs that matched the energy almost perfectly sat far below it. Exact string matching makes this worse: "indie pop" gets zero credit for a "pop" fan, and a user whose genre is not in the catalog (k-pop) never gets a genre point at all. Since most genres have only one song, users with niche tastes get one good match and then generic high-energy filler, which is a small version of a filter bubble that favors whatever the catalog has the most of.

---

## 7. Evaluation

**Profiles tested:** three core profiles (pop/happy, lofi/chill, rock/intense) and three adversarial ones:

- Sad but Hyped: sad mood with very high energy (conflicting preferences).
- Genre Not in Catalog: k-pop, a genre that does not exist in the catalog.
- Acoustic Metal Fan: metal/angry but likes acoustic sound (another conflict).

I checked whether the #1 song made sense, whether the rest of the top 5 "felt" right, and whether the reasons matched the math.

**High-Energy Pop**

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

**Chill Lofi**

```
==================================================
Profile: Chill Lofi
Prefs: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
==================================================
1. Library Rain by Paper Lanterns - Score: 4.93
   Because: genre match (+2.0), mood match (+1.0), energy close to target (+1.50), acoustic fit (+0.43)
2. Midnight Coding by LoRoom - Score: 4.75
   Because: genre match (+2.0), mood match (+1.0), energy close to target (+1.40), acoustic fit (+0.35)
3. Focus Flow by LoRoom - Score: 3.81
   Because: genre match (+2.0), energy close to target (+1.42), acoustic fit (+0.39)
4. Spacewalk Thoughts by Orbit Bloom - Score: 2.85
   Because: mood match (+1.0), energy close to target (+1.40), acoustic fit (+0.46)
5. Coffee Shop Stories by Slow Stereo - Score: 1.92
   Because: energy close to target (+1.47), acoustic fit (+0.45)
```

**Deep Intense Rock**

```
==================================================
Profile: Deep Intense Rock
Prefs: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}
==================================================
1. Storm Runner by Voltline - Score: 4.93
   Because: genre match (+2.0), mood match (+1.0), energy close to target (+1.48), acoustic fit (+0.45)
2. Gym Hero by Max Pulse - Score: 2.93
   Because: mood match (+1.0), energy close to target (+1.46), acoustic fit (+0.47)
3. Bassline Riot by Kilowatt Kids - Score: 1.90
   Because: energy close to target (+1.41), acoustic fit (+0.48)
4. Ashes and Iron by Grave Signal - Score: 1.89
   Because: energy close to target (+1.40), acoustic fit (+0.49)
5. Ritmo de Noche by Calle Luna - Score: 1.82
   Because: energy close to target (+1.42), acoustic fit (+0.40)
```

**Sad but Hyped (edge case)**

```
==================================================
Profile: Sad but Hyped (edge case)
Prefs: {'genre': 'indie', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': False}
==================================================
1. Empty Station by Ghost Tapes - Score: 3.81
   Because: genre match (+2.0), mood match (+1.0), energy close to target (+0.64), acoustic fit (+0.17)
2. Storm Runner by Voltline - Score: 1.93
   Because: energy close to target (+1.48), acoustic fit (+0.45)
3. Gym Hero by Max Pulse - Score: 1.93
   Because: energy close to target (+1.46), acoustic fit (+0.47)
4. Bassline Riot by Kilowatt Kids - Score: 1.90
   Because: energy close to target (+1.41), acoustic fit (+0.48)
5. Ashes and Iron by Grave Signal - Score: 1.89
   Because: energy close to target (+1.40), acoustic fit (+0.49)
```

**Genre Not in Catalog (edge case)**

```
==================================================
Profile: Genre Not in Catalog (edge case)
Prefs: {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.7, 'likes_acoustic': False}
==================================================
1. Rooftop Lights by Indigo Parade - Score: 2.74
   Because: mood match (+1.0), energy close to target (+1.41), acoustic fit (+0.33)
2. Sunrise City by Neon Echo - Score: 2.73
   Because: mood match (+1.0), energy close to target (+1.32), acoustic fit (+0.41)
3. Concrete Crown by Blockwise - Score: 1.82
   Because: energy close to target (+1.38), acoustic fit (+0.44)
4. Night Drive Loop by Neon Echo - Score: 1.81
   Because: energy close to target (+1.42), acoustic fit (+0.39)
5. Gospel Sunrise by Mount Zion Choir - Score: 1.68
   Because: energy close to target (+1.47), acoustic fit (+0.21)
```

**Acoustic Metal Fan (edge case)**

```
==================================================
Profile: Acoustic Metal Fan (edge case)
Prefs: {'genre': 'metal', 'mood': 'angry', 'energy': 0.95, 'likes_acoustic': True}
==================================================
1. Ashes and Iron by Grave Signal - Score: 4.48
   Because: genre match (+2.0), mood match (+1.0), energy close to target (+1.47), acoustic fit (+0.01)
2. Bassline Riot by Kilowatt Kids - Score: 1.50
   Because: energy close to target (+1.48), acoustic fit (+0.01)
3. Gym Hero by Max Pulse - Score: 1.50
   Because: energy close to target (+1.47), acoustic fit (+0.03)
4. Storm Runner by Voltline - Score: 1.49
   Because: energy close to target (+1.44), acoustic fit (+0.05)
5. Ritmo de Noche by Calle Luna - Score: 1.45
   Because: energy close to target (+1.35), acoustic fit (+0.10)
```

**Profile comparisons**

- **Pop vs Lofi:** Pop leans toward high energy, produced tracks (Sunrise City, Gym Hero). Lofi flips to low energy acoustic tracks (Library Rain, Spacewalk Thoughts). The energy target and the acoustic flag pull the two lists to opposite ends of the catalog, which is what should happen.
- **Pop vs Rock:** Both have high energy targets, so Gym Hero shows up in both. For pop it earns the genre points; for rock it earns the "intense" mood points. Same song, different reason, which makes sense because Gym Hero is a loud, intense pop song.
- **Lofi vs Rock:** No overlap at all. Rock's top 5 are all above 0.85 energy and lofi's are all below 0.45. Energy closeness alone separates "chill lofi" from "intense rock."
- **Rock vs Sad but Hyped:** Positions 2 to 5 are almost the same high energy songs, because once genre and mood stop matching, energy decides everything. The only difference is the #1 slot, where Sad but Hyped gets a slow indie song purely from labels.
- **Pop vs Genre Not in Catalog:** Both like happy songs around 0.7 to 0.8 energy, but Genre Not in Catalog never gets genre points, so its top score is only 2.74 vs 4.88 and Rooftop Lights and Sunrise City nearly tie. The system has nothing real for this user and does not say so.
- **Rock vs Acoustic Metal Fan:** Both want loud music. The acoustic flag barely matters (+0.01 to +0.10) because there are no loud acoustic songs in the data, so the Acoustic Metal Fan basically gets the rock list with metal on top.

**Why does Gym Hero keep showing up?** In plain words: Gym Hero is labeled "pop," it is very high energy, and it sounds produced, not acoustic. Anyone who says "pop" gets 2 free points for it, and anyone who wants high energy gets nearly full energy points. So a "Happy Pop" listener sees it at #2 even though it is an intense workout song, because the system only knows the word "pop," not the feeling.

**Experiment (weight shift):** doubling energy (3.0) and halving genre (1.0) moved Rooftop Lights above Gym Hero for the pop profile. That felt more accurate. For Sad but Hyped it turned the #1 into a near tie (3.46 vs 3.42), so it got different, not clearly better. Output is in the README.

**Automated tests:** 5 pytest tests check CSV loading, the scoring math, and that results come back in the right order.

---

## 8. Future Work

- Partial genre matches (treat "indie pop" as close to both "indie" and "pop") using a small genre similarity map.
- Use tempo, valence and danceability in the score, and let users give a range instead of one value.
- Detect when there is no good match (like k-pop) and tell the user instead of showing filler.
- Add fake listening history so the system can try simple collaborative filtering.

---

## 9. Personal Reflection

My biggest learning moment was realizing a recommender is really just math and sorting. Every song gets points for matching genre, mood and energy, and the list is sorted by score. When I changed the genre points from 2.0 to 1.0, Gym Hero went from a clear #2 to basically tied with Rooftop Lights (2.78 vs 2.77). One number changed what a "happy pop" listener would see, which showed me the person choosing the weights has a lot of control.

I used an AI agent to build the project from the assignment steps. Its first version used things we haven't covered in class, so I had it simplified to loops, if statements and dictionaries. After that I read through score_song to understand how each point is added, and I checked Sunrise City's score by hand to make sure the 4.88 was right.

What surprised me was how real the results feel with only four features. Seeing the reasons printed next to each song makes it seem smart, but it only knows labels. Gym Hero shows up for happy pop fans just because it's tagged "pop," even though it's an intense workout song.

If I kept going, I would make "indie pop" count as partly "pop" so songs aren't ignored because of a slightly different label.
