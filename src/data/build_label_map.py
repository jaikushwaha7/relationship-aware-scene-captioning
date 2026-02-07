import json
from collections import Counter

INPUT_FILE = "data/processed/vg_5k_subset.json"
OUTPUT_FILE = "data/processed/label_map.json"
TOP_K = 150  # limit vocabulary size


def main():
    data = json.load(open(INPUT_FILE))
    counter = Counter()

    for item in data:
        for obj in item["objects"]:
            name = obj["names"][0].lower()
            counter[name] += 1

    most_common = counter.most_common(TOP_K)
    label_map = {name: idx for idx, (name, _) in enumerate(most_common)}

    json.dump(label_map, open(OUTPUT_FILE, "w"), indent=2)
    print(f"Saved {len(label_map)} object classes")


if __name__ == "__main__":
    main()
