FROM python:3.9
# Устанавливает переменную окружения, которая гарантирует,
# что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1
# Создаём рабочаю директорию
WORKDIR /app
# Устанавливаем зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# Копируем приложение
COPY . .
# Прослушиваем порт
EXPOSE 8000
# Команда для старта сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]