"""
Command line runner for the Music Recommender Simulation.

Run with: python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(name, user_prefs, songs):
    """Print the top 5 songs for one user profile."""
    print("=" * 50)
    print(f"Profile: {name}")
    print(f"Prefs: {user_prefs}")
    print("=" * 50)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    rank = 1
    for song, score, explanation in recommendations:
        print(f"{rank}. {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"   Because: {explanation}")
        rank = rank + 1
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Three normal profiles
    pop = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    lofi = {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}
    rock = {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False}

    # Edge case profiles meant to "trick" the scoring
    sad_but_hyped = {"genre": "indie", "mood": "sad", "energy": 0.9, "likes_acoustic": False}
    ghost_genre = {"genre": "k-pop", "mood": "happy", "energy": 0.7, "likes_acoustic": False}
    acoustic_rager = {"genre": "metal", "mood": "angry", "energy": 0.95, "likes_acoustic": True}

    print_recommendations("High-Energy Pop", pop, songs)
    print_recommendations("Chill Lofi", lofi, songs)
    print_recommendations("Deep Intense Rock", rock, songs)
    print_recommendations("Sad but Hyped (edge case)", sad_but_hyped, songs)
    print_recommendations("Genre Not in Catalog (edge case)", ghost_genre, songs)
    print_recommendations("Acoustic Metal Fan (edge case)", acoustic_rager, songs)


if __name__ == "__main__":
    main()
