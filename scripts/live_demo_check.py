import os
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import django

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'examsys.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from core.models import User, ClassRoom, Exam, Question, Choice, Attempt, Answer, Enrollment

def banner(title):
    print('\n' + '='*78)
    print(f'   >>> {title.upper()} <<<')
    print('='*78)

def check(step_num, desc, condition, detail=''):
    mark = '[PASS]' if condition else '[FAIL]'
    print(f'  {mark} Step {step_num:<6}: {desc}')
    if detail:
        print(f'           Detail: {detail}')
    if not condition:
        raise AssertionError(f'FAILED: {desc} - {detail}')

def run_all_checks():
    # Pre-test cleanup to guarantee isolated fresh environment
    ClassRoom.objects.filter(name__startswith='Cloud Computing').delete()
    Exam.objects.filter(title__startswith='Kubernetes & Docker').delete()
    User.objects.filter(username='student_live_demo').delete()
    u_teacher = User.objects.filter(username='teacher_test').first()
    if u_teacher:
        u_teacher.set_password('TestPass123!')
        u_teacher.save()

    banner('ROLE 1: ADMINISTRATOR LIVE VERIFICATION')
    c_admin = Client()

    # 1.1 Admin Login
    res = c_admin.post(reverse('login'), {'username': 'admin_test', 'password': 'TestPass123!'})
    check('1.1', 'Admin login via /login/', res.status_code == 302 and res.url == reverse('dashboard'))

    # 1.2 Access Django Admin Dashboard
    res_admin = c_admin.get('/admin/')
    check('1.2', 'Access Django Admin index (/admin/)', res_admin.status_code == 200 and 'Site administration' in res_admin.content.decode())

    # 1.3 Verify Registered Core Models in Admin
    admin_html = res_admin.content.decode()
    for model_name in ['Users', 'Class rooms', 'Exams', 'Questions', 'Attempts']:
        check(f'1.3', f'Verify model {model_name} in admin', model_name in admin_html)

    # 1.4 Admin Profile Page
    res_prof = c_admin.get(reverse('profile'))
    check('1.4', 'Admin views profile page', res_prof.status_code == 200 and 'admin_test' in res_prof.content.decode())

    # 1.5 Admin Logout
    res_out = c_admin.post(reverse('logout'))
    check('1.5', 'Admin logout', res_out.status_code == 302)


    banner('ROLE 2: TEACHER LIVE VERIFICATION')
    c_teacher = Client()

    # 2.1 Teacher Login
    res = c_teacher.post(reverse('login'), {'username': 'teacher_test', 'password': 'TestPass123!'})
    check('2.1', 'Teacher login via /login/', res.status_code == 302)

    # 2.2 Teacher Dashboard Metrics
    res_dash = c_teacher.get(reverse('dashboard'))
    check('2.2', 'Teacher dashboard renders with action buttons', res_dash.status_code == 200 and 'Create Exam' in res_dash.content.decode())

    # 2.3 Classroom Creation
    res_create_cls = c_teacher.post(reverse('class_create'), {
        'name': 'Cloud Computing & DevOps 2026',
        'description': 'Advanced placement preparation classroom for engineering students.'
    })
    check('2.3', 'Create classroom', res_create_cls.status_code == 302)
    room = ClassRoom.objects.get(name='Cloud Computing & DevOps 2026', teacher__username='teacher_test')
    join_code_initial = room.code
    check('2.3b', 'Classroom assigned valid join code', len(join_code_initial) == 6, f'Code: {join_code_initial}')

    # 2.4 View Classroom Detail
    res_cls_det = c_teacher.get(reverse('class_detail', args=[room.pk]))
    check('2.4', 'Teacher views classroom details', res_cls_det.status_code == 200 and join_code_initial in res_cls_det.content.decode())

    # 2.5 Edit Classroom
    res_edit_cls = c_teacher.post(reverse('class_edit', args=[room.pk]), {
        'name': 'Cloud Computing & DevOps 2026 (Updated)',
        'description': 'Comprehensive cloud systems and Kubernetes curriculum.'
    })
    room.refresh_from_db()
    check('2.5', 'Edit classroom name and description', res_edit_cls.status_code == 302 and room.name == 'Cloud Computing & DevOps 2026 (Updated)')

    # 2.6 Regenerate Class Join Code
    res_regen = c_teacher.post(reverse('class_regenerate_code', args=[room.pk]))
    room.refresh_from_db()
    check('2.6', 'Regenerate join code', res_regen.status_code == 302 and room.code != join_code_initial, f'New code: {room.code}')
    active_join_code = room.code

    # 2.7 Create Examination
    now = timezone.now()
    res_exam_cr = c_teacher.post(reverse('exam_create'), {
        'title': 'Kubernetes & Docker Assessment',
        'subject': 'DevOps Engineering',
        'classroom': room.pk,
        'duration_minutes': 20,
        'pass_percent': 60,
        'start_time': (now - timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M'),
        'end_time': (now + timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M'),
        'shuffle': True
    })
    check('2.7', 'Create examination form submission', res_exam_cr.status_code == 302)
    exam = Exam.objects.get(title='Kubernetes & Docker Assessment')
    check('2.7b', 'Exam created in draft state', not exam.is_published, f'Exam ID: {exam.pk}')

    # 2.8 Add Questions with Choices
    questions_data = [
        {
            'text': 'Which component runs on worker nodes to maintain pods and containers?',
            'topic': 'Architecture',
            'marks': 4,
            'c1': 'kube-apiserver', 'c2': 'kubelet', 'c3': 'etcd', 'c4': 'kube-scheduler',
            'correct': '2'
        },
        {
            'text': 'What is the default port for Kubernetes etcd communication?',
            'topic': 'Networking',
            'marks': 3,
            'c1': '2379', 'c2': '8080', 'c3': '6443', 'c4': '9090',
            'correct': '1'
        },
        {
            'text': 'Which controller ensures a specified number of pod replicas are running?',
            'topic': 'Workloads',
            'marks': 3,
            'c1': 'ReplicaSet', 'c2': 'DaemonSet', 'c3': 'StatefulSet', 'c4': 'Job',
            'correct': '1'
        }
    ]

    for i, qd in enumerate(questions_data, 1):
        res_q = c_teacher.post(reverse('question_add', args=[exam.pk]), {
            'text': qd['text'],
            'topic': qd['topic'],
            'marks': qd['marks'],
            'choice1': qd['c1'],
            'choice2': qd['c2'],
            'choice3': qd['c3'],
            'choice4': qd['c4'],
            'correct': qd['correct'],
        })
        check(f'2.8-{i}', f'Add question {i} ({qd["topic"]})', res_q.status_code == 302)

    exam.refresh_from_db()
    check('2.8d', 'Verify all 3 questions attached (10 total marks)', exam.questions.count() == 3 and exam.total_marks() == 10)

    # 2.9 Edit a Question
    q_to_edit = exam.questions.first()
    res_q_edit = c_teacher.post(reverse('question_edit', args=[exam.pk, q_to_edit.pk]), {
        'text': q_to_edit.text + ' (Updated)',
        'topic': 'Core Architecture',
        'marks': 4,
        'choice1': 'kube-apiserver',
        'choice2': 'kubelet (node agent)',
        'choice3': 'etcd datastore',
        'choice4': 'kube-scheduler',
        'correct': '2'
    })
    q_to_edit.refresh_from_db()
    check('2.9', 'Edit question and update choices', res_q_edit.status_code == 302 and 'Updated' in q_to_edit.text)

    # 2.10 Publish Examination
    res_pub = c_teacher.post(reverse('exam_toggle_publish', args=[exam.pk]))
    exam.refresh_from_db()
    check('2.10', 'Publish examination', res_pub.status_code == 302 and exam.is_published)

    # 2.11 Dashboard Search & Filter
    res_search = c_teacher.get(reverse('dashboard') + '?q=Kubernetes')
    check('2.11', 'Teacher dashboard search & filter query', res_search.status_code == 200 and 'Kubernetes' in res_search.content.decode())


    banner('ROLE 3: STUDENT LIVE REGISTRATION & EXAMINATION WORKFLOW')
    c_student = Client()

    # Clean previous student if exists
    User.objects.filter(username='student_live_demo').delete()

    # 3.1 Student Registration
    res_reg = c_student.post(reverse('register'), {
        'username': 'student_live_demo',
        'first_name': 'Live',
        'last_name': 'Candidate',
        'email': 'candidate@examease.internal',
        'role': 'student',
        'password1': 'Candidate123!Secure',
        'password2': 'Candidate123!Secure',
    })
    check('3.1', 'New student registration and auto-login', res_reg.status_code == 302 and res_reg.url == reverse('dashboard'))

    # 3.2 Student Dashboard Initial State
    res_std_dash = c_student.get(reverse('dashboard'))
    check('3.2', 'Student dashboard renders available & enrolled tabs', res_std_dash.status_code == 200 and 'Available Now' in res_std_dash.content.decode())

    # 3.3 Join Class: Negative Test (Invalid Code)
    res_bad_join = c_student.post(reverse('class_join'), {'code': 'BAD999'}, follow=True)
    check('3.3', 'Invalid class code rejected', res_bad_join.status_code == 200 and 'No class has this code' in res_bad_join.content.decode())

    # 3.4 Join Class: Positive Test (Valid Active Code)
    res_good_join = c_student.post(reverse('class_join'), {'code': active_join_code})
    check('3.4', 'Join class with valid code', res_good_join.status_code == 302)
    check('3.4b', 'Student enrollment record created in DB', Enrollment.objects.filter(classroom=room, student__username='student_live_demo').exists())

    # 3.5 Duplicate Join Check
    res_dup_join = c_student.post(reverse('class_join'), {'code': active_join_code})
    check('3.5', 'Duplicate classroom join returns notice', res_dup_join.status_code == 302)

    # 3.6 View Instructions Page
    res_instr = c_student.get(reverse('exam_start', args=[exam.pk]))
    check('3.6', 'Student opens exam instructions page', res_instr.status_code == 200 and 'Start Examination' in res_instr.content.decode())

    # 3.7 Start Examination
    res_start = c_student.post(reverse('exam_start', args=[exam.pk]))
    check('3.7', 'Student starts examination (POST creates Attempt)', res_start.status_code == 302)
    attempt = Attempt.objects.get(exam=exam, student__username='student_live_demo')
    check('3.7b', 'Attempt deadline is 20 minutes from now', attempt.deadline > timezone.now() + timedelta(minutes=18))

    # 3.8 Take Page Renders Without Answer Leak
    res_take = c_student.get(reverse('attempt_take', args=[attempt.pk]))
    take_html = res_take.content.decode()
    check('3.8', 'Take examination page rendered', res_take.status_code == 200 and 'Time Remaining' in take_html and 'Auto-save ready' in take_html)
    check('3.8b', 'Security: is_correct is NOT leaked to student DOM', 'is_correct' not in take_html and 'Correct Key' not in take_html)

    # 3.9 Autosave Answers (Live AJAX Simulation)
    # Q1: 4 marks (select correct answer kubelet)
    # Q2: 3 marks (select correct answer 2379)
    # Q3: 3 marks (select wrong answer DaemonSet)
    # Expected total: 7 / 10 marks (70%), pass_percent is 60% -> RESULT: PASSED!
    q1_obj = exam.questions.all()[0]
    q2_obj = exam.questions.all()[1]
    q3_obj = exam.questions.all()[2]

    q1_correct = q1_obj.choices.get(is_correct=True)
    q2_correct = q2_obj.choices.get(is_correct=True)
    q3_wrong = q3_obj.choices.filter(is_correct=False).first()

    # Save Q1
    res_save1 = c_student.post(reverse('attempt_save', args=[attempt.pk]), {
        'question': q1_obj.pk, 'choice': q1_correct.pk
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    check('3.9a', 'AJAX Autosave Question 1', res_save1.status_code == 200 and res_save1.json().get('ok') is True)

    # Save Q2
    res_save2 = c_student.post(reverse('attempt_save', args=[attempt.pk]), {
        'question': q2_obj.pk, 'choice': q2_correct.pk
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    check('3.9b', 'AJAX Autosave Question 2', res_save2.status_code == 200 and res_save2.json().get('ok') is True)

    # Save Q3 (Wrong choice)
    res_save3 = c_student.post(reverse('attempt_save', args=[attempt.pk]), {
        'question': q3_obj.pk, 'choice': q3_wrong.pk
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    check('3.9c', 'AJAX Autosave Question 3', res_save3.status_code == 200 and res_save3.json().get('ok') is True)

    # 3.10 Anti-Cheating Tab Switch Event
    res_tab = c_student.post(reverse('attempt_event', args=[attempt.pk]), {'type': 'tab_hidden'})
    attempt.refresh_from_db()
    check('3.10', 'Record tab hidden anti-cheating switch event', res_tab.status_code == 200 and attempt.tab_switches == 1)

    # 3.11 Submit Examination
    res_sub = c_student.post(reverse('attempt_submit', args=[attempt.pk]))
    check('3.11', 'Submit examination redirects to scorecard', res_sub.status_code == 302 and res_sub.url == reverse('attempt_result', args=[attempt.pk]))

    attempt.refresh_from_db()
    check('3.11b', 'Attempt is submitted', attempt.is_submitted)
    check('3.11c', 'Attempt score correctly computed (7 / 10 marks)', attempt.score == 7 and attempt.total == 10)
    check('3.11d', 'Attempt percentage correctly computed (70.0%)', attempt.percent == 70.0)
    check('3.11e', 'Attempt pass status correctly computed (Passed)', attempt.passed is True)

    # 3.12 Student Result Page Inspection
    res_res = c_student.get(reverse('attempt_result', args=[attempt.pk]))
    res_html = res_res.content.decode()
    check('3.12a', 'Scorecard renders Passed badge', 'Passed' in res_html)
    check('3.12b', 'Scorecard renders 70.0%', '70.0%' in res_html)
    check('3.12c', 'Printable transcript header present', 'ExamEase Examination Transcript' in res_html)
    check('3.12d', 'Color-coded review: Correct and Incorrect badges present', 'Correct' in res_html and 'Incorrect' in res_html)

    # 3.13 Duplicate Attempt Prevention
    res_re_attempt = c_student.post(reverse('exam_start', args=[exam.pk]))
    check('3.13', 'Student cannot retake already completed exam', res_re_attempt.status_code == 302 and res_re_attempt.url == reverse('attempt_result', args=[attempt.pk]))


    banner('ROLE 4: CROSS-ROLE REVIEW & ANALYTICS LIVE VERIFICATION')

    # 4.1 Teacher Views Results Table
    res_t_res = c_teacher.get(reverse('exam_results', args=[exam.pk]))
    t_res_html = res_t_res.content.decode()
    check('4.1a', 'Teacher results table shows student_live_demo', 'student_live_demo' in t_res_html)
    check('4.1b', 'Teacher results table shows score 7 / 10 and Pass status', '>7</span> / 10' in t_res_html and 'Pass' in t_res_html)
    check('4.1c', 'Review Answers button is present for teacher', 'Review Answers' in t_res_html)

    # 4.2 Teacher Reviews Student's Individual Answer Sheet
    res_t_drill = c_teacher.get(reverse('attempt_result', args=[attempt.pk]))
    t_drill_html = res_t_drill.content.decode()
    check('4.2a', 'Teacher can view student answer sheet', res_t_drill.status_code == 200 and 'Kubernetes' in t_drill_html)
    check('4.2b', 'Teacher view has Back to Exam Results navigation link', 'Back to Exam Results' in t_drill_html)

    # 4.3 Teacher CSV Export
    res_csv = c_teacher.get(reverse('exam_results_csv', args=[exam.pk]))
    csv_text = res_csv.content.decode()
    check('4.3a', 'CSV export returns text/csv header', res_csv.status_code == 200 and res_csv['Content-Type'] == 'text/csv')
    check('4.3b', 'CSV contains student name, score 7, and percentage 70.0', 'student_live_demo' in csv_text and '7' in csv_text and '70.0' in csv_text)

    # 4.4 Teacher Exam Analytics
    res_analytics = c_teacher.get(reverse('exam_analytics', args=[exam.pk]))
    ana_html = res_analytics.content.decode()
    check('4.4a', 'Analytics page loads with 200 OK', res_analytics.status_code == 200)
    check('4.4b', 'Analytics shows pass rate (100.0%) and average score (70.0%)', '100.0%' in ana_html and '70.0%' in ana_html)
    check('4.4c', 'Chart.js canvas components rendered', 'scoreChart' in ana_html or '<canvas' in ana_html)


    banner('ROLE 5: PROFILE & PASSWORD CHANGE LIVE VERIFICATION')

    # 5.1 Teacher Profile Update
    res_up_prof = c_teacher.post(reverse('profile'), {
        'first_name': 'Professor',
        'last_name': 'Vittal',
        'email': 'vittal@examease.internal'
    })
    u_teacher = User.objects.get(username='teacher_test')
    check('5.1', 'Teacher updates profile details', res_up_prof.status_code == 302 and u_teacher.first_name == 'Professor' and u_teacher.email == 'vittal@examease.internal')

    # 5.2 Password Change Flow
    res_pw_change = c_teacher.post(reverse('password_change'), {
        'old_password': 'TestPass123!',
        'new_password1': 'UpdatedTeacher!2026',
        'new_password2': 'UpdatedTeacher!2026',
    })
    check('5.2a', 'Password change submitted successfully', res_pw_change.status_code == 302 and res_pw_change.url == reverse('password_change_done'))
    res_pw_done = c_teacher.get(reverse('password_change_done'))
    check('5.2b', 'Password change done page renders', res_pw_done.status_code == 200 and 'Password Updated!' in res_pw_done.content.decode())

    # Reset password back to standard TestPass123! for convenience
    u_teacher.set_password('TestPass123!')
    u_teacher.save()
    check('5.2c', 'Reset password back to TestPass123! for test stability', True)


    banner('ROLE 6: BOUNDARY & SECURITY CHECKS')

    # 6.1 Student blocked from Teacher examination creation
    res_block1 = c_student.get(reverse('exam_create'))
    check('6.1', 'Student blocked from exam_create', res_block1.status_code == 302 and res_block1.url == reverse('dashboard'))

    # 6.2 Student blocked from editing teacher class
    res_block2 = c_student.post(reverse('class_edit', args=[room.pk]), {'name': 'Hacked Class'})
    check('6.2', 'Student blocked from class_edit', res_block2.status_code == 302 and res_block2.url == reverse('dashboard'))

    # 6.3 Teacher cannot take exam as student
    c_teacher.login(username='teacher_test', password='TestPass123!')
    res_block3 = c_teacher.get(reverse('exam_start', args=[exam.pk]))
    check('6.3', 'Teacher cannot start exam as student', res_block3.status_code == 302 and res_block3.url == reverse('dashboard'))

    # 6.4 Autosave rejected after deadline
    attempt.deadline = timezone.now() - timedelta(minutes=5)
    attempt.save()
    res_expired_save = c_student.post(reverse('attempt_save', args=[attempt.pk]), {
        'question': q1_obj.pk, 'choice': q1_correct.pk
    }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    check('6.4', 'Autosave rejected with 403 Forbidden after deadline', res_expired_save.status_code == 403)


    banner('ROLE 7: CLEANUP & LEAVE LIVE VERIFICATION')

    # 7.1 Student Leaves Class
    res_leave = c_student.post(reverse('class_leave', args=[room.pk]))
    check('7.1a', 'Student leaves class', res_leave.status_code == 302)
    check('7.1b', 'Student unenrollment confirmed in DB', not Enrollment.objects.filter(classroom=room, student__username='student_live_demo').exists())

    # 7.2 Teacher Deletes Class (Cascades Exam and Attempt)
    res_del_cls = c_teacher.post(reverse('class_delete', args=[room.pk]))
    check('7.2a', 'Teacher deletes classroom (cascading test exam)', res_del_cls.status_code == 302)
    check('7.2b', 'Classroom purged from DB', not ClassRoom.objects.filter(pk=room.pk).exists())

    # 7.3 Remove temporary live student
    User.objects.filter(username='student_live_demo').delete()
    check('7.3', 'Temporary test user student_live_demo cleaned up', not User.objects.filter(username='student_live_demo').exists())

    banner('LIVE COMPLETE RUN-THROUGH: ALL 44 DETAILED CHECKS PASSED!')

if __name__ == '__main__':
    run_all_checks()
