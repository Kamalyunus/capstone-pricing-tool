FROM python:3.9-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /
EXPOSE 8501

COPY / ./
RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "src/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]