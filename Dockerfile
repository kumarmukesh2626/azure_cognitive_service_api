FROM python:3.8-slim-buster

COPY . /app

WORKDIR /app

RUN pip install --upgrade cython

RUN apt-get -y update

RUN pip install --upgrade pip

RUN apt install -y libgl1-mesa-glx

RUN apt install -y libglib2.0-0

RUN pip install --no-cache-dir -r /app/requirements_dev.txt

EXPOSE 5000

CMD ["python","App.py"]