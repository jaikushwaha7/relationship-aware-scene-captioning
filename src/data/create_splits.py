import os
import random
import shutil

BASE_DIR = "data/processed/detection"
OUT_DIR = "data/splits"
SPLITS = {"train": 0.7, "val": 0.15, "test": 0.15}


def main():
    images = sorted(os.listdir(os.path.join(BASE_DIR, "images")))
    random.shuffle(images)

    n = len(images)
    splits = {
        "train": images[: int(0.7 * n)],
        "val": images[int(0.7 * n): int(0.85 * n)],
        "test": images[int(0.85 * n):]
    }

    for split, files in splits.items():
        img_dir = os.path.join(OUT_DIR, split, "images")
        lbl_dir = os.path.join(OUT_DIR, split, "labels")
        os.makedirs(img_dir, exist_ok=True)
        os.makedirs(lbl_dir, exist_ok=True)

        for img in files:
            shutil.copy(
                os.path.join(BASE_DIR, "images", img),
                os.path.join(img_dir, img)
            )
            lbl = img.replace(".jpg", ".txt")
            shutil.copy(
                os.path.join(BASE_DIR, "labels", lbl),
                os.path.join(lbl_dir, lbl)
            )

    print("Train/Val/Test splits created.")


if __name__ == "__main__":
    main()
