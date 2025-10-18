FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y chromium chromium-driver
RUN pip install beautifulsoup4 requests selenium autogen matplotlib weasyprint transformers tourch

#fix chrome driver permissions
RUN chmod +x /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod 4755 /usr/bin/chromedriver

COPY agent.py compile_magazine.py ./

CMD ["python", "agent.py"]
