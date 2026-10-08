"""
Command line runner for the Music Recommender Simulation.

Usage:
    python -m src.main                       # run every profile, balanced mode
    python -m src.main --profile pop         # one profile
    python -m src.main --mode energy_focused # switch scoring strategy
    python -m src.main --diversity           # penalize repeat artists/genres
"""

import argparse
import textwrap

try:
    from src.recommender import SCORING_MODES, load_songs, recommend_songs
except ImportError:  # allows `python src/main.py` too
    from recommender import SCORING_MODES, load_songs, recommend_songs


PROFILES = {
    # Core profiles
    "pop": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    # Adversarial / edge-case profiles
    "sad_but_hyped": {"genre": "indie", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
    "ghost_genre": {"genre": "k-pop", "mood": "happy", "energy": 0.7, "likes_acoustic": False},
    "acoustic_rager": {"genre": "metal", "mood": "angry", "energy": 0.95, "likes_acoustic": True},
}


def format_table(recs) -> str:
    """Render recommendations as an ASCII table that includes the reasons."""
    width = 58
    lines = [f"{'#':<3}{'Title':<22}{'Artist':<18}{'Score':>6}  Reasons", "-" * (49 + width)]
    for i, (song, score, explanation) in enumerate(recs, 1):
        wrapped = textwrap.wrap(explanation, width) or [""]
        lines.append(f"{i:<3}{song['title'][:21]:<22}{song['artist'][:17]:<18}{score:>6.2f}  {wrapped[0]}")
        for extra in wrapped[1:]:
            lines.append(f"{'':<49}  {extra}")
    return "\n".join(lines)


def run_profile(name: str, prefs: dict, songs, k: int, mode: str, diversity: bool) -> None:
    """Print the top k recommendations for one named profile."""
    recs = recommend_songs(prefs, songs, k=k, mode=mode, diversity=diversity)
    print(f"\nProfile: {name}  |  mode={mode}  diversity={'on' if diversity else 'off'}")
    print(f"Prefs: {prefs}\n")
    print(format_table(recs))
    print()


def main() -> None:
    """Load songs, parse CLI flags, and print recommendations."""
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument("--profile", choices=list(PROFILES), help="run one profile only")
    parser.add_argument("--mode", default="balanced", choices=list(SCORING_MODES))
    parser.add_argument("--diversity", action="store_true", help="penalize repeat artists/genres")
    parser.add_argument("-k", type=int, default=5)
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    targets = {args.profile: PROFILES[args.profile]} if args.profile else PROFILES
    for name, prefs in targets.items():
        run_profile(name, prefs, songs, args.k, args.mode, args.diversity)


if __name__ == "__main__":
    main()
