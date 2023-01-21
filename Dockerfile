FROM python:3.9-slim

WORKDIR /
EXPOSE 8501

COPY / ./
RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "src/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]