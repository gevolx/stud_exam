from django.shortcuts import render
from django.shortcuts import redirect

from .models import StudTests, Attempts, StudAnswers
from TestSystem.models import SignUp_Model
from TestCreation.models import TeacherTests, Questions


def web_testing(request):
    ##################################################
    # Изменить, указав соответствующие request
    # request.session['user_id'] = '2'
    # request.session['test_id'] = '18'
    # request.session['passed_test_id'] = '1'
    # request.session['attempt_id'] = '1'
    ##################################################

    query_test_info = TeacherTests.objects.get(id=request.session['test_id'])
    student = StudTests.objects.get(test_id=request.session['test_id'])
    show_attempt = query_test_info.attempt_count - student.attempts_count
    print(show_attempt)
    query_questions = Questions.objects.filter(test_id_id=request.session['test_id']).all().order_by('?')
   
    if request.method == 'POST':
        if request.POST.get('start_test'):
            return render(request, 'web_testing.html', {
                    'query': query_questions, # Вопросы
                    'test_info': query_test_info, # Общая информация по тесту
                })

        elif request.POST.get('finish'):
            read_answers = request.POST.get("answer_to_send", None)
            timer = request.POST.get("finish_time", None)
            answers = {}
            right_ans_counter = 0
            if read_answers != None:
                read_answers = read_answers.split(',')
                for i in read_answers:
                    quest_num, ans = i.split('=')
                    answers[quest_num] = ans 
            test = TeacherTests.objects.get(pk=request.session['test_id'])
            for q in query_questions:
                stud = StudAnswers()
                quest_num = str(q.id)
                stud.question_id = quest_num
                stud.attempt_id = request.session['attempt_id']

                if quest_num in answers:

                    if q.manychoises:
                        correct = True
                        anses = answers[quest_num]
                        if (anses[0] == '1' and q.isright1) or (anses[0] == '0' and not q.isright1):
                            correct = False
                        if (anses[1] == '1' and q.isright2) or (anses[1] == '0' and not q.isright2):
                            correct = False
                        if (anses[2] == '1' and q.isright3) or (anses[2] == '0' and not q.isright3):
                            correct = False
                        if (anses[3] == '1' and q.isright4) or (anses[3] == '0' and not q.isright4):
                            correct = False
                        stud.iscorrect = correct
                        right_ans_counter += 1 if correct else 0
                        stud.choosen_answer1 = True if anses[0] == '1' else False
                        stud.choosen_answer2 = True if anses[1] == '1' else False
                        stud.choosen_answer3 = True if anses[2] == '1' else False
                        stud.choosen_answer4 = True if anses[3] == '1' else False
                    else:
                        anses = [q.isright1, q.isright2, q.isright3, q.isright4]
                        stud.iscorrect = True if anses[int(answers[quest_num])-1] else False
                        right_ans_counter += 1 if anses[int(answers[quest_num])-1] else 0
                        stud.choosen_answer1 = True if answers[quest_num] == '1' else False
                        stud.choosen_answer2 = True if answers[quest_num] == '2' else False
                        stud.choosen_answer3 = True if answers[quest_num] == '3' else False
                        stud.choosen_answer4 = True if answers[quest_num] == '4' else False

                else:
                    stud.iscorrect = False
                    stud.choosen_answer1 = False
                    stud.choosen_answer2 = False
                    stud.choosen_answer3 = False
                    stud.choosen_answer4 = False

                stud.save()
            attempts = Attempts.objects.get(pk=request.session['attempt_id'])
            if timer != "EXPIRED":
                attempts.time = query_test_info.time - int(timer.split(':')[2])
            else:
                attempts.time = 0
            attempts.result = right_ans_counter
            attempts.save()
            update_best = StudTests.objects.get(pk=request.session['passed_test_id'])
            update_best.best_result = max(update_best.best_result, (right_ans_counter / test.question_count * 100))
            update_best.save()
            del request.session['test_id']
            del request.session['passed_test_id']
            del request.session['attempt_id']

        return redirect('/profile/')

    else:
        return render(request, 'start_test.html', {
            'item': query_test_info,
            'student': show_attempt,
            })


    # user = SignUp_Model.objects.get(pk=request.session['user_id'])
    # test = TeacherTests.objects.get(pk=request.session['test_id'])
    # passed_test = StudTests(user=user, test=test)
    # passed_test.save()


    # passed_test_id = StudTests.objects.get(pk=request.session['passed_test_id'])
    # attempt = Attempts(passed_test=passed_test_id)
    # attempt.save()
