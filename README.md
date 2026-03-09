# Cardiovascular Disease Prediction API & Dashboard

## Project Structure

- `api_server.py` — Flask API for ML predictions
- `cardioUiDashboard.py` — Streamlit dashboard
- `artifacts/` — Trained models and preprocessor
- `cardio-dashboard/` — Next.js frontend dashboard
- `scripts/` — Model retraining and diagnosis scripts
- `streamlit_requirements.txt` — Python dependencies
- `Dockerfile` — Container setup for the Python API
- `Procfile` — Gunicorn entrypoint for the Python API
- `render.yaml` — Render blueprint for both API and Next.js dashboard

## Render Deployment

This repository is now structured as a two-service Render deployment:

1. `cardio-api`: Flask API serving the trained models.
2. `cardio-dashboard`: Next.js frontend that calls the API with `NEXT_PUBLIC_API_URL`.

### One-click setup with `render.yaml`

1. Push the latest code to GitHub.
2. In Render, create a new Blueprint instance from the repository.
3. Render will detect both services from `render.yaml`.
4. After the services are created, confirm the actual frontend URL and backend URL.
5. If Render assigns different service hostnames than the defaults in `render.yaml`, update these variables:
  - `CORS_ORIGINS` on `cardio-api`
  - `NEXT_PUBLIC_API_URL` on `cardio-dashboard`

## Local Development

- Install Python dependencies:
  ```bash
  pip install -r streamlit_requirements.txt
  ```
- Run API server:
  ```bash
  python api_server.py
  ```
- Run Streamlit dashboard:
  ```bash
  streamlit run cardioUiDashboard.py
  ```

- Run Next.js dashboard:
  ```bash
  cd cardio-dashboard
  cp .env.example .env.local
  npm install
  npm run dev
  ```

## Frontend (Next.js)

- The dashboard reads its backend base URL from `NEXT_PUBLIC_API_URL`.
- Set `NEXT_PUBLIC_API_URL=http://localhost:5000` for local development.
- Set `NEXT_PUBLIC_API_URL=https://your-api-service.onrender.com` in production.

---

For any issues, check logs on Render or open an issue in the GitHub repo.
