import argparse
from pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Content Creation Pipeline")
    parser.add_argument("--topic", required=True, help="Topic to write about")
    args = parser.parse_args()
    final = run_pipeline(args.topic)
    print("\n=== FINAL CONTENT ===\n")
    print(final)


if __name__ == "__main__":
    main()