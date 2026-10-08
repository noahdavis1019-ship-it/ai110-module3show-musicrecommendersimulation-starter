from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


from src.recommender import load_songs, score_song, recommend_songs


def test_load_songs_converts_numeric_fields():
    songs = load_songs("data/songs.csv")
    assert len(songs) >= 10
    assert isinstance(songs[0]["energy"], float)
    assert isinstance(songs[0]["id"], int)


def test_score_song_returns_score_and_reasons():
    prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "pop", "mood": "happy", "energy": 0.8, "acousticness": 0.2}
    score, reasons = score_song(prefs, song)
    assert score == 4.5  # 2.0 genre + 1.0 mood + 1.5 perfect energy
    assert any("genre match" in r for r in reasons)


def test_energy_rewards_closeness_not_magnitude():
    prefs = {"energy": 0.3}
    near = {"genre": "x", "mood": "x", "energy": 0.3, "acousticness": 0.5}
    far = {"genre": "x", "mood": "x", "energy": 0.9, "acousticness": 0.5}
    assert score_song(prefs, near)[0] > score_song(prefs, far)[0]


def test_recommend_songs_sorted_and_limited():
    songs = load_songs("data/songs.csv")
    recs = recommend_songs({"genre": "lofi", "mood": "chill", "energy": 0.35}, songs, k=3)
    assert len(recs) == 3
    scores = [s for _, s, _ in recs]
    assert scores == sorted(scores, reverse=True)
    assert recs[0][0]["genre"] == "lofi"


def test_diversity_penalty_demotes_repeat_artist():
    songs = load_songs("data/songs.csv")
    prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}
    plain = [s["title"] for s, _, _ in recommend_songs(prefs, songs, k=5)]
    diverse = [s["title"] for s, _, _ in recommend_songs(prefs, songs, k=5, diversity=True)]
    assert plain.index("Focus Flow") < diverse.index("Focus Flow")
