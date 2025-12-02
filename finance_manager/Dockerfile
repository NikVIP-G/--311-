FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    python3-tk \
    tk-dev \
    tcl-dev \
    tk \
    tcl \
    xvfb \
    xauth \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -c "import tkinter; print('✅ Tkinter установлен')"

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

CMD ["xvfb-run", "--server-args='-screen 0 1024x768x24'", "python", "main.py"]