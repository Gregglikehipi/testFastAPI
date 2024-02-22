FROM python:3.11.4

WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code"

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY app /code/app

CMD [ "python", "app/main.py"]