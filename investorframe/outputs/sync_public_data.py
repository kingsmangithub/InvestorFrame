import shutil

from investorframe.app.config import DATA_DIR, ROOT

PUBLIC_DATA_DIR = ROOT / "dashboard" / "public" / "data"


def main() -> None:
    PUBLIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for source in DATA_DIR.glob("*.json"):
        shutil.copy2(source, PUBLIC_DATA_DIR / source.name)
    print(f"Synced {len(list(DATA_DIR.glob('*.json')))} files to {PUBLIC_DATA_DIR}")


if __name__ == "__main__":
    main()
