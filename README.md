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
- `render.yaml` — Render blueprint for the Python API

## Recommended Deployment

Use this split setup:

1. `cardio-api`: Flask API serving the trained models.
2. `cardio-dashboard`: Next.js frontend deployed on Vercel.

### Backend on Render

1. Push the latest code to GitHub.
2. In Render, create a new Blueprint instance from the repository.
3. Render will detect the `cardio-api` service from `render.yaml`.
4. After the API is live, copy its public URL.
5. Update `CORS_ORIGINS` on Render to match your real Vercel frontend URL.

### Frontend on Vercel

1. Import the same GitHub repository into Vercel.
2. Set the project root directory to `cardio-dashboard`.
3. Add this environment variable in Vercel:
  - `NEXT_PUBLIC_API_URL=https://your-render-api.onrender.com`
4. Deploy the project.
5. After Vercel gives you the live URL, set that URL in the Render `CORS_ORIGINS` variable and redeploy the API.

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
- In Vercel, set the root directory to `cardio-dashboard`.

---

For any issues, check logs on Render or open an issue in the GitHub repo.
