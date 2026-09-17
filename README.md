# Smart Campus Resource & Decision Support Platform — Backend

## What this is

A Flask backend that unifies three subject problem statements into one system:

- **Operating Systems** — JWT auth, role-based access control, priority scheduling for booking requests, thread-safe
  locking
- **HPC** — real parallelism (ThreadPoolExecutor) for resource search, conflict detection, utilization analytics
  (map-reduce), and ML batch inference
- **Machine Learning** — a regression model for demand forecasting and a PCA+KMeans model for resource clustering

## Tech stack

- Python 3.14, Flask
- Supabase (Postgres), pooled connection (port 6543)
- scikit-learn, pandas, numpy
- Deployed on Render

## Running locally

1. Clone the repo and create a virtual environment:

python -m venv .venv
.venv\Scripts\activate

2. Install dependencies:

3. Copy `.env.example` to `.env` and fill in:
    - `DATABASE_URL` — your Supabase pooled connection string
    - `JWT_SECRET_KEY` — any random secret string (generate with
      `python -c "import secrets; print(secrets.token_hex(32))"`)
4. Run the SQL in `sql/schema.sql` in your Supabase SQL Editor to create the tables.
5. Start the server:
6. Test with `http://localhost:5000/`

## Live deployment

Backend is live at: `https://smart-campus-backend-zj1o.onrender.com`

## Where each concept is implemented

| Concept                           | File                                                 | Description                                                                                   |
|-----------------------------------|------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| JWT auth + RBAC                   | `utils/auth_utils.py`                                | Token generation/verification, `token_required` and `role_required` decorators                |
| Priority Scheduling (OS)          | `services/scheduling.py`                             | Faculty/admin requests processed before student requests via a priority heap; FCFS tiebreaker |
| Thread-safe locking (OS)          | `services/scheduling.py`, `routes/booking_routes.py` | Per-resource locks prevent double-booking under concurrent requests                           |
| Parallel resource search (HPC)    | `services/parallel_search.py`                        | ThreadPoolExecutor checks resource availability concurrently                                  |
| Parallel conflict detection (HPC) | `services/conflict_detection.py`                     | Concurrent conflict checks across resources                                                   |
| Map-reduce analytics (HPC)        | `services/analytics_engine.py`                       | Booking data split into chunks, aggregated in parallel, merged                                |
| Parallel ML batch inference (HPC) | `services/ml_engine.py` (`predict_demand_batch`)     | Multiple resource predictions run concurrently                                                |
| Demand forecasting (ML)           | `services/ml_engine.py`                              | Linear regression trained on synthetic data (documented as synthetic)                         |
| Resource clustering (ML)          | `services/ml_engine.py`                              | PCA + KMeans on real booking-derived features                                                 |

## API endpoints

- `POST /auth/register`, `POST /auth/login`
- `GET /resources`, `POST /resources`
- `POST /bookings`, `GET /bookings`, `PATCH /bookings/{id}`
- `GET /analytics/utilization` (admin/faculty only)
- `GET /ml/demand-forecast`, `POST /ml/demand-forecast/retrain`, `POST /ml/demand-forecast/batch`
- `GET /ml/clusters`

## Notes / known simplifications

- Demand forecasting is trained on synthetic data since real historical booking data doesn't exist yet for this demo.
- Cluster model retrains on every `/ml/clusters` call rather than caching — acceptable for a small demo dataset.
- Clustering requires at least 3 resources in the database to run.