# Используем официальный образ Python 3.11
FROM python:3.11

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Проверка и настройка прав доступа к директории .cache/pip
RUN mkdir -p /root/.cache/pip && chown -R root:root /root/.cache/pip

# Копирование файла requirements.txt
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остального кода
COPY . .

# Запуск вашего приложения
CMD ["python", "main.py"]
