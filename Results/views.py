from django.shortcuts import render
from django.shortcuts import redirect

from WebTesting.models import StudTests, Attempts, StudAnswers
from TestSystem.models import SignUp_Model
from TestCreation.models import TeacherTests, Questions

def attempt_result(request):
    if request.method == 'POST':
        try:
            del request.session['attempt_id']
        except:
            pass
        return redirect('/student_result/')

    ##################################################
    # Изменить, указав соответствующие request
    # request.session['user_id'] = '2'
    # request.session['test_id'] = '18'
    # request.session['passed_test_id'] = '1'
    # request.session['attempt_id'] = '1'
    # request.session['student'] = '2'
    ##################################################

    query_test_info = TeacherTests.objects.get(id=request.session['test_id'])
    query_questions = Questions.objects.filter(test_id_id=request.session['test_id']).all()
    query_answers = StudAnswers.objects.filter(attempt_id=request.session['attempt_id']).all() 
    query_attempt_info = Attempts.objects.get(id=request.session['attempt_id'])
    query_user = SignUp_Model.objects.get(pk=request.session['student'])

    return render(request, 'attempt_result.html', {
        'test_info': query_test_info, # Общая информация по тесту
        'attempt_info': query_attempt_info, # Информация по попытке
        'res': int(query_attempt_info.result / query_test_info.question_count  * 100), # Результат
        'zipping': zip(query_questions, query_answers), # Вопросы и ответы
        'user': query_user, # Данные о пользователе        
    })

def student_result(request):

    if request.method == 'POST':
        if request.POST.get("action", "") == "info":
            request.session['attempt_id'] = request.POST.get("more_info")
            return redirect('/attempt_result/')
        
        if request.POST.get("back"):
            try:
                del request.session['student']
            except:
                pass
            try:
                user = SignUp_Model.objects.get(pk=int(request.session['user_id']))
                if user.user_type == 'stud':
                    return redirect('/profile/') # Тут профиль
                else:
                    return redirect('/test_result/') # Тут редирект на страницу статистики по тесту
            except:
                return redirect('/profile/') # Тут профиль


    ##################################################
    # Изменить, указав соответствующие request
    # request.session['user_id'] = '2'
    # request.session['test_id'] = '18'
    # request.session['student'] = '2'
    # request.session['attempt_id'] = '1'
    ##################################################

    test = StudTests.objects.get(test_id=request.session['test_id'])
    request.session['passed_test_id'] = test.id
    query_test_info = TeacherTests.objects.get(id=request.session['test_id'])
    # query_questions = Questions.objects.filter(test_id_id=request.session['test_id']).all()
    query_attempt_info = Attempts.objects.filter(passed_test_id=request.session['passed_test_id'])
    query_user = SignUp_Model.objects.get(pk=request.session['student'])
    res = []
    for attempt in query_attempt_info:
        res.append(int(attempt.result / query_test_info.question_count  * 100))

    return render(request, 'student_result.html', {
        'test_info': query_test_info, # Общая информация по тесту
        'attempts': zip(query_attempt_info, res), # Информация по всем попыткам
        'user': query_user,
    })

def test_result(request):
    if request.method == 'POST':
        if request.POST.get("action", "") == "info":
            request.session['student'] = request.POST.get("more_info")
            return redirect('/student_result/')
        
        if request.POST.get("back"):
            try:
                del request.session['test_id']
            except:
                pass
            return redirect('/profile/') # Тут профиль


    ##################################################
    # Изменить, указав соответствующие request
    # request.session['user_id'] = '2'
    # request.session['test_id'] = '18'
    # request.session['passed_test_id'] = '1'
    # request.session['student'] = '2'
    ##################################################

    query_test_info = TeacherTests.objects.get(id=request.session['test_id'])
    query_user = []
    tests = StudTests.objects.filter(test_id=request.session['test_id'])
    for test in tests:
        query_user.append(SignUp_Model.objects.get(pk=test.user_id))
  
    return render(request, 'test_result.html', {
        'test_info': query_test_info, # Общая информация по тесту
        'users': zip(query_user, tests), # Пользователи, проходившие этот тест

    })