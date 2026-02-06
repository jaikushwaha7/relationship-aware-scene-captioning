import json
import os
import random
from tqdm import tqdm

RAW_VG_DIR = "data/raw/visual_genome"
OUTPUT_DIR = "data/processed"
TARGET_IMAGE_COUNT = 5000

SPATIAL_RELATIONS = {
    "left of",
    "right of",
    "in front of",
    "behind",
    "on top of",
    "under",
    "inside",
    "around",
    "over",
    "next to"
}


def normalize_predicate(text):
    return text.lower().strip()


def load_json(filename):
    with open(os.path.join(RAW_VG_DIR, filename), "r") as f:
        return json.load(f)


def main():
    print("Loading Visual Genome annotations...")
    relationships = load_json("relationships.json")
    objects = load_json("objects.json")

    valid_images = []
    image_to_objects = {}

    # Map objects by image_id
    for entry in objects:
        image_id = entry["image_id"]
        image_to_objects[image_id] = entry["objects"]

    print("Filtering images by spatial relationships...")

    for entry in tqdm(relationships):
        image_id = entry["image_id"]
        rels = entry["relationships"]

        if image_id not in image_to_objects:
            continue

        filtered_rels = []
        for r in rels:
            predicate = normalize_predicate(r["predicate"])

            if predicate in SPATIAL_RELATIONS:
                filtered_rels.append(r)

        if len(filtered_rels) > 0:
            valid_images.append({
                "image_id": image_id,
                "relationships": filtered_rels,
                "objects": image_to_objects[image_id]
            })

    print(f"Total valid images found: {len(valid_images)}")

    random.shuffle(valid_images)
    subset = valid_images[:TARGET_IMAGE_COUNT]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, "vg_5k_subset.json")
    with open(output_path, "w") as f:
        json.dump(subset, f)

    print(f"Saved 5K subset to: {output_path}")


if __name__ == "__main__":
    main()
