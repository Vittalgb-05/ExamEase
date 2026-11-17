# ExamEase – Live Render Production Deployment & Verification Report

**Project:** ExamEase – Online Examination Management Platform  
**Developer & Maintainer:** Vittal G B  
**Live Production URL:** [**https://examease-i8mj.onrender.com**](https://examease-i8mj.onrender.com)  
**Hosting Provider:** Render (Free Web Service + Managed PostgreSQL Database)  
**Database Engine:** PostgreSQL (`examease-db`)  
**Deployment Method:** Render Blueprint (`render.yaml`) synchronized from GitHub  
**GitHub Repository:** [`https://github.com/Vittalgb-05/ExamEase`](https://github.com/Vittalgb-05/ExamEase)  
**Verification Date:** 17 November 2026  
**Status:** **100% OPERATIONAL & VERIFIED LIVE ON RENDER**  

---

## 1. Production Architecture Overview

```
                    Internet / Candidates / Educators
                                  │
                                  ▼
                     HTTPS (Cloudflare / Render CDN)
                                  │
                                  ▼
               Render Web Service: examease (Python 3.12.7)
              ┌───────────────────────────────────────────┐
              │  Gunicorn WSGI: examsys.wsgi:application  │
              │  WhiteNoise (Compressed & Cached Statics) │
              │  Django 5.1.7 Application Core            │
              └─────────────────────┬─────────────────────┘
                                    │
                                    │ (Encrypted Connection Pool)
                                    ▼
               Render Managed PostgreSQL Database (examease-db)
               (8 Relational Models, Unique Constraints, ACID)
```

---

## 2. Production Configuration Details

| Parameter | Configuration | Status |
|---|---|:---:|
| **Live Web Service URL** | [https://examease-i8mj.onrender.com](https://examease-i8mj.onrender.com) | **ACTIVE** |
| **Service Name** | `examease` | **LIVE** |
| **Service ID** | `srv-dbu90e2fngtc73e42pj0` | **CONFIRMED** |
| **Runtime Environment** | Python 3.12.7 | **VERIFIED** |
| **WSGI Server** | Gunicorn (`gunicorn examsys.wsgi:application`) | **RUNNING** |
| **Database** | Managed PostgreSQL (`examease-db`) paired via `DATABASE_URL` | **CONNECTED** |
| **Static Files Engine** | WhiteNoise (`CompressedStaticFilesStorage`) | **SERVING** |
| **HTTPS Security** | SSL/TLS enforced via `SECURE_PROXY_SSL_HEADER` & `SECURE_SSL_REDIRECT` | **ENFORCED** |
| **Cookie Security** | `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True` | **ENFORCED** |
| **HSTS** | `SECURE_HSTS_SECONDS=31536000`, Include Subdomains, Preload | **ENFORCED** |
| **Allowed Hosts** | `ALLOWED_HOSTS = [..., ".onrender.com"]` | **SECURE** |
| **CSRF Trusted Origins** | `CSRF_TRUSTED_ORIGINS = [..., "https://*.onrender.com"]` | **SECURE** |

---

## 3. Live Browser Verification Log

All workflows below were executed against the **actual live website** at `https://examease-i8mj.onrender.com` using the **Microsoft Edge (Chromium Engine)** driven via the Chrome DevTools Protocol (CDP):

| # | Role / Flow | Action Performed Live on Render | Expected Visual Result | Live Screenshot Evidence | Status |
| :-: | :--- | :--- | :--- | :--- | :-: |
| 1 | **Branding** | Open https://examease-i8mj.onrender.com/ | ExamEase landing hero with Vittal G B developer credit | [`live_01_homepage.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_01_homepage.png) | **PASS** |
| 2 | **Teacher** | Register & Open Dashboard | Teacher registered on Render PostgreSQL and redirected to Dashboard | [`live_02_teacher_dashboard.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_02_teacher_dashboard.png) | **PASS** |
| 3 | **Teacher** | Create Classroom | Classroom saved in PostgreSQL; join code generated | [`live_03_classroom_created.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_03_classroom_created.png) | **PASS** |
| 4 | **Teacher** | Create Examination | Exam created in draft mode and linked to classroom | [`live_04_exam_draft.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_04_exam_draft.png) | **PASS** |
| 5 | **Teacher** | Add 5 MCQ Questions | 5 Questions and 20 choices saved in Render PostgreSQL (10 marks total) | [`live_05_questions_added.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_05_questions_added.png) | **PASS** |
| 6 | **Teacher** | Edit Question | Question text updated and saved on live database | [`live_06_question_edited.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_06_question_edited.png) | **PASS** |
| 7 | **Teacher** | Publish Examination | Exam published; status changed to Open / Live Now | [`live_07_exam_published.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_07_exam_published.png) | **PASS** |
| 8 | **Student** | Register & Open Dashboard | Student registered in separate incognito session | [`live_08_student_dashboard.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_08_student_dashboard.png) | **PASS** |
| 9 | **Student** | Join Classroom via Code | Enrolled into teacher cohort via live code | [`live_09_student_joined_class.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_09_student_joined_class.png) | **PASS** |
| 10 | **Student** | Exam Instructions Screen | Instructions screen showing 15 mins, 5 questions, 60% pass mark | [`live_10_exam_instructions.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_10_exam_instructions.png) | **PASS** |
| 11 | **Student** | Answer Questions & Autosave | AJAX autosaved to PostgreSQL; Question 3 marked with review flag | [`live_11_exam_take_active.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_11_exam_take_active.png) | **PASS** |
| 12 | **Student** | Browser Refresh (Persistence) | All selections and review flag remained 100% intact after reload | [`live_12_persistence_verified.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_12_persistence_verified.png) | **PASS** |
| 13 | **Student** | Submit Exam & View Scorecard | Instant atomic grading: 8/10 Marks (80.0%), Passed status | [`live_13_result_scorecard.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_13_result_scorecard.png) | **PASS** |
| 14 | **Student** | Review Answer Sheet | Question-by-question breakdown with correct keys | [`live_14_result_breakdown.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_14_result_breakdown.png) | **PASS** |
| 15 | **Cross-Role** | Teacher Submissions Leaderboard | Teacher sees candidate score 8/10 (80.0%) and Pass status in table | [`live_15_teacher_results_table.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_15_teacher_results_table.png) | **PASS** |
| 16 | **Cross-Role** | Teacher Reviews Student Paper | Teacher audits student answers with breadcrumb navigation | [`live_16_teacher_review_paper.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_16_teacher_review_paper.png) | **PASS** |
| 17 | **Teacher** | Open Exam Analytics | Chart.js graphs: 100% pass rate, 80% class average, topic mastery | [`live_17_exam_analytics.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_17_exam_analytics.png) | **PASS** |
| 18 | **Teacher** | Profile Management | User profile and personal statistics dashboard | [`live_18_user_profile.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_18_user_profile.png) | **PASS** |
| 19 | **Teacher** | Password Change Screen | Bootstrap-styled password update form | [`live_19_password_change.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_19_password_change.png) | **PASS** |

---

## 4. Key Workflows Verified on Live Production

### 4.1 Educator / Teacher Experience
1. **Account Registration:** Registered teacher account on the live PostgreSQL database with bcrypt/PBKDF2 password hashing.
2. **Classroom Cohort Management:** Created a new classroom (*"Cloud Engineering & Distributed Systems"*) and verified the instant generation of a 6-character alphanumeric join code.
3. **Exam Authoring:** Configured exam duration (15 mins), start/end availability window, 60% passing mark, and restricted enrollment to the new classroom cohort.
4. **Question Bank Authoring:** Created **5 MCQ questions** with customized point allocations (10 total marks), 4 choices each, and designated correct answer keys.
5. **Question Editing:** Edited Question 1 to verify update forms and live database persistence.
6. **Publishing:** Toggled examination status from Draft to **Open / Live Now**.

### 4.2 Candidate / Student Experience
1. **Isolated Session:** Launched an independent incognito session to simulate candidate access.
2. **Account Registration & Class Join:** Registered candidate account and enrolled into the classroom using the teacher's join code.
3. **Examination Briefing:** Reviewed exam guidelines, rules, and question counts before launching.
4. **Active Examination Cockpit:**
   - Real-time countdown timer running on live server authority.
   - Interactive Question Palette with status indicators.
   - Answered questions 1–5; verified real-time AJAX autosaving over HTTPS.
   - Marked Question 3 with the "Flag for Review" bookmark.
5. **Persistence Across Reload:** Performed a full browser refresh (`F5`) on the live exam URL; confirmed that all radio button selections and the review flag **remained 100% intact**.
6. **Submission & Scorecard:** Submitted the exam; instantly received the official scorecard displaying **8 / 10 Marks (80.0%)**, green **Passed** badge, and color-coded answer review breakdown.

### 4.3 Real-Time Cross-Role Synchronization
1. Returned to the Teacher session; the candidate's score immediately appeared on the **Submissions Leaderboard**.
2. Clicked **"Review Answers"** to inspect the student's graded question paper from the educator perspective.
3. Opened **Exam Analytics**; Chart.js rendered live score distributions (100% pass rate, 80% class average) and topic comprehension metrics.
4. Inspected User Profile and Password Change forms.

---

## 5. Visual Evidence Index

All live production screenshots are stored in [`demo-evidence/`](file:///j:/Desktop/online-exam-system/demo-evidence):

1. [`live_01_homepage.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_01_homepage.png) – Live homepage with ExamEase branding and Vittal G B attribution.
2. [`live_02_teacher_dashboard.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_02_teacher_dashboard.png) – Teacher dashboard on Render PostgreSQL.
3. [`live_03_classroom_created.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_03_classroom_created.png) – Classroom created with unique join code.
4. [`live_04_exam_draft.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_04_exam_draft.png) – Exam creation workspace in draft mode.
5. [`live_05_questions_added.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_05_questions_added.png) – 5 MCQ questions added with mark allocation.
6. [`live_06_question_edited.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_06_question_edited.png) – Question edit verified in PostgreSQL.
7. [`live_07_exam_published.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_07_exam_published.png) – Exam published and Open for candidates.
8. [`live_08_student_dashboard.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_08_student_dashboard.png) – Student dashboard in isolated incognito session.
9. [`live_09_student_joined_class.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_09_student_joined_class.png) – Student enrolled in class via join code.
10. [`live_10_exam_instructions.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_10_exam_instructions.png) – Exam instructions briefing screen.
11. [`live_11_exam_take_active.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_11_exam_take_active.png) – Live examination-taking interface with timer and autosave.
12. [`live_12_persistence_verified.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_12_persistence_verified.png) – State persistence confirmed after live page reload.
13. [`live_13_result_scorecard.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_13_result_scorecard.png) – Official scorecard: 8/10 (80.0%), Passed badge.
14. [`live_14_result_breakdown.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_14_result_breakdown.png) – Color-coded question breakdown review.
15. [`live_15_teacher_results_table.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_15_teacher_results_table.png) – Teacher submissions leaderboard.
16. [`live_16_teacher_review_paper.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_16_teacher_review_paper.png) – Teacher inspecting candidate question sheet.
17. [`live_17_exam_analytics.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_17_exam_analytics.png) – Chart.js analytics graphs on live production.
18. [`live_18_user_profile.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_18_user_profile.png) – User profile dashboard and statistics.
19. [`live_19_password_change.png`](file:///j:/Desktop/online-exam-system/demo-evidence/live_19_password_change.png) – Styled password change screen.

---

## 6. Conclusion & Operational Status

ExamEase is **100% operational, secure, and publicly accessible** at [**https://examease-i8mj.onrender.com**](https://examease-i8mj.onrender.com). All administrative, teacher, and student assessment workflows operate seamlessly with zero errors, PostgreSQL persistence, WhiteNoise asset delivery, and responsive SaaS design.
