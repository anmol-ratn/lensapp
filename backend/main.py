from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import json
from torchvision.models import resnet18, ResNet18_Weights
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)


def read_rgb_image_from_file(file):
    return Image.open(file).convert("RGB")


def get_model_inference(model_arch, weights, image):
    model = model_arch(weights=weights)
    model.eval()
    processed_image = weights.transforms()(image)
    input = torch.unsqueeze(processed_image, 0)  # Adds extra dimension to image
    return model(input)


def get_top_three_labels_with_percentage(output):

    # Reads the thousand labels of imagenet dataset from the accompanied file
    with open("imagenet_labels.json", "r") as f:
        labels = json.load(f)

    percentage = torch.nn.functional.softmax(output, dim=1)[0] * 100

    _, indices = torch.sort(output, descending=True)
    li = [
        f'{labels[str(idx.item())].split(",")[0].upper()} ({percentage[idx.item()].item():.4f})'
        for idx in indices[0][:3]
    ]

    return li


@app.post("/")
async def root(file: UploadFile = File(...)):
    image = read_rgb_image_from_file(file.file)
    output = get_model_inference(resnet18, ResNet18_Weights.DEFAULT, image)
    top_three_results = get_top_three_labels_with_percentage(output)
    return {"data": top_three_results}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True)
