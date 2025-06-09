FROM python:3.9-slim

WORKDIR /opt/brain-agriculture/

COPY requirements.txt alembic.ini ./main.py .
COPY ./tests ./tests
COPY ./alembic ./alembic
COPY ./app ./app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["python", "main.py"] 
