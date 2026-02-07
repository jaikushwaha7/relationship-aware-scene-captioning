import os
import json
import glob
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

# --- CONFIGURATION (Replacing Argparse) ---
RAW_VG_DIR = "data/raw/visual_genome"
SUBSET_PATH = "data/processed/vg_5k_subset.json"
TARGET_INDEX = 0  # Change this to view different images
SAVE_PATH = ""    # Provide a path if you want to save the output

# --- HELPER FUNCTIONS ---

def load_subset(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Subset file not found at {path}")
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
        x, y, w, h = obj.get("x", 0), obj.get("y", 0), obj.get("w", 0), obj.get("h", 0)
        label = get_object_label(obj)
        draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
        draw.text((x + 3, y + 3), label, fill="yellow")

# --- EXECUTION ---

# 1. Load Data
subset = load_subset(SUBSET_PATH)
entry = subset[TARGET_INDEX]
image_id = entry["image_id"]
objects = entry.get("objects", [])
relationships = entry.get("relationships", [])

# 2. Find and Process Image
image_path = find_image_path(image_id)
if not image_path:
    print(f"Error: Image {image_id} not found.")
else:
    # print(f"Displaying Image ID: {image_id}")
    # image = Image.open(image_path).convert("RGB")
    # draw_objects(image, objects)

    # # 3. Visualization
    # plt.figure(figsize=(12, 10))
    # plt.imshow(image)
    # plt.axis("off")

    # # Title with top 3 relationships
    # rel_summary = "; ".join(get_rel_text(rel) for rel in relationships[:3])
    # plt.title(f"Relationships: {rel_summary}...", fontsize=10)
    
    # if SAVE_PATH:
    #     image.save(SAVE_PATH)
    #     print(f"Saved to {SAVE_PATH}")
        
    # plt.show()
    pass
from ipywidgets import interact, IntSlider

# Load the data once
subset = load_subset(SUBSET_PATH)

def view_image(index):
    """Function to render the image based on the slider index"""
    entry = subset[index]
    image_id = entry["image_id"]
    objects = entry.get("objects", [])
    relationships = entry.get("relationships", [])

    image_path = find_image_path(image_id)
    if not image_path:
        print(f"Error: Image {image_id} not found.")
        return

    # Process and display
    image = Image.open(image_path).convert("RGB")
    draw_objects(image, objects)

    plt.figure(figsize=(12, 8))
    plt.imshow(image)
    plt.axis("off")
    
    # Show first 3 relationships in title
    rel_summary = "; ".join(get_rel_text(rel) for rel in relationships[:3])
    plt.title(f"Index: {index} | ID: {image_id}\n{rel_summary}...", fontsize=12)
    plt.show()

# Create the interactive slider
interact(
    view_image, 
    index=IntSlider(
        min=0, 
        max=len(subset)-1, 
        step=1, 
        value=0, 
        description='Image Index:',
        continuous_update=False # Wait until you release the slider to update
    )
)