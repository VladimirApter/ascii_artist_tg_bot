# Используем официальный образ Python 3.11
FROM python:3.11

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Создание необходимых директорий
RUN mkdir -p /path/to/your/directory

# Копирование файла requirements.txt
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir numpy==1.23.0
RUN pip install --no-cache-dir opencv-python==4.5.5.64
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остального кода
COPY . .

# Запуск вашего приложения
CMD ["python", "main.py"]
