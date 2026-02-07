def serialize_scene(objects, relationships):
    parts = []

    for r in relationships:
        subj = r["subject"]
        obj = r["object"]
        pred = r["predicate"]
        parts.append(f"{subj} {pred} {obj}")

    return "; ".join(parts)
