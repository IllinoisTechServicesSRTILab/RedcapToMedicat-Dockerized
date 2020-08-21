FROM python:3

RUN mkdir -p /scripts
WORKDIR /scripts

COPY . .

RUN pip install -r requirements.txt
ENTRYPOINT ["python","redcap_batch_handler.py"]