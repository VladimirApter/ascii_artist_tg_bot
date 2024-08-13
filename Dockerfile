FROM python:3.11

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Создание необходимых директорий
RUN mkdir -p /app/ascii_artist/frames \
    && mkdir -p /app/ascii_artist/images \
    && mkdir -p /app/ascii_artist/result_frames \
    && mkdir -p /app/ascii_artist/videos

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt .

# Установка numpy и opencv-python с использованием предварительно собранных бинарных пакетов
RUN pip install --no-cache-dir numpy==1.23.0 opencv-python==4.5.5.64

# Установка остальных зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта
COPY . .

# Запуск приложения
CMD ["python", "main.py"]
