import argparse
import glob
import json
import os

from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

RAW_VG_DIR = "data/raw/visual_genome"
SUBSET_PATH = "data/processed/vg_5k_subset.json"


def load_subset(path):
    with open(path, "r") as f:
        return json.load(f)


def find_image_path(image_id):
    candidates = [
        os.path.join(RAW_VG_DIR, "VG_100K", f"{image_id}.jpg"),
        os.path.join(RAW_VG_DIR, "VG_100K_2", f"{image_id}.jpg"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path

    # Fallback to any extension
    patterns = [
        os.path.join(RAW_VG_DIR, "VG_100K", f"{image_id}.*"),
        os.path.join(RAW_VG_DIR, "VG_100K_2", f"{image_id}.*"),
    ]
    for pattern in patterns:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

    return None


def get_object_label(obj):
    if "names" in obj and obj["names"]:
        return obj["names"][0]
    if "name" in obj and obj["name"]:
        return obj["name"]
    return f"id:{obj.get('object_id', 'unknown')}"


def get_rel_text(rel):
    subject = rel.get("subject", {})
    obj = rel.get("object", {})
    predicate = rel.get("predicate", "")
    subj_name = get_object_label(subject)
    obj_name = get_object_label(obj)
    return f"{subj_name} {predicate} {obj_name}".strip()


def draw_objects(image, objects):
    draw = ImageDraw.Draw(image)
    for obj in objects:
        x = obj.get("x", 0)
        y = obj.get("y", 0)
        w = obj.get("w", 0)
        h = obj.get("h", 0)
        label = get_object_label(obj)

        # Bounding box
        draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
        draw.text((x + 3, y + 3), label, fill="yellow")


def main():
    parser = argparse.ArgumentParser(description="Test one VG subset image.")
    parser.add_argument("--subset", default=SUBSET_PATH, help="Path to subset json.")
    parser.add_argument("--index", type=int, default=0, help="Index in subset list.")
    parser.add_argument("--save", default="", help="Optional path to save annotated image.")
    args = parser.parse_args()

    subset = load_subset(args.subset)
    if not subset:
        raise ValueError("Subset is empty.")

    if args.index < 0 or args.index >= len(subset):
        raise IndexError(f"Index {args.index} out of range (0..{len(subset) - 1}).")

    entry = subset[args.index]
    image_id = entry["image_id"]
    objects = entry.get("objects", [])
    relationships = entry.get("relationships", [])

    print("Step 1: Load + display image")
    image_path = find_image_path(image_id)
    if not image_path:
        raise FileNotFoundError(f"Could not find image for id {image_id} in VG_100K/ or VG_100K_2/.")
    print(f"Image id: {image_id}")
    print(f"Image path: {image_path}")

    print("\nStep 2: Print relationships + objects")
    print(f"Objects: {len(objects)}")
    print(f"Relationships: {len(relationships)}")
    for i, rel in enumerate(relationships[:20], 1):
        print(f"  {i}. {get_rel_text(rel)}")
    if len(relationships) > 20:
        print("  ...")

    print("\nStep 3: Draw boxes + relation text")
    image = Image.open(image_path).convert("RGB")
    draw_objects(image, objects)

    plt.figure(figsize=(10, 8))
    plt.imshow(image)
    plt.axis("off")

    # Render a short relation summary as a title
    rel_summary = "; ".join(get_rel_text(rel) for rel in relationships[:5])
    if len(relationships) > 5:
        rel_summary += "; ..."
    plt.title(rel_summary)

    if args.save:
        os.makedirs(os.path.dirname(args.save), exist_ok=True)
        image.save(args.save)
        print(f"Saved annotated image to: {args.save}")

    plt.show()


if __name__ == "__main__":
    main()
