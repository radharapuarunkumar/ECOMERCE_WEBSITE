# NovaCart E-Commerce — Full Stack

NovaCart is a full-stack e-commerce learning project with a polished Next.js storefront, FastAPI backend, PostgreSQL on Neon, JWT customer authentication, role-protected admin dashboard, product inventory, and order management. Its deployment pattern mirrors PDF-to-eCourse: Next.js on Vercel, FastAPI on Render, PostgreSQL on Neon.

## Stack
- Frontend: Next.js 14, React, TypeScript, responsive CSS
- Backend: FastAPI (Python)
- Database: PostgreSQL on Neon
- ORM/migrations: SQLAlchemy 2 + Alembic
- Authentication: hashed passwords + JWT bearer tokens
- Hosting: Vercel frontend, Render backend, Neon database

## Features
- Responsive shopping home page with search, category filters, product cards and cart
- Customer registration/login; `/auth/me` profile endpoint
- JWT-protected checkout and customer-only order history
- Server-calculated totals using trusted product prices; stock checked and decremented transactionally
- Admin dashboard with product create/edit/soft-delete, order listing, status updates, summary cards
- PostgreSQL schema for users, products, orders and order items
- API health endpoint and interactive Swagger docs
- Demo product seed data and initial admin account from environment variables

> This is a portfolio/college project starter, not a fully audited marketplace. It does not integrate a payment gateway, shipment provider, tax engine, email/SMS notifications, returns, coupons, product reviews, image uploads, or production-grade observability. Do not collect real payments until those systems and a security review are in place.

## Folder structure
```text
NovaCart_Ecommerce_FullStack/
├── frontend/                 # Deploy this folder to Vercel
│   ├── app/                   # Home, login, register, cart, orders, admin
│   ├── lib/api.ts
│   ├── package.json
│   └── .env.example
└── backend/                  # Deploy this folder to Render
    ├── app/                   # FastAPI routes, SQLAlchemy models, auth
    ├── alembic/               # Database migration
    ├── requirements.txt
    └── .env.example
```

## 1. Neon PostgreSQL
1. Create a project/database in the [Neon Console](https://console.neon.tech/).
2. Copy the connection string from **Connect**. Keep it secret.
3. For SQLAlchemy/psycopg use a URL like `postgresql+psycopg://USER:PASSWORD@HOST/DBNAME?sslmode=require`. If Neon gives you `postgresql://...`, the backend normalizes it automatically.

## 2. Backend local setup
Requires Python 3.11+.
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Edit `.env` with your real `DATABASE_URL`, a long random `JWT_SECRET_KEY`, your frontend URL, and a strong private `ADMIN_PASSWORD`. Never commit `.env`.

Run the initial migration, then start the API:
```bash
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```
The app also calls `create_all` at startup to simplify the college-project setup; Alembic remains available for controlled schema evolution. API docs: `http://localhost:8000/docs`; health: `http://localhost:8000/api/health`.

### Admin account
On first startup the backend creates the admin user using `ADMIN_EMAIL` and `ADMIN_PASSWORD`. Sign in at `/login`, then open `/admin`. Configure a strong unique password before deploying. If an account with that email already exists, startup does not reset its password or role.

## 3. Frontend local setup
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```
Set `NEXT_PUBLIC_API_URL=http://localhost:8000/api` in `frontend/.env.local`. Open `http://localhost:3000`.

## 4. Deploy backend to Render
1. Push the repository to GitHub.
2. In Render, create a Python Web Service and set **Root Directory** to `backend`.
3. Build command: `pip install -r requirements.txt`.
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Set these environment variables in Render:
   - `DATABASE_URL` — Neon connection string
   - `JWT_SECRET_KEY` — long random secret
   - `JWT_EXPIRE_MINUTES` — `1440`
   - `FRONTEND_URL` — exact deployed Vercel origin, e.g. `https://your-site.vercel.app`
   - `ADMIN_EMAIL` — chosen admin email
   - `ADMIN_PASSWORD` — strong private password
   - `SEED_DEMO_PRODUCTS` — `true` (optional)
6. Deploy, then verify `https://YOUR-API.onrender.com/api/health` reports database connected.

## 5. Deploy frontend to Vercel
1. Import the GitHub repository in Vercel.
2. Set **Root Directory** to `frontend`; framework should detect Next.js.
3. Add environment variable `NEXT_PUBLIC_API_URL=https://YOUR-API.onrender.com/api` (no trailing slash).
4. Deploy. If the Vercel domain changes, update Render's `FRONTEND_URL` and redeploy the backend.

## Main API endpoints
- `POST /api/auth/register` — create customer account
- `POST /api/auth/login` — issue JWT
- `GET /api/auth/me` — current authenticated user
- `GET /api/products?search=&category=&limit=100` — browse products
- `GET /api/products/{id}` — product details
- `POST /api/orders` — authenticated checkout; body has `customer_name`, `customer_phone`, `customer_address`, and `items: [{product_id, quantity}]`
- `GET /api/orders/me` — current user's orders
- `POST /api/admin/products` — admin product create
- `PUT /api/admin/products/{id}` — admin product update
- `DELETE /api/admin/products/{id}` — admin soft-delete
- `GET /api/admin/orders` — admin order list
- `PATCH /api/admin/orders/{id}` — admin order status update

## Safety notes
- Passwords are hashed; they are never stored in plain text.
- Admin endpoints check the authenticated user's role on the server. Hiding the admin page alone is not authorization.
- The browser cart is only a convenience; product prices and stock are re-read from PostgreSQL during checkout.
- JWTs are kept in localStorage in this starter for simplicity. For a production storefront, prefer secure HttpOnly cookies, CSRF protection, rate limiting, email verification/password reset, audit logging, and a security review.
- The demo checkout creates orders but does not charge money. Add a payment gateway before taking payments.
