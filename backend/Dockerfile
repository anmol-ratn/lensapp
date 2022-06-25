FROM python:3.8.10-slim

WORKDIR /app

COPY main.py imagenet_labels.json ./

RUN pip3 install wheel
RUN pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install fastapi
RUN pip3 install "uvicorn[standard]"
RUN pip3 install python-multipart

EXPOSE 3001

CMD ["python3", "main.py"]
