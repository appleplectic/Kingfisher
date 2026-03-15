import torch
from ultralytics import YOLO

if __name__ == '__main__':
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = YOLO("yolo11l.pt")
    metrics = model.val(data="data.yaml", save_json=True, device=device)
    print(metrics.box.maps)
