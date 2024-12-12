FROM python:3.12
RUN mkdir /app
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
