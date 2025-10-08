FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y chromium-driver
RUN pip install beautifulsoup4 requests selenium autogen matplotlib weasyprint transformers

COPY agent.py compile_magazine.py ./

CMD ["python", "agent.py"]