FROM python:3.10-slim

WORKDIR /app

ADD . /app

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 5000

CMD ["python", "app.py"]