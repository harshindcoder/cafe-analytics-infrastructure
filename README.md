# ☕ Café Analytics Platform

**An End-to-End Data Engineering & Analytics System (Docker · PostgreSQL · Python · Apache Superset)**

---

## 📌 Overview

This project implements a **production-style analytics platform** for a fictional **Seoul-based café** selling **coffees and cakes**.

The system simulates transactional café orders, ingests them into a relational database with proper constraints, and exposes governed analytics through **Apache Superset** — all running in a fully containerized environment.

> 🎯 **Objective**
> Build, debug, and operate a realistic data engineering pipeline rather than a demo-only dashboard.

---

## 🏗️ System Architecture

```
┌──────────────────┐
│  Python Ingestion│
│  (Batch Job)     │
└───────┬──────────┘
        ↓
┌──────────────────┐
│  PostgreSQL 15   │
│  Orders & Items  │
└───────┬──────────┘
        ↓
┌──────────────────┐
│ Apache Superset  │
│ BI & Dashboards  │
└──────────────────┘

(All services orchestrated via Docker Compose)
```

---

## 🧠 Data Modeling

### Schema Design Philosophy

* Designed around **real POS systems**
* Supports **multi-item orders**
* Optimized for **analytics & aggregations**
* Enforces **data integrity via constraints**

### Tables

#### `items` (Dimension)

```sql
item_no       INT PRIMARY KEY
item_name     TEXT
category      coffee | cake
description   TEXT
price         NUMERIC(8,2)
```

#### `order_items` (Fact)

```sql
(order_no, item_no)  PRIMARY KEY
quantity             INT
order_ts             TIMESTAMP
```

**Grain**: One row per item per order
This enables accurate revenue, quantity, and time-series analysis.

---

## 🔄 Data Ingestion

The ingestion service:

* Inserts café menu items (idempotent)
* Generates realistic order volumes
* Creates multi-item orders
* Spreads orders across operating hours
* Enforces foreign-key relationships

📁 Location:

```
ingestion/ingest.py
```

The ingestion container runs as a **batch job** and exits after completion.

---

## 📊 Analytics & BI (Apache Superset)

Superset is used as the analytics layer, enabling:

* Revenue analysis by time
* Coffee vs cake sales comparison
* Average order size
* Item-level performance
* Peak café hours

### Database Connection

```
postgresql+psycopg2://cafe_user:cafe_pass@postgres:5432/cafe
```

---

## 🔐 Role-Based Access Control (RBAC)

This project intentionally implements **governed analytics**, not open access.

### Roles Used

| Role    | Capabilities                                 |
| ------- | -------------------------------------------- |
| Admin   | Full access (DB, SQL Lab, users, dashboards) |
| Analyst | Query datasets, build charts & dashboards    |
| Viewer  | Read-only dashboard access                   |

### Why This Matters

* Mirrors enterprise BI environments
* Prevents unrestricted SQL access
* Enables controlled data exposure
* Validates multi-user workflows

---

## 🌍 Multi-Device Validation

The platform was accessed and validated from:

* Multiple laptops
* Browser-only sessions
* Different user roles

This confirmed:

* Stateless UI behavior
* Dockerized service reliability
* Role-specific access enforcement
* Production-like usability

---

## 🐳 Dockerized Infrastructure

### Services

| Service     | Purpose               |
| ----------- | --------------------- |
| `postgres`  | Relational data store |
| `ingestion` | Batch data generator  |
| `superset`  | BI & analytics UI     |

All services communicate via a private Docker network.

---

## 🧩 Superset Driver Configuration (Important)

Superset requires database drivers to be installed **inside its runtime environment**.

A custom Dockerfile is used to safely enable PostgreSQL support.

📁 `superset/Dockerfile`

```dockerfile
FROM apache/superset:latest

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    psycopg2-binary \
    sqlalchemy \
    sqlalchemy-utils \
    redis \
    pymysql \
    clickhouse-connect

USER superset
```

This resolves common `PostgresEngineSpec` errors in Superset.

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd seoul-cafe-analytics
```

---

### 2️⃣ Build & Start Services

```bash
docker compose down -v
docker compose build --no-cache
docker compose up
```

---

### 3️⃣ Access Superset

* URL: **[http://localhost:8088](http://localhost:8088)**
* Username: `admin`
* Password: `admin`

---

### 4️⃣ Verify Postgres Driver

```bash
docker exec -it cafe_superset superset shell
```

```python
import psycopg2
psycopg2.__version__
```

---

## 🛠️ Key Engineering Challenges Solved

* Superset driver loading issues
* Docker build vs runtime Python environments
* Foreign-key constraint handling
* Duplicate primary key errors
* Secure, role-based analytics access

## 🧑‍💻 Author
**Harsh Indoria**
