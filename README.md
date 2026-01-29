# relationship-aware-scene-captioning

# RASC: Relationship-Aware Scene Captioning for Accessibility

## 📌 Overview

RASC is a computer vision and vision-language project that generates **relationship-aware scene descriptions** to improve accessibility for visually impaired users. Instead of listing detected objects, the system explicitly models **spatial relationships** (e.g., *left of*, *on*, *near*) and produces cognitively meaningful natural language descriptions.

**Example:**

> *"A person walking a dog on the left side of a tree-lined street."*

---

## 🎯 Motivation

Most existing accessibility tools provide flat object lists or generic captions that miss spatial and relational context. This project addresses that gap by explicitly learning object relationships and converting them into natural language descriptions that better support scene understanding and navigation.

---

## 🧠 Method Overview

We use a **three-stage pipeline**:

1. **Object Detection**

   * YOLOv8 pretrained on COCO (optionally fine-tuned on Visual Genome)

2. **Relationship Prediction**

   * Scene Graph Generation using learned spatial relationships or geometry-based rules

3. **Scene Graph → Text**

   * T5-small fine-tuned to convert structured scene graphs into natural language descriptions

```
Image → YOLOv8 → Scene Graph (Objects + Relationships) → T5 → Caption
```

---

## 📊 Dataset

* **Visual Genome** (Krishna et al., 2017)
* ~5,000 image subset
* Focus on 10 object categories and 10 spatial relationships

Dataset links:

* [https://visualgenome.org/](https://visualgenome.org/)
* [https://visualgenome.org/api/v0/api_home.html](https://visualgenome.org/api/v0/api_home.html)

---

## 🧪 Evaluation

We evaluate each stage independently:

* **Object Detection:** mAP@0.5
* **Relationship Prediction:** F1-score
* **Captioning:** CIDEr

### Ablation Studies

* Pretrained vs fine-tuned detector
* Learned vs rule-based relationship modeling

---

## ⚠️ Limitations

* Limited dataset subset (5K images)
* Only spatial relationships (no temporal or causal reasoning)
* No user study with visually impaired participants
* Multi-stage pipeline may propagate errors

---

## 👥 Team & Contributions

* **Jai Kushwaha** — Object detection, relationship modeling, evaluation
* **Caner Gel** — Caption generation, poster design, presentation

---


## 📚 References

* Krishna et al., *Visual Genome*, IJCV 2017
* Zellers et al., *Neural Motifs*, CVPR 2018
* Raffel et al., *T5*, JMLR 2020
* Ultralytics, *YOLOv8*, 2023

---

## 📄 License

MIT License
