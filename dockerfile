FROM python:3.11.1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

COPY /app /app/

CMD ["python", "your_app.py"]
