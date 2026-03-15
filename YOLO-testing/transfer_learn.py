from ultralytics import YOLO
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load a pre-trained YOLO model (e.g., YOLOv8n - nano version)
model = YOLO('yolo11n.pt')

# Train the model on your custom dataset
model.train(
    data='data.yaml',  # Path to dataset YAML file (defines train/val splits and classes)
    epochs=5,                         # Number of epochs to train
    imgsz=640,                         # Input image size
    batch=16,                          # Batch size
    name='custom_yolo11_model',        # Name for the experiment
    pretrained=True                    # Use pre-trained weights
)

# Evaluate the model
metrics = model.val(data="data.yaml", save_json=True, device=device)
print(metrics.box.maps)

# Export the model to various formats (e.g., ONNX, CoreML, TensorRT)
model.export(format='onnx')