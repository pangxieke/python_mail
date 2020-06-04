FROM python:3.7.5
WORKDIR /usr/src/app
COPY src/ /usr/src/app/
RUN pip install redis

CMD ["python", "mail.py"]
