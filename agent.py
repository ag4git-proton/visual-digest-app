import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
from transformers import pipeline
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, filename="/app/output/agent.log")

# Configuration
category = os.getenv("CATEGORY", "Games")
output_dir = "/app/output"

# Initialize Hugging Face LLM
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
except Exception as e:
    logging.error(f"LLM init failed: {e}")
    summarizer = None

# Scrape app store with Selenium
def scrape_top_apps():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(f"--user-data-dir=/tmp/chrome-data-{category}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        url = "https://play.google.com/store/apps/top"
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        apps = soup.find_all("div", class_="VfPpkd-EScbFb-JIbuQc")[:5]
        driver.quit()
        return [app.text.strip() for app in apps if app.text.strip()] or ["No data"]
    except Exception as e:
        logging.error(f"Scraping failed: {e}")
        return ["No data"]

# Generate visual
def create_visual(data, category):
    try:
        plt.figure(figsize=(8, 4))
        plt.bar(range(len(data)), [1] * len(data))
        plt.xticks(range(len(data)), data, rotation=45)
        plt.title(f"Top Apps in {category}")
        output_path = f"{output_dir}/{category}_chart.png"
        plt.savefig(output_path)
        plt.close()
        return output_path
    except Exception as e:
        logging.error(f"Visual creation failed: {e}")
        return f"{output_dir}/error.png"

# Summarize with LLM
def llm_summarize(text):
    try:
        if summarizer:
            summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
            return summary[0]["summary_text"]
        return f"Summary for {category}: {text[:100]}..."
    except Exception as e:
        logging.error(f"Summarization failed: {e}")
        return f"Error summarizing {category}"

# Main agent logic
def run_agent():
    try:
        apps = scrape_top_apps()
        text = " ".join(apps)
        summary = llm_summarize(text)
        visual = create_visual(apps, category)
        
        # Save output
        output = {"category": category, "summary": summary, "visual": visual}
        with open(f"{output_dir}/{category}_output.json", "w") as f:
            json.dump(output, f)
        logging.info(f"Agent {category} completed successfully")
    except Exception as e:
        logging.error(f"Agent {category} failed: {e}")

if __name__ == "__main__":
    run_agent()
