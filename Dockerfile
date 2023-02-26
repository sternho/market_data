FROM python:3.9-buster

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

WORKDIR financial

CMD ["python3", "api_statistics.py"]
