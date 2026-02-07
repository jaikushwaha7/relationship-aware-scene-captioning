import json
from collections import Counter

data = json.load(open("data/processed/vg_5k_subset.json"))

obj_counter = Counter()
rel_counter = Counter()

for item in data:
    for o in item["objects"]:
        obj_counter[o["names"][0].lower()] += 1
    for r in item["relationships"]:
        rel_counter[r["predicate"].lower()] += 1

print("Top Objects:", obj_counter.most_common(10))
print("Top Relations:", rel_counter.most_common(10))
