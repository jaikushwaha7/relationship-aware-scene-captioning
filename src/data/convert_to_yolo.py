import json
import os
from PIL import Image

VG_IMAGE_DIR = "data/raw/visual_genome/VG_100K"
INPUT_FILE = "data/processed/vg_5k_subset.json"
LABEL_MAP = "data/processed/label_map.json"
OUTPUT_DIR = "data/processed/detection"


def normalize_bbox(x, y, w, h, img_w, img_h):
    xc = (x + w / 2) / img_w
    yc = (y + h / 2) / img_h
    w /= img_w
    h /= img_h
    return xc, yc, w, h


def main():
    data = json.load(open(INPUT_FILE))
    label_map = json.load(open(LABEL_MAP))

    img_out = os.path.join(OUTPUT_DIR, "images")
    lbl_out = os.path.join(OUTPUT_DIR, "labels")
    os.makedirs(img_out, exist_ok=True)
    os.makedirs(lbl_out, exist_ok=True)

    for item in data:
        image_id = item["image_id"]
        img_name = f"{image_id}.jpg"
        img_path = os.path.join(VG_IMAGE_DIR, img_name)

        if not os.path.exists(img_path):
            continue

        img = Image.open(img_path)
        W, H = img.size

        yolo_lines = []

        for obj in item["objects"]:
            name = obj["names"][0].lower()
            if name not in label_map:
                continue

            bbox = obj
            x, y, w, h = bbox["x"], bbox["y"], bbox["w"], bbox["h"]
            xc, yc, bw, bh = normalize_bbox(x, y, w, h, W, H)

            class_id = label_map[name]
            yolo_lines.append(f"{class_id} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}")

        if not yolo_lines:
            continue

        img.save(os.path.join(img_out, img_name))
        with open(os.path.join(lbl_out, f"{image_id}.txt"), "w") as f:
            f.write("\n".join(yolo_lines))

    print("YOLO conversion completed.")


if __name__ == "__main__":
    main()
