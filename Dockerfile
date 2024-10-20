FROM python:3.12

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx  libxrender-dev libx11-6 libxext-dev libxinerama-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev tk-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install -r requirments.txt



CMD ["python3","main.py"] 