FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

#ENV AWS_PROFILE=default

CMD ["python", "route53.py"]
