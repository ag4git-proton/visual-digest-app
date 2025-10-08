# Visual Digest App

Weekly magazine of top app downloads by category (Games, Productivity, Social, Health, Education), built as a DAO with AI agents.

## Setup
1. Install Docker and Docker Compose.
2. Deploy `VisualDigestDAO.sol` on Sepolia testnet via Remix IDE.
3. Update `compile_magazine.py` with Infura key and contract address/ABI.
4. Run locally: `docker-compose up -d`.
5. Check outputs in `./output` (logs, JSON, magazine PDF/HTML).

## Usage
- Agents scrape Google Play, summarize with Hugging Face LLM, create charts.
- Team votes on outputs via DAO (use Metamask with Sepolia).
- Weekly magazine compiled every Monday (cron in Docker).

## Deployment
- Local: Run `test.sh` to build, run, and test.
- Optional: Deploy to Render free tier (`render.yaml` provided).

## Files
- `docker-compose.yml`: Runs agents, compiler, cron.
- `agent.py`: Scrapes, summarizes, creates visuals per category.
- `compile_magazine.py`: Compiles approved outputs into magazine.
- `VisualDigestDAO.sol`: DAO for voting.
- `test.sh`: Local test script.