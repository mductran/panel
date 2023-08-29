FROM python:3.11

ENV PYTHONBUFFERED 1

WORKDIR ~/panel

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]