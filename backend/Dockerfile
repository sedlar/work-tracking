FROM python:3.7

RUN mkdir -p /app

WORKDIR /app
COPY ./requirements.txt /app/
COPY ./requirements-dev.txt /app/
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
ENV PYTHONPATH /app
COPY ./src /app
COPY ./tests /app/tests

EXPOSE 8000
CMD ["python", "/app/wt/app.py"]
