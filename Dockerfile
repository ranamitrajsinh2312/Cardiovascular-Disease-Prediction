# Dockerfile for Render deployment
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install -r streamlit_requirements.txt

EXPOSE 5000

CMD ["gunicorn", "api_server:app", "--bind", "0.0.0.0:5000"]
