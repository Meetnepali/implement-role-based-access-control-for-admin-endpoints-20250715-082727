# Dockerfile for FastAPI app
FROM python:3.10-slim
WORKDIR /app
COPY app /app/app
COPY install.sh /app/install.sh
COPY run.sh /app/run.sh
RUN chmod +x /app/install.sh /app/run.sh
RUN /app/install.sh
EXPOSE 8000
CMD ["bash", "/app/run.sh"]
