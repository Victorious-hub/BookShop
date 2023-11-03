FROM python:3.11

COPY ./BookShop BookShop

WORKDIR /BookShop
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

RUN python3 manage.py migrate

CMD ["python","manage.py","runserver", "0.0.0.0:8000"]