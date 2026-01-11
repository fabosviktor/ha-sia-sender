FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir flask pysiaalarm

COPY sia_server.py /app/sia_server.py
COPY run.sh /app/run.sh

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
