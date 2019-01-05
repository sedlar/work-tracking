FROM python:3.7

RUN mkdir -p /app

WORKDIR /app
COPY ./requirements.txt /app/
COPY ./requirements-dev.txt /app/
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
ENV PYTHONPATH /app
COPY ./src /app
COPY ./swagger /app/swagger
COPY ./tests /app/tests
COPY ./.pylintrc /app
COPY ./alembic.ini /app
COPY ./alembic /app/alembic

EXPOSE 8000
CMD ["python", "/app/wt/app.py"]
