FROM python:3-onbuild

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
WORKDIR /app/Flask-CAS
RUN python setup.py install
WORKDIR /app

CMD [ "python", "main.py" ]