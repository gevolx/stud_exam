from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .forms import SignUpForm, ChangeForm, UserLoginForm
from .models import SignUp_Model

# def login_view(request):
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#     return render(request, 'sign_in.html', {'form': form})


# Заглавная страница, надо что-то сюда вставить
def index(request):
    form = UserLoginForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        request.session['user_id'] = user.id
        print(request.session['user_id'])
        _next = _next or '/'
        return redirect('/profile/')
        # if SignUp_Model.objects.get(username=username).user_type == 'teacher':
        #     return redirect('/create_test/')
        # else:
        #     return render(request, 'sign_in.html', {'form': form})
    return render(request, 'sign_in.html', {'form': form})
   #return render(request, 'sign_in.html', {})

def logout_view(request):
    logout(request)
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')


def sign_in(request):
    # form = UserLoginForm(request.POST or None)
    # if form.is_valid():
    #     username = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)
    #     login(request, user)
    # return render(request, 'sign_in.html', {'form': form})
    #return render(request, 'sign_in.html', {})
    pass




def admin_panel(request):
    if request.method == 'POST':
        ans = '0'
        form = SignUpForm(request.POST)
        form1 = ChangeForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, password=raw_password)
            user.save()

            return redirect('/admin_panel/')

        elif request.POST.get('btn5'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            status = request.POST.get('choose_user')
            print(status)
            status = not(eval(status.split('+')[0]))
            print(status)
            u = User.objects.get(username=username)
            if password != '':
                u.set_password(password)           
                SignUp_Model.objects.filter(username=username).update(password=password)
            SignUp_Model.objects.filter(username=username).update(locked=status)
            SignUp_Model.objects.filter(username=username).update(login_attempts=0)
            SignUp_Model.save
            u.save

            return redirect('/admin_panel/')
        
        elif request.POST.get('btn4'):
            username = request.POST.get('username')
            SignUp_Model.objects.filter(username=username).delete()
            u = User.objects.get(username=username)
            u.delete()
            return redirect('/admin_panel/')

        else:
            return forms.ValidationError("This isnt any name!")

    else:
        # ans - индекс новой записи для генерации логина
        ans = str(SignUp_Model.objects.order_by('-id').first()).split()[-1][1:-1]
        if ans.isdigit():
            ans = str(int(ans) + 1)
        else:
            ans = 1
        options = SignUp_Model.objects.order_by('username').all()
        form = SignUpForm()
        form1 = ChangeForm()
    return render(request, 'admin_panel.html', {
        'form': form, 
        'ans': ans,
        'form1': form1,
        'options': options,
        })