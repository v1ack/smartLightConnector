FROM python:3.10.5-bullseye

WORKDIR /app
ENV PYTHONPATH /app

RUN apt-get update && apt-get install -y libdbus-glib-1-dev libdbus-1-dev libglib2.0-dev python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev gcc libcairo2-dev pkg-config

COPY requirements.server.txt ./
RUN pip install --no-cache-dir -r requirements.server.txt

COPY . .


CMD [ "uvicorn", "ble_light.server:app", "--host", "0.0.0.0" ]