FROM python:3.12 as base
WORKDIR /app
COPY app.py .
ENV PORT=4000
EXPOSE $PORT
CMD ["python", "app.py"]




FROM base as development

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt



FROM base as production

COPY requirements.txt .
RUN pip install -r requirements.txt
