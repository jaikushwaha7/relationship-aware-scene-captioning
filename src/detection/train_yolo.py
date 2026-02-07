from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")  # lightweight, good for VG

    model.train(
        data="configs/yolo.yaml",
        epochs=1,
        imgsz=640,
        batch=16,
        project="experiments",
        name="yolo_vg"
    )

if __name__ == "__main__":
    main()
