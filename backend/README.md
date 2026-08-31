# AI-Powered Legal Metrology Packaged Commodity Compliance System (SIH 2026)

An AI-assisted regulatory compliance inspection platform built with **FastAPI**, **PostgreSQL / SQLite**, **SQLAlchemy**, **OpenCV**, **PaddleOCR**, and **ReportLab**. Designed for Legal Metrology officers and inspectors to rapidly inspect packaged commodities, extract mandatory statutory declarations, run versioned metrology rules, detect potential non-compliance, calculate transparent compliance scores, record inspector verification reviews, and generate official compliance reports.

---

## 1. System Architecture & Workflow

```text
Packaging Images Upload
          ↓
OpenCV Image Quality Check (Resolution, Blur, Contrast, Exposure)
          ↓
Non-Destructive Image Preprocessing (CLAHE, Bilateral Filter, Sharpening)
          ↓
OCR Engine (PaddleOCR with Bounding Boxes & Confidence)
          ↓
Text Normalization (Standardizes currency symbols, units, formatting)
          ↓
Declaration Extractor (Regex + Spatial Patterns for MRP, Net Qty, Dates, Mfg, Care)
          ↓
Compliance Rule Engine (Legal Metrology Packaged Commodities Rules 2011)
          ↓
Potential Violation Generator (Explainable findings with evidence bounding boxes)
          ↓
Transparent Compliance Score (AI-assisted preliminary percentage metric)
          ↓
Inspector Verification (Human-in-the-Loop: Confirm / Reject / Edit / Remarks)
          ↓
Official PDF Compliance Report (ReportLab) & Real-time Dashboard
```

> [!NOTE]
> **AI-Assisted Legal Principle**: In accordance with metrology enforcement guidelines, AI findings represent preliminary detections and do NOT automatically impose penalties. All actions undergo authorized inspector review and verification.

---

## 2. Technology Stack

- **Backend**: Python 3.12+, FastAPI, Uvicorn, Pydantic v2, Pydantic Settings
- **ORM & Migrations**: SQLAlchemy 2.0, Alembic
- **Database**: PostgreSQL (Production) / SQLite (Zero-config local development & CI)
- **Security**: JWT Authentication (python-jose), Password Hashing (Argon2 / bcrypt), Role-Based Access Control (`ADMIN`, `INSPECTOR`), Non-repudiable Audit Logging
- **Computer Vision & OCR**: OpenCV (Laplacian variance, CLAHE, Bilateral filtering), PaddleOCR (multilingual character recognition with bounding boxes)
- **Reporting**: ReportLab (official branded multi-page inspection summaries)
- **Testing**: pytest, FastAPI TestClient, httpx
- **Containerization**: Docker, Docker Compose

---

## 3. Project Directory Structure

```text
backend/
├── app/
│   ├── main.py                     # FastAPI application factory & router registration
│   ├── config.py                   # Pydantic Settings configuration
│   ├── api/                        # REST API routers
│   │   ├── auth.py                 # Login, Me, Logout
│   │   ├── users.py                # Admin user management
│   │   ├── products.py             # Product catalog & search
│   │   ├── inspections.py          # Inspection lifecycle & image uploads
│   │   ├── analysis.py             # AI orchestration & Inspector reviews
│   │   ├── reports.py              # PDF report generation & downloads
│   │   ├── rules.py                # Legal Metrology regulatory rules
│   │   └── dashboard.py            # Summary metrics & violation charts
│   ├── models/                     # SQLAlchemy declarative models
│   ├── schemas/                    # Pydantic v2 schemas
│   ├── services/                   # Business logic & domain services
│   ├── ai/                         # OpenCV, OCR, Extractor, Readability, Font Estimation
│   ├── rules/                      # Rule engine & statutory validators
│   ├── database/                   # DB engine, sessionmaker & Alembic migrations
│   ├── middleware/                 # Exception handlers & structured logging
│   └── utils/                      # Security, files, helpers & constants
├── tests/                          # Complete pytest suite (31 tests)
├── uploads/                        # Evidence image storage
├── reports/                        # Generated PDF compliance reports
├── seed.py                         # Bootstrap script (Admin, Inspector, Rules, Demo product)
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 4. Setup & Installation

### Prerequisites
- Python 3.12+
- `pip` package manager
- (Optional) PostgreSQL 15+ or Docker

### Local Installation
1. Clone the repository and navigate to the `backend` directory:
   ```bash
   cd d:/SIH26034/backend
   ```

2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 5. Environment Variables Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Key environment configuration variables:
```ini
APP_NAME=Legal Metrology AI Compliance System
APP_ENV=development
DEBUG=True
API_V1_STR=/api
HOST=0.0.0.0
PORT=8000

# Secret key for signing JWTs
SECRET_KEY=change-this-ultra-secure-secret-key-for-legal-metrology-compliance-2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Database Connection (SQLite local default; or PostgreSQL URI)
DATABASE_URL=sqlite:///./metrology.db
# DATABASE_URL=postgresql://metrology_user:metrology_password@localhost:5432/metrology_db

# CORS Allowed Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173

# Storage Settings
UPLOAD_DIR=uploads
REPORT_DIR=reports
MAX_UPLOAD_SIZE_MB=10

# AI / OCR Configuration
OCR_ENGINE=paddleocr
USE_MOCK_OCR_IF_UNAVAILABLE=True

# Default Seed Credentials
SEED_ADMIN_EMAIL=admin@metrology.gov.in
SEED_ADMIN_PASSWORD=AdminPassword@2026
SEED_INSPECTOR_EMAIL=inspector@metrology.gov.in
SEED_INSPECTOR_PASSWORD=InspectorPassword@2026
```

---

## 6. Database Setup & Seeding

### Initialize Database & Bootstrap Default Records:
Run the seed script:
```bash
python seed.py
```
This automatically:
- Creates all required database tables
- Creates default Admin account (`admin@metrology.gov.in` / `AdminPassword@2026`)
- Creates default Inspector account (`inspector@metrology.gov.in` / `InspectorPassword@2026`)
- Seeds the 6 core statutory prototype rules (LM-001 to LM-006)
- Seeds demo product `ABC Premium Biscuits` and demo inspection `LM-2026-0248`

### Database Migrations with Alembic:
Generate a migration revision:
```bash
alembic revision --autogenerate -m "Add compliance tables"
```
Apply migrations:
```bash
alembic upgrade head
```

---

## 7. Running the Application

### Start Local Development Server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Base URL: `http://localhost:8000/api`
- Interactive Swagger Documentation: `http://localhost:8000/docs`
- ReDoc API Reference: `http://localhost:8000/redoc`

---

## 8. Running Automated Tests

Run the full pytest suite:
```bash
python -m pytest -v
```

Tests cover:
- Health checks & OpenAPI schema validation
- JWT authentication, password hashing, and role authorization
- Product catalog CRUD and search
- Inspection lifecycle, ID generation (`LM-YYYY-XXXX`), and query filters
- Multipart image uploads, OpenCV quality metrics, and size limits
- OCR bounding box extraction and text normalization
- Deterministic declaration extractors (MRP, Quantity, Date, Mfg, Care)
- Compliance rule engine, scoring algorithms, and explainable violations
- Inspector review workflows (Confirm / Reject / Edit) and visual evidence retrieval
- ReportLab PDF generation and download
- Dashboard summary analytics and violation breakdown

---

## 9. Docker Deployment

To spin up the PostgreSQL database and backend service together:
```bash
docker-compose up --build
```
This starts:
- `metrology_postgres` on port `5432` with healthchecks
- `metrology_backend` on port `8000` with volume persistence for `uploads/` and `reports/`

---

## 10. Core API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/health` | Service health status | No |
| `POST` | `/api/auth/login` | Login and obtain JWT token | No |
| `GET` | `/api/auth/me` | Current user profile | Yes |
| `POST` | `/api/auth/logout` | Logout & audit log | Yes |
| `GET` | `/api/users` | List users | Admin Only |
| `POST` | `/api/users` | Create user | Admin Only |
| `POST` | `/api/products` | Create product specification | Yes |
| `GET` | `/api/products` | Paginated product list | Yes |
| `GET` | `/api/products/search` | Search product catalog | Yes |
| `POST` | `/api/inspections` | Create new inspection | Yes |
| `GET` | `/api/inspections` | List inspections (with filters) | Yes |
| `GET` | `/api/inspections/{id}` | Full inspection details | Yes |
| `PUT` | `/api/inspections/{id}` | Update inspection | Yes |
| `POST` | `/api/inspections/{id}/images` | Upload packaging image & evaluate quality | Yes |
| `GET` | `/api/inspections/{id}/images` | List packaging images | Yes |
| `POST` | `/api/inspections/{id}/analyze` | Trigger full AI analysis pipeline | Yes |
| `POST` | `/api/violations/{id}/review` | Inspector verification (Confirm / Reject) | Yes |
| `GET` | `/api/violations/{id}/evidence` | Get visual evidence & bounding box | Yes |
| `POST` | `/api/inspections/{id}/report` | Generate official PDF report | Yes |
| `GET` | `/api/reports/{id}/download` | Download inspection PDF | Yes |
| `GET` | `/api/rules` | List regulatory metrology rules | Yes |
| `GET` | `/api/dashboard/summary` | Aggregate dashboard KPI metrics | Yes |
| `GET` | `/api/dashboard/violations` | Violations breakdown by category | Yes |
| `GET` | `/api/dashboard/recent-inspections` | Recent inspection stream | Yes |

---

## 11. Frontend Integration Guide

The backend exposes a standardized REST contract designed for seamless React / TypeScript frontend integration:

1. **Authentication**:
   - Send `POST /api/auth/login` with email and password.
   - Store `access_token` in memory / secure storage.
   - Attach header `Authorization: Bearer <access_token>` to all subsequent requests.

2. **Standard Error Schema**:
   All errors follow predictable format:
   ```json
   {
     "error": {
       "code": "IMAGE_TOO_LARGE",
       "message": "Maximum image size is 10 MB."
     }
   }
   ```

3. **Bounding Box Visualization**:
   Detected declarations and OCR tokens include standard bounding boxes:
   ```json
   {
     "x": 120.0,
     "y": 240.0,
     "width": 200.0,
     "height": 50.0
   }
   ```
   Frontend components can directly overlay highlight rectangles on packaging images using these coordinates.

---

## 12. Primary Demonstration Walkthrough Flow

1. **Login**:
   - Sign in as `inspector@metrology.gov.in` (`InspectorPassword@2026`).
2. **Create Inspection**:
   - Create inspection for `ABC Premium Biscuits` by `ABC Foods Pvt. Ltd.`.
   - Inspection ID generated: `LM-2026-0248`.
3. **Upload Packaging Images**:
   - Upload front and back packaging images.
   - OpenCV returns quality assessment score (e.g. `91.0`, blur: sharp).
4. **Trigger AI Compliance Analysis**:
   - Initiates `/api/inspections/{id}/analyze`.
   - PaddleOCR detects text tokens with bounding boxes.
   - Declarations extracted: MRP (`₹199`), Net Qty (`500 g`), MFD (`06/2026`), Manufacturer (`ABC Foods Pvt. Ltd.`), Product Name (`ABC Premium Biscuits`), Consumer Care (`Not Detected`).
   - Compliance score calculated: `83.3%` with status `REQUIRES_REVIEW`.
   - Potential violation generated for `LM-006: Consumer Care Details`.
5. **Inspector Verification**:
   - Inspector inspects evidence bounding box at `/api/violations/{id}/evidence`.
   - Submits confirmation review at `/api/violations/{id}/review` with decision `CONFIRM`.
6. **Generate Compliance Report**:
   - Calls `/api/inspections/{id}/report`.
   - ReportLab produces official inspection report `REP-2026-XXXX.pdf`.
7. **Dashboard Update**:
   - Real-time summary and violation charts at `/api/dashboard/summary` reflect latest inspection findings.

---

## 13. Known Limitations & Future Scope

### Current Prototype Limitations (MVP Scope)
- Font-size estimation relies on relative bounding box pixel ratios and is labeled as an AI-assisted estimate pending calibrated camera scale reference.
- Multilingual OCR is optimized for English packaging declarations, with Hindi supported via PaddleOCR multilingual models.

### Future Scope
- Mobile offline synchronization for remote field inspections with local SQLite cache.
- Computer vision packaging curvature and perspective rectification for curved cylindrical containers.
- E-commerce packaged commodity catalog crawlers and automated marketplace scanning.
- Integration with National Consumer Helpline and State Metrology enforcement portals.
