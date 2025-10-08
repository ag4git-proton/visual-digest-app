# Visual Digest App - Technical README

## Overview
DAO-based app with AI agents to scrape top apps (Games, Productivity, Social, Health, Education), summarize with LLM, and compile a weekly magazine.

## Setup
1. Install Docker, Docker Compose.
2. Deploy `VisualDigestDAO.sol` on Sepolia testnet (Remix IDE).
3. Update `compile_magazine.py` with Infura key, contract address, ABI.
4. Run: `docker-compose up -d`.
5. Outputs in `./output` (logs, JSON, magazine PDF/HTML).

## Key Files
- `docker-compose.yml`: Runs agents, compiler, cron.
- `agent.py`: Scrapes Google Play, summarizes, creates charts.
- `compile_magazine.py`: Builds magazine from approved outputs.
- `VisualDigestDAO.sol`: DAO for voting.
- `test.sh`: Local test script.

## Notes
- Uses free tools: Selenium, Hugging Face (BART), WeasyPrint.
- Cron runs weekly (Mondays).
- Optional: Deploy to Render free tier (`render.yaml`).