FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /django/complete_the_quote
COPY . /django/complete_the_quote
RUN pip install -r requirements.txt