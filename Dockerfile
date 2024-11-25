FROM python:3.11.9-alpine3.20

MAINTAINER CesarSanchez "cesar.sanchez@conext.com.ve"

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r requeriments.txt

EXPOSE 8000

CMD ["fastapi", "run","--workers","4","--port", "8000"]