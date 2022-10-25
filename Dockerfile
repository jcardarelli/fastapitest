FROM python:3.11.0-alpine

# Run all commands from this directory
WORKDIR /usr/src

# Copy the requirements file first since it shouldn't change often
COPY requirements.txt ./

# Setup before we can run pip install
RUN \
  apk update --no-cache && \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
  pip install --no-cache-dir -r requirements.txt && \
  apk --purge del .build-deps && \
  rm ./requirements.txt

# Copy all application files to container
COPY app/ /usr/src/app
COPY alembic/ /usr/src/alembic
COPY alembic.ini /usr/src/alembic.ini

# Set env vars and run app with uvicorn
ENV POSTGRES_CONNECTION=.env
ENV PYTHON_PATH=$PWD

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]