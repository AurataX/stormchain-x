FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.lock .
RUN pip install --no-cache-dir -r requirements.lock \
    && useradd --create-home --uid 10001 stormchain
COPY --chown=stormchain:stormchain app ./app
COPY --chown=stormchain:stormchain data ./data
COPY --chown=stormchain:stormchain database ./database
USER stormchain
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
