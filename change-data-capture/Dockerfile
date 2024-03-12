FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y default-mysql-client

CMD ["python", "flux.py", "tail", "-f", "/dev/null"]