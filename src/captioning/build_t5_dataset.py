import json
from serialize_graph import serialize_scene

INPUT = "data/processed/vg_5k_subset.json"
OUTPUT = "data/processed/scene_graphs/t5_data.json"

def main():
    data = json.load(open(INPUT))
    samples = []

    for item in data:
        objects = {o["object_id"]: o["names"][0] for o in item["objects"]}
        rels = []

        for r in item["relationships"]:
            rels.append({
                "subject": objects[r["subject"]["object_id"]],
                "predicate": r["predicate"],
                "object": objects[r["object"]["object_id"]],
            })

        graph = serialize_scene(objects, rels)
        caption = item.get("image_caption", "")  # if available

        samples.append({"input": graph, "target": caption})

    json.dump(samples, open(OUTPUT, "w"), indent=2)

if __name__ == "__main__":
    main()
