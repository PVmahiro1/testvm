FROM bitnami/python:3.8


WORKDIR /bot

# Install python requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /bot
CMD ["python", "main.py"]