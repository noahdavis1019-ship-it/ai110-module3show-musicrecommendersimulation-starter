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

**Changes from the starter:** implemented loading, scoring and ranking; added the acoustic fit; added four scoring modes (balanced, genre first, mood first, energy focused) that only change the weights; added an optional diversity penalty (-1.0 for a repeat artist, -0.5 for a repeat genre already in the list).

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

The biggest weakness I found is that genre is a gatekeeper. A genre match is worth 2 points, more than a perfect energy score, so a single label can beat everything else. In the `sad_but_hyped` test (indie, sad, energy 0.9), the #1 song was Empty Station, a quiet 0.33-energy track, because it matched genre and mood, while four songs that matched the energy almost perfectly sat far below it. Exact string matching makes this worse: "indie pop" gets zero credit for a "pop" fan, and a user whose genre is not in the catalog (k-pop) never gets a genre point at all. Since most genres have only one song, users with niche tastes get one good match and then generic high-energy filler, which is a small version of a filter bubble that favors whatever the catalog has the most of.

---

## 7. Evaluation

**Profiles tested:** three core profiles (pop/happy, lofi/chill, rock/intense) and three adversarial ones:

- `sad_but_hyped`: sad mood with very high energy (conflicting preferences).
- `ghost_genre`: k-pop, a genre that does not exist in the catalog.
- `acoustic_rager`: metal/angry but likes acoustic sound (another conflict).

I checked whether the #1 song made sense, whether the rest of the top 5 "felt" right, and whether the reasons matched the math.

**pop**

```
Profile: pop  |  mode=balanced  diversity=off
Prefs: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}

#  Title                 Artist             Score  Reasons
-----------------------------------------------------------------------------------------------------------
1  Sunrise City          Neon Echo           4.88  genre match (+2.00); mood match (+1.00); energy 0.82 vs
                                                   target 0.80 (+1.47); non-acoustic fit (+0.41)
2  Gym Hero              Max Pulse           3.78  genre match (+2.00); energy 0.93 vs target 0.80 (+1.30);
                                                   non-acoustic fit (+0.47)
3  Rooftop Lights        Indigo Parade       2.77  mood match (+1.00); energy 0.76 vs target 0.80 (+1.44);
                                                   non-acoustic fit (+0.33)
4  Concrete Crown        Blockwise           1.91  energy 0.78 vs target 0.80 (+1.47); non-acoustic fit
                                                   (+0.44)
5  Ritmo de Noche        Calle Luna          1.83  energy 0.85 vs target 0.80 (+1.43); non-acoustic fit
                                                   (+0.40)
```

**lofi**

```
Profile: lofi  |  mode=balanced  diversity=off
Prefs: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}

#  Title                 Artist             Score  Reasons
-----------------------------------------------------------------------------------------------------------
1  Library Rain          Paper Lanterns      4.93  genre match (+2.00); mood match (+1.00); energy 0.35 vs
                                                   target 0.35 (+1.50); acoustic fit (+0.43)
2  Midnight Coding       LoRoom              4.75  genre match (+2.00); mood match (+1.00); energy 0.42 vs
                                                   target 0.35 (+1.40); acoustic fit (+0.35)
3  Focus Flow            LoRoom              3.81  genre match (+2.00); energy 0.40 vs target 0.35 (+1.42);
                                                   acoustic fit (+0.39)
4  Spacewalk Thoughts    Orbit Bloom         2.85  mood match (+1.00); energy 0.28 vs target 0.35 (+1.40);
                                                   acoustic fit (+0.46)
5  Coffee Shop Stories   Slow Stereo         1.92  energy 0.37 vs target 0.35 (+1.47); acoustic fit (+0.45)
```

**rock**

```
Profile: rock  |  mode=balanced  diversity=off
Prefs: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}

#  Title                 Artist             Score  Reasons
-----------------------------------------------------------------------------------------------------------
1  Storm Runner          Voltline            4.93  genre match (+2.00); mood match (+1.00); energy 0.91 vs
                                                   target 0.90 (+1.48); non-acoustic fit (+0.45)
2  Gym Hero              Max Pulse           2.93  mood match (+1.00); energy 0.93 vs target 0.90 (+1.46);
                                                   non-acoustic fit (+0.47)
3  Bassline Riot         Kilowatt Kids       1.90  energy 0.96 vs target 0.90 (+1.41); non-acoustic fit
                                                   (+0.48)
4  Ashes and Iron        Grave Signal        1.89  energy 0.97 vs target 0.90 (+1.40); non-acoustic fit
                                                   (+0.49)
5  Ritmo de Noche        Calle Luna          1.82  energy 0.85 vs target 0.90 (+1.42); non-acoustic fit
                                                   (+0.40)
```

**sad_but_hyped**

```
Profile: sad_but_hyped  |  mode=balanced  diversity=off
Prefs: {'genre': 'indie', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': False}

#  Title                 Artist             Score  Reasons
-----------------------------------------------------------------------------------------------------------
1  Empty Station         Ghost Tapes         3.81  genre match (+2.00); mood match (+1.00); energy 0.33 vs
                                                   target 0.90 (+0.64); non-acoustic fit (+0.17)
2  Storm Runner          Voltline            1.93  energy 0.91 vs target 0.90 (+1.48); non-acoustic fit
                                                   (+0.45)
3  Gym Hero              Max Pulse           1.93  energy 0.93 vs target 0.90 (+1.46); non-acoustic fit
                                                   (+0.47)
4  Bassline Riot         Kilowatt Kids       1.90  energy 0.96 vs target 0.90 (+1.41); non-acoustic fit
                                                   (+0.48)
5  Ashes and Iron        Grave Signal        1.89  energy 0.97 vs target 0.90 (+1.40); non-acoustic fit
                                                   (+0.49)
```

**ghost_genre**

```
Profile: ghost_genre  |  mode=balanced  diversity=off
Prefs: {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.7, 'likes_acoustic': False}

#  Title                 Artist             Score  Reasons
-----------------------------------------------------------------------------------------------------------
1  Rooftop Lights        Indigo Parade       2.74  mood match (+1.00); energy 0.76 vs target 0.70 (+1.41);
                                                   non-acoustic fit (+0.33)
2  Sunrise City          Neon Echo           2.73  mood match (+1.00); energy 0.82 vs target 0.70 (+1.32);
                                                   non-acoustic fit (+0.41)
3  Concrete Crown        Blockwise           1.82  energy 0.78 vs target 0.70 (+1.38); non-acoustic fit
                                                   (+0.44)
4  Night Drive Loop      Neon Echo           1.81  energy 0.75 vs target 0.70 (+1.42); non-acoustic fit
                                                   (+0.39)
5  Gospel Sunrise        Mount Zion Choir    1.68  energy 0.68 vs target 0.70 (+1.47); non-acoustic fit
                                                   (+0.21)
```

**acoustic_rager**

```
Profile: acoustic_rager  |  mode=balanced  diversity=off
Prefs: {'genre': 'metal', 'mood': 'angry', 'energy': 0.95, 'likes_acoustic': True}

#  Title                 Artist             Score  Reasons
-----------------------------------------------------------------------------------------------------------
1  Ashes and Iron        Grave Signal        4.48  genre match (+2.00); mood match (+1.00); energy 0.97 vs
                                                   target 0.95 (+1.47); acoustic fit (+0.01)
2  Bassline Riot         Kilowatt Kids       1.50  energy 0.96 vs target 0.95 (+1.48); acoustic fit (+0.01)
3  Gym Hero              Max Pulse           1.50  energy 0.93 vs target 0.95 (+1.47); acoustic fit (+0.03)
4  Storm Runner          Voltline            1.49  energy 0.91 vs target 0.95 (+1.44); acoustic fit (+0.05)
5  Ritmo de Noche        Calle Luna          1.45  energy 0.85 vs target 0.95 (+1.35); acoustic fit (+0.10)
```

**Profile comparisons**

- **Pop vs Lofi:** Pop leans toward high energy, produced tracks (Sunrise City, Gym Hero). Lofi flips to low energy acoustic tracks (Library Rain, Spacewalk Thoughts). The energy target and the acoustic flag pull the two lists to opposite ends of the catalog, which is what should happen.
- **Pop vs Rock:** Both have high energy targets, so Gym Hero shows up in both. For pop it earns the genre points; for rock it earns the "intense" mood points. Same song, different reason, which makes sense because Gym Hero is a loud, intense pop song.
- **Lofi vs Rock:** No overlap at all. Rock's top 5 are all above 0.85 energy and lofi's are all below 0.45. Energy closeness alone separates "chill lofi" from "intense rock."
- **Rock vs Sad but hyped:** Positions 2 to 5 are almost the same high energy songs, because once genre and mood stop matching, energy decides everything. The only difference is the #1 slot, where sad_but_hyped gets a slow indie song purely from labels.
- **Pop vs Ghost genre:** Both like happy songs around 0.7 to 0.8 energy, but ghost_genre never gets genre points, so its top score is only 2.74 vs 4.88 and Rooftop Lights and Sunrise City nearly tie. The system has nothing real for this user and does not say so.
- **Rock vs Acoustic rager:** Both want loud music. The acoustic flag barely matters (+0.01 to +0.10) because there are no loud acoustic songs in the data, so the acoustic rager basically gets the rock list with metal on top.

**Why does Gym Hero keep showing up?** In plain words: Gym Hero is labeled "pop," it is very high energy, and it sounds produced, not acoustic. Anyone who says "pop" gets 2 free points for it, and anyone who wants high energy gets nearly full energy points. So a "Happy Pop" listener sees it at #2 even though it is an intense workout song, because the system only knows the word "pop," not the feeling.

**Experiment (weight shift):** doubling energy (3.0) and halving genre (1.0) moved Rooftop Lights above Gym Hero for the pop profile. That felt more accurate. For sad_but_hyped it turned the #1 into a near tie (3.46 vs 3.42), so it got different, not clearly better. Output is in the README.

**Experiment (diversity penalty):** for lofi, LoRoom no longer takes two of the top 4 spots; Focus Flow drops from #3 to #4.

**Automated tests:** 7 pytest tests cover CSV loading, the scoring math, energy closeness, sort order, and the diversity penalty.

---

## 8. Future Work

- Partial genre matches (treat "indie pop" as close to both "indie" and "pop") using a small genre similarity map.
- Use tempo, valence and danceability in the score, and let users give a range instead of one value.
- Detect when there is no good match (like k-pop) and tell the user instead of showing filler.
- Add fake listening history so the system can try simple collaborative filtering.

---

## 9. Personal Reflection

**Biggest learning moment:** realizing that "recommend" just means "score everything and sort." The intelligence is all in the weights, and I was the one choosing them. Changing one number (genre 2.0 to 1.0) changed what a "happy pop" fan sees.

**How AI helped, and when I double-checked:** the AI was useful for explaining collaborative vs content-based filtering, suggesting the energy closeness formula, generating new songs in valid CSV format, and brainstorming adversarial profiles. I still had to check its work. I verified the scores by hand for Sunrise City (2.0 + 1.0 + 1.47 + 0.41 = 4.88), wrote a test that the energy rule rewards closeness and not magnitude, and fixed the starter import so `python -m src.main` actually runs.

**What surprised me:** even with four features and simple addition, the output *feels* like a real recommendation, especially with reasons attached. That made me realize how easy it is to trust a system that only looks smart.

**What I would try next:** a genre similarity map, using the unused audio features, and a "no good match" message so the system is honest about what it does not know.
