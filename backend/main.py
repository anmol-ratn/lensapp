from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch
import json
from torchvision.models import resnet18
from torchvision import transforms
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_methods=["*"],
)


@app.post("/")
async def root(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")

    preprocess = transforms.Compose(
        [
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    model = resnet18(pretrained=True)
    model.eval()
    output = model(torch.unsqueeze(preprocess(image), 0))

    with open("imagenet_labels.json", "r") as f:
        labels = json.load(f)

    percentage = torch.nn.functional.softmax(output, dim=1)[0] * 100

    _, indices = torch.sort(output, descending=True)
    li = [
        f'{labels[str(idx.item())].split(",")[0].upper()} ({percentage[idx.item()].item():.4f})'
        for idx in indices[0][:3]
    ]

    return {"data": li}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3001, reload=True)
