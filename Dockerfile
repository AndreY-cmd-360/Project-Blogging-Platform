FROM python:3.12

WORKDIR /app

COPY requirements.txt /app
COPY app.py /app
COPY templates /app/templates
COPY static /app/static

RUN python -m venv venv
RUN /bin/bash -c "source venv/bin/activate"

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]