# MeowCount
<img width="3000" height="3000" alt="meowcount" src="https://github.com/user-attachments/assets/47bd4fed-e8cd-4247-9238-b05644376f5b" />

MeowCount is a minimal Flask web app that shows how many Discord servers (guilds) you’re in. It uses Discord OAuth2 to request the `identify` and `guilds` scopes, counts your servers from the Discord API, and displays the result. No database is required.

## Oneclick Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2F0xtbug%2Fmeowcount)

## Installation
### Local
1. Prerequisites: Python 3.11+.
2. Create `.env` with your Discord app credentials:
   ```bash
   CLIENT_ID=your_discord_client_id
   CLIENT_SECRET=your_discord_client_secret
   REDIRECT_URI=http://localhost:3000
   SECRET_KEY=replace_with_a_random_secret
   PORT=3000
   APP_MODE=dev # change to prod if production
   ```
3. Install and run:
   ```bash
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```
### Docker
- With Compose (recommended):
  ```bash
  docker compose up -d meowcount
  docker compose logs -f meowcount
  ```
- Manual:
  ```bash
  docker build -t meowcount .
  docker run -d -p 3000:3000 --env-file .env --name meowcount meowcount
  ```
> App at http://localhost:3000

## Docker: Development
- Development service (`meowcount-dev`, auto-reload, bind mount):
  ```bash
  docker compose up meowcount-dev
  ```
> App at http://localhost:3001

## Environment Notes
- `REDIRECT_URI` must match your Discord application redirect (e.g., `http://localhost:3000/auth` base is set via app logic).
- In production, set a strong `SECRET_KEY` and use HTTPS for the redirect URL.
