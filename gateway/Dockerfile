FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_INDEX_URL=https://mirrors.cloud.tencent.com/pypi/simple \
    PIP_DEFAULT_TIMEOUT=30

WORKDIR /app

RUN sed -i \
        -e 's|http://deb.debian.org/debian-security|http://mirrors.cloud.tencent.com/debian-security|' \
        -e 's|http://deb.debian.org/debian|http://mirrors.cloud.tencent.com/debian|' \
        /etc/apt/sources.list.d/debian.sources \
    && apt-get -o Acquire::Retries=3 update \
    && apt-get -o Acquire::Retries=3 install --no-install-recommends -y ca-certificates ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --retries 3 --upgrade pip \
    && pip install --no-cache-dir --retries 3 -r /app/requirements.txt

COPY app /app/app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
