FROM python:3.10-alpine


RUN apk update && \
    apk upgrade

# Set workdir
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python3", "app.py"]
