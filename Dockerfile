FROM python:3.9

ARG source
ARG port
ARG apiKey
ARG context_id
ARG user_id

ENV source=$source
ENV port=$port
ENV apiKey=$apiKey
ENV context_id=$context_id
ENV user_id=$user_id

ADD zapu.py .

RUN mkdir /results

RUN pip install python-owasp-zap-v2.4

ENTRYPOINT ["python", "./zapu.py"]
