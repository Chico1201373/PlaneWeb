
FROM python:3.9
WORKDIR /usr/src/app
COPY app.py .
COPY requirements.txt .
CMD ["python", "app.py"] 
