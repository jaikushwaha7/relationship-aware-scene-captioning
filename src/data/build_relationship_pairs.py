import json

INPUT_FILE = "data/processed/vg_5k_subset.json"
LABEL_MAP = "data/processed/label_map.json"
OUTPUT_FILE = "data/processed/relationships/relationship_pairs.json"


def normalize_bbox(obj, img_w, img_h):
    xc = (obj["x"] + obj["w"] / 2) / img_w
    yc = (obj["y"] + obj["h"] / 2) / img_h
    return [xc, yc, obj["w"] / img_w, obj["h"] / img_h]


def main():
    data = json.load(open(INPUT_FILE))
    label_map = json.load(open(LABEL_MAP))

    pairs = []

    for item in data:
        image_id = item["image_id"]

        for rel in item["relationships"]:
            subj = rel["subject"]
            obj = rel["object"]
            predicate = rel["predicate"].lower()

            subj_name = subj["names"][0].lower()
            obj_name = obj["names"][0].lower()

            if subj_name not in label_map or obj_name not in label_map:
                continue

            pairs.append({
                "image_id": image_id,
                "subject": {
                    "class": label_map[subj_name],
                    "bbox": normalize_bbox(subj, rel["width"], rel["height"])
                },
                "object": {
                    "class": label_map[obj_name],
                    "bbox": normalize_bbox(obj, rel["width"], rel["height"])
                },
                "predicate": predicate
            })

    json.dump(pairs, open(OUTPUT_FILE, "w"))
    print(f"Saved {len(pairs)} relationship pairs")


if __name__ == "__main__":
    main()
