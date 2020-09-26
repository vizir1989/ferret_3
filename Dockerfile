FROM python
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=ferret
RUN flask init-db
CMD flask run --host 0.0.0.0