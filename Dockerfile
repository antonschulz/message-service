FROM python:3.12-slim-bookworm

# UV installation
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2) Download & run the uv installer, then remove it
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# 3) Make sure uv’s bin (~/.local/bin) is on PATH
ENV PATH="/root/.local/bin/:$PATH"
#########################

WORKDIR /app

COPY . .

# 8) Expose port 8000 (Uvicorn default)
EXPOSE 8000

RUN uv sync --locked

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
