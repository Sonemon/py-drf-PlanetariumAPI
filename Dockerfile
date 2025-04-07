FROM python:3.11.6-alpine3.18

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

RUN chown -R my_user:my_user /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER my_user

ENTRYPOINT ["/entrypoint.sh"]