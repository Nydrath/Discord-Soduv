FROM python:3.9 as builder

# https://pythonspeed.com/articles/multi-stage-docker-python/

RUN git clone https://github.com/Nydrath/Saphrael --depth 1
WORKDIR /Saphrael
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install -r requirements.txt
COPY "keys.json" .

FROM python:3.9 as saphrael
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /Saphrael .
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT [ "python3", "saphrael.py" ]