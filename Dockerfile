FROM python:3.8-slim-buster 

WORKDIR /code

RUN python3 -m pip install --upgrade pip 

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8080

CMD ["gunicorn", "--workers=3", "--bind", "0.0.0.0:8080", "app:app"]
