FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip 
RUN pip install -r /app/requirements.txt

COPY ./fastApi /app/fastApi/

CMD ["uvicorn", "fastApi.main:app", "--host", "0.0.0.0", "--port", "10100"]