FROM python:3.8-slim

RUN apt-get update && apt-get install -y build-essential

RUN pip3 install cython numpy==1.23.3 pystan==2.19.1.1

WORKDIR /
EXPOSE 8501

COPY / ./
RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "src/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]