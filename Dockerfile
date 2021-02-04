FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 7070

COPY ./src /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7070"]
