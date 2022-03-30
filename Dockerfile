from manimcommunity/manim:v0.13.1 as builder
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
