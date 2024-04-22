FROM amazon/aws-cli:latest AS awscli


FROM python:3.9


WORKDIR /file


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 7000

CMD ["python3", "-m","main", "run", "--host=0.0.0.0", "--port=7000"]