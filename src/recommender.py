import csv
from dataclasses import dataclass
from typing import List, Dict, Tuple

# Algorithm Recipe: how many points each check is worth
GENRE_POINTS = 2.0
MOOD_POINTS = 1.0
ENERGY_POINTS = 1.5
ACOUSTIC_POINTS = 0.5


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the list of songs."""
        self.songs = songs

    def make_prefs(self, user: UserProfile) -> Dict:
        """Turn a UserProfile into the dictionary that score_song expects."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for this user, best first."""
        prefs = self.make_prefs(user)
        scored = []
        for song in self.songs:
            score, reasons = score_song(prefs, vars(song))
            scored.append((song, score))
        scored = sorted(scored, key=lambda pair: pair[1], reverse=True)

        results = []
        for song, score in scored[:k]:
            results.append(song)
        return results

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a sentence explaining the song's score."""
        score, reasons = score_song(self.make_prefs(user), vars(song))
        return f"Score {score:.2f}: " + ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read the songs CSV into a list of dictionaries with numbers converted."""
    songs = []
    with open(csv_path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match
    if song["genre"] == user_prefs.get("genre"):
        score = score + GENRE_POINTS
        reasons.append(f"genre match (+{GENRE_POINTS})")

    # Mood match
    if song["mood"] == user_prefs.get("mood"):
        score = score + MOOD_POINTS
        reasons.append(f"mood match (+{MOOD_POINTS})")

    # Energy: closer to the target = more points
    if "energy" in user_prefs:
        gap = abs(song["energy"] - user_prefs["energy"])
        energy_score = ENERGY_POINTS * (1 - gap)
        score = score + energy_score
        reasons.append(f"energy close to target (+{energy_score:.2f})")

    # Acoustic: reward acoustic songs for acoustic fans, and the opposite for everyone else
    if "likes_acoustic" in user_prefs:
        if user_prefs["likes_acoustic"]:
            acoustic_score = ACOUSTIC_POINTS * song["acousticness"]
        else:
            acoustic_score = ACOUSTIC_POINTS * (1 - song["acousticness"])
        score = score + acoustic_score
        reasons.append(f"acoustic fit (+{acoustic_score:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort from highest to lowest, and return the top k."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    # sorted() makes a new sorted list. item[1] is the score.
    scored = sorted(scored, key=lambda item: item[1], reverse=True)
    return scored[:k]
