import csv
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Algorithm Recipe weights (default "balanced" mode)
# ---------------------------------------------------------------------------
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.5
ACOUSTIC_WEIGHT = 0.5

# Scoring modes (Strategy pattern): each mode is just a set of weights.
SCORING_MODES: Dict[str, Dict[str, float]] = {
    "balanced": {"genre": 2.0, "mood": 1.0, "energy": 1.5, "acoustic": 0.5},
    "genre_first": {"genre": 3.0, "mood": 0.5, "energy": 1.0, "acoustic": 0.25},
    "mood_first": {"genre": 1.0, "mood": 2.5, "energy": 1.5, "acoustic": 0.5},
    "energy_focused": {"genre": 1.0, "mood": 1.0, "energy": 3.0, "acoustic": 0.5},
}

INT_FIELDS = {"id"}
FLOAT_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}


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

    def to_prefs(self) -> Dict:
        """Convert this profile into the dict format used by score_song."""
        return {
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "likes_acoustic": self.likes_acoustic,
        }


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song], mode: str = "balanced"):
        """Store the catalog and the scoring mode to use."""
        self.songs = songs
        self.mode = mode

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, best first."""
        prefs = user.to_prefs()
        scored = [(song, score_song(prefs, asdict(song), self.mode)[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation of why this song got its score."""
        score, reasons = score_song(user.to_prefs(), asdict(song), self.mode)
        return f"Score {score:.2f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts with numeric fields converted."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in INT_FIELDS:
                row[key] = int(row[key])
            for key in FLOAT_FIELDS:
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Score one song against user prefs and return (score, reasons)."""
    w = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    score = 0.0
    reasons: List[str] = []

    # Categorical matches (case-insensitive exact match)
    if str(song["genre"]).lower() == str(user_prefs.get("genre", "")).lower():
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.2f})")

    if str(song["mood"]).lower() == str(user_prefs.get("mood", "")).lower():
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.2f})")

    # Numeric closeness: reward being NEAR the target, not just high or low
    if "energy" in user_prefs:
        gap = abs(float(song["energy"]) - float(user_prefs["energy"]))
        pts = w["energy"] * (1 - gap)
        score += pts
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{pts:.2f})")

    # Acoustic preference
    if "likes_acoustic" in user_prefs:
        a = float(song["acousticness"])
        fit = a if user_prefs["likes_acoustic"] else 1 - a
        pts = w["acoustic"] * fit
        score += pts
        label = "acoustic" if user_prefs["likes_acoustic"] else "non-acoustic"
        reasons.append(f"{label} fit (+{pts:.2f})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort high to low, and return the top k with explanations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode)
        scored.append((song, score, reasons))

    # sorted() returns a NEW list and leaves `songs` untouched; .sort() would mutate in place.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    if diversity:
        ranked = apply_diversity_penalty(ranked, k)

    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]


def apply_diversity_penalty(
    ranked: List[Tuple[Dict, float, List[str]]],
    k: int,
    artist_penalty: float = 1.0,
    genre_penalty: float = 0.5,
) -> List[Tuple[Dict, float, List[str]]]:
    """Greedily build a top list, penalizing repeat artists and genres already picked."""
    remaining = list(ranked)
    picked: List[Tuple[Dict, float, List[str]]] = []
    while remaining and len(picked) < k:
        seen_artists = {s["artist"] for s, _, _ in picked}
        seen_genres = {s["genre"] for s, _, _ in picked}
        best_i, best_adj, best_reasons = 0, None, None
        for i, (song, score, reasons) in enumerate(remaining):
            adj, extra = score, []
            if song["artist"] in seen_artists:
                adj -= artist_penalty
                extra.append(f"repeat artist (-{artist_penalty:.2f})")
            if song["genre"] in seen_genres:
                adj -= genre_penalty
                extra.append(f"repeat genre (-{genre_penalty:.2f})")
            if best_adj is None or adj > best_adj:
                best_i, best_adj, best_reasons = i, adj, reasons + extra
        song, _, _ = remaining.pop(best_i)
        picked.append((song, best_adj, best_reasons))
    return picked + remaining
