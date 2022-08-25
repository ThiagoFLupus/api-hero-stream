FROM python:3

RUN apt-get update -y
ADD . /var/www/
WORKDIR /var/www/
RUN pip install -r requirements.txt
# variável de ambiente, para permitir os prints internos no log do container
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "server.py"]