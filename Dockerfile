FROM python:3.10-slim

WORKDIR app/
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["bash", "entrypoint.sh"]
