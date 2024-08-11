# Используем официальный образ Python 3.11
FROM python:3.11

# Создание рабочей директории
WORKDIR /app

# Копирование файла requirements.txt
COPY requirements.txt .

# Установка конкретных версий NumPy и OpenCV
RUN pip install --no-cache-dir numpy==1.23.0
RUN pip install --no-cache-dir opencv-python==4.5.5.64

# Установка остальных зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остального кода
COPY . .

# Запуск вашего приложения
CMD ["python", "main.py"]
