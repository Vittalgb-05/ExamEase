# ExamEase – Online Examination Management Platform

> **Smart Examinations. Simple Evaluation.**  
> **Customized and enhanced by Vittal G B**

[![Developer: Vittal G B](https://img.shields.io/badge/Developer-Vittal%20G%20B-1e40af.svg?style=flat-square)](https://github.com/Vittalgb-05)
[![Repository](https://img.shields.io/badge/GitHub-Vittalgb--05%2FExamEase-0f172a.svg?style=flat-square&logo=github)](https://github.com/Vittalgb-05/ExamEase)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776ab.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django 5.x](https://img.shields.io/badge/Django-5.x-092e20.svg?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Bootstrap 5.3](https://img.shields.io/badge/Bootstrap-5.3-7952b3.svg?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384.svg?style=flat-square&logo=chartdotjs&logoColor=white)](https://www.chartjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791.svg?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-10b981.svg?style=flat-square)](LICENSE)

---

## Overview

**ExamEase** is an enterprise-grade, full-stack examination management platform built with Django 5 and Bootstrap 5. It is designed for educational institutions, educators, and training programs to streamline the end-to-end examination lifecycle: from timed exam authoring with cohort-based join codes to live candidate telemetry, real-time autosaving, deterministic question shuffling, and instantaneous grading with comprehensive learning analytics.

ExamEase features a modern SaaS visual design, robust server-side deadline enforcement, anti-tamper tab-switching telemetry, and exportable audit reports.

---

## Visual Showcase

The platform has been visually verified across all user roles via Chromium browser automation. Below are genuine evidence captures:

| Homepage & Visual Identity | Teacher Dashboard & Analytics |
|:---:|:---:|
| ![Homepage](demo-evidence/01_homepage.png) | ![Teacher Dashboard](demo-evidence/07_teacher_dashboard.png) |
| *Deep Navy SaaS Landing Page with Feature Showcase* | *Educator Dashboard with Live Metrics & Exam Roster* |

| Live Examination Cockpit | Official Result Scorecard |
|:---:|:---:|
| ![Exam Interface](demo-evidence/15_student_exam_take_initial.png) | ![Result Scorecard](demo-evidence/18_student_result_scorecard.png) |
| *Digital Countdown Timer, Question Palette & Autosave* | *Instant Grading, Passing Badge & Review Breakdown* |

| Classroom & Cohort Management | Exam Analytics Engine |
|:---:|:---:|
| ![Classroom Details](demo-evidence/08_teacher_classroom_created.png) | ![Analytics](demo-evidence/22_teacher_exam_analytics.png) |
| *Unique 6-Character Student Join Codes* | *Interactive Score Distributions & Topic Mastery* |

---

## Key Features & Workflows

### 1. Administrator Experience
- **Model Governance:** Direct administration of users, classrooms, exams, questions, choices, and attempt histories through Django Admin.
- **Role Assignment:** Manage teacher, student, and staff accounts with complete relational integrity.
- **Audit Logging:** Track exam availability windows, student enrollment records, and submission timestamps.

### 2. Educator / Teacher Experience
- **Classroom Cohort Management:** Create classrooms that generate unique 6-character alphanumeric join codes (e.g., `Z8PYFQ`) to isolate exam cohorts.
- **Exam Authoring:** Set duration limits, testing start/end windows, passing percentages, and optional classroom restrictions.
- **Question Bank Builder:** Create multiple-choice questions with customized point values, topic classifications, and 4 choices with one-click correct answer keys.
- **Question Editing & Versioning:** Update questions in draft state; questions lock automatically once candidate attempts begin.
- **Live Leaderboard & Roster:** View submissions with total scores, percentages, elapsed minutes, and tab-switch counts. Filter by pass/fail or search by student name.
- **One-Click CSV Export:** Export sanitized tabular results for institutional archives or spreadsheet analysis.
- **Learning Analytics Engine:** Interactive Chart.js charts categorizing score distributions, question difficulty indices, and weak-topic diagnostics.

### 3. Student Experience
- **Unified Assessment Dashboard:** Real-time categorization of examinations (*Available Now*, *Upcoming*, *Completed*, *Missed*).
- **One-Click Class Enrollment:** Join teacher cohorts directly using join codes.
- **Live Examination Cockpit:**
  - Sticky countdown timer with dynamic color changes as the deadline approaches.
  - Interactive Question Palette with status indicators (*Answered*, *Unanswered*, *Flagged for Review*).
  - Bookmark questions using the "Flag for Review" button.
  - Live progress meter tracking completed questions.
  - Safe submit confirmation modal displaying answered vs. unanswered counts.
- **Real-Time Asynchronous Autosave:** Answers are saved immediately via AJAX with visual sync indicators; zero data loss on network hiccups or accidental page reloads.
- **Instant Result Scorecard:** View grades, pass/fail status, duration taken, and color-coded answer-by-answer review sheets.
- **Printable Result Transcript:** Formal transcript formatted for PDF saving and printing (`@media print`).

### 4. Security & Anti-Tamper Safeguards
- **Server-Side Authority:** Deadlines and question timings are strictly enforced on the server. Client clock adjustments or page reloads cannot grant extra time.
- **Database Constraints:** `UniqueConstraint` guarantees exactly one attempt per student per exam and prevents duplicate answer rows.
- **Tab-Switch Telemetry:** Listens to `visibilitychange` events and logs backgrounding counts when the exam tab loses focus.
- **Deterministic Shuffling:** Questions and options are shuffled pseudo-randomly per attempt seed, maintaining consistent order across browser reloads.
- **CSV Formula Injection Defense:** Strips and quotes formula trigger characters (`=`, `+`, `-`, `@`) upon export.

---

## Tech Stack & Architecture

```
ExamEase Architecture
├── Presentation Layer
│   ├── Bootstrap 5.3.3 & Bootstrap Icons
│   ├── Custom CSS Design System (variables, cards, palettes)
│   ├── Chart.js 4.4 (analytics graphs)
│   └── Vanilla JavaScript (AJAX auto-save, timer, palette)
├── Application Layer (Django 5.1.x)
│   ├── Core App (views, models, forms, urls, utils)
│   ├── Role-Based Access Control (Teacher, Student, Admin)
│   ├── Asynchronous Autosave & Submission Finalizer
│   └── Analytics & CSV Generation Engine
└── Persistence Layer
    ├── SQLite (Local Development)
    └── PostgreSQL / Neon (Production Ready)
```

| Layer | Technologies |
|---|---|
| **Backend** | Python 3.10+, Django 5.x |
| **Frontend** | HTML5, Bootstrap 5.3.3, Bootstrap Icons, Custom CSS3, Vanilla JavaScript |
| **Data Visualization** | Chart.js 4.4 |
| **Database** | SQLite (Local Development), PostgreSQL / Neon (Production) |
| **WSGI / Static Files** | Gunicorn, WhiteNoise |
| **Deployment / CI** | Render, Git |

---

## Project Structure

```
ExamEase/
├── core/                              # Main application package
│   ├── management/
│   │   └── commands/
│   │       └── seed_demo.py           # Demo dataset generator (classes, exams, attempts)
│   ├── static/
│   │   └── core/
│   │       ├── css/
│   │       │   └── style.css          # ExamEase design system & responsive styling
│   │       └── img/
│   │           ├── favicon.svg        # ExamEase branded browser icon
│   │           └── logo.svg           # ExamEase vector logo
│   ├── templates/
│   │   ├── core/                      # Application templates (dashboards, exam taking, results)
│   │   └── registration/              # Authentication templates (login, password change)
│   ├── forms.py                       # Form definitions & validation rules
│   ├── models.py                      # Data models (User, ClassRoom, Exam, Attempt, etc.)
│   ├── tests.py                       # Automated test suite (53 unit/integration tests)
│   ├── urls.py                        # Application route patterns
│   ├── utils.py                       # Analytics algorithms & CSV helpers
│   └── views.py                       # View logic, auto-save & grading handlers
├── examsys/                           # Project configuration
│   ├── settings.py                    # Environment-driven Django settings
│   ├── urls.py                        # Project root URL routing
│   └── wsgi.py                        # WSGI entry point for Gunicorn
├── demo-evidence/                     # High-resolution browser verification screenshots
├── scripts/                           # Browser automation & verification scripts
├── .env.example                       # Example environment variables template
├── .gitignore                         # Git exclusion rules
├── build.sh                           # Build script for production deployment
├── manage.py                          # Django management CLI
├── Procfile                           # Process definition for web hosting
├── render.yaml                        # Render Blueprint configuration
├── requirements.txt                   # Production Python dependencies
├── LICENSE                            # MIT License
└── README.md                          # Project documentation
```

---

## Getting Started

### Prerequisites

- **Python 3.10+** (Python 3.11 or 3.12 recommended)
- **Git**
- **pip** (Python package manager)

---

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Vittalgb-05/ExamEase.git
   cd ExamEase
   ```

2. **Create and activate a virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Populate initial data (Optional):**
   ```bash
   python manage.py seed_demo
   ```

6. **Create an administrator account:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.

---

## Automated Testing

ExamEase includes an automated test suite covering atomic grading, deadline enforcement, autosave logic, role-based authorization, tab-switch tracking, profile management, and dashboard search filters.

Run the test suite:
```bash
python manage.py test
```

Expected output:
```text
Creating test database for alias 'default'...
.....................................................
----------------------------------------------------------------------
Ran 53 tests in 1.85s

OK
Destroying test database for alias 'default'...
```

---

## Production Deployment (Render + PostgreSQL)

ExamEase includes pre-configured deployment files (`render.yaml`, `build.sh`, `Procfile`) for zero-cost cloud deployment:

1. Push your repository to GitHub.
2. In the [Render Dashboard](https://dashboard.render.com), create a new **Web Service** or **Blueprint** connected to your repository.
3. Configure the following environment variables:

| Variable | Description | Recommended Value |
|---|---|---|
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django cryptographic secret | *(Long random string)* |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://USER:PASS@HOST/DB?sslmode=require` |
| `ALLOWED_HOSTS` | Allowed host headers | `your-service.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins for CSRF validation | `https://your-service.onrender.com` |

---

## Attribution & License

This project is a customized, enhanced, and rebranded portfolio adaptation based on the open-source **Online Exam System** originally created by **Md. Asibul Islam** ([asibulislam/online-exam-system](https://github.com/asibulislam/online-exam-system)).

The original codebase is licensed under the **MIT License**, which is fully preserved in the [`LICENSE`](LICENSE) file. All UI redesigns, branding transformations, profile management systems, search enhancements, browser testing infrastructure, and examination experience improvements were developed by **Vittal G B** as part of the ExamEase portfolio project.

```
MIT License
Copyright (c) 2026 Md. Asibul Islam
Customized and Enhanced by Vittal G B, 2026
```
