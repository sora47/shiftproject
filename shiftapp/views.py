from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import DutyChoiceForm
from .models import ShiftBaseModel, ShiftModel
from .function import month_calendar, shiftbase_list, prevnextmonth_dic
from datetime import datetime

# Create your views here.

WEEKDAY = ['日', '月', '火', '水', '木', '金', '土']


# アカウント登録
def signup_func(request):
    if request.method == 'POST':
        postusername = request.POST['username']
        postlastname = request.POST['lastname']
        postpassword = request.POST['password']
        try:
            User.objects.get(username=postusername)
            d = {'error': 'このユーザーは登録されています．'}
            return render(request, 'signup.html', d)
        except:
            user = User.objects.create_user(postusername, '', postpassword)
            user.last_name = postlastname
            user.save()
            user = authenticate(request, username=postusername, password=postpassword)
            login(request, user)
            return redirect('top')
    return render(request, 'signup.html', {})


# ログイン
def login_func(request):
    if request.method == 'POST':
        postusername = request.POST['username']
        postpassword = request.POST['password']
        user = authenticate(request, username=postusername, password=postpassword)
        if user is not None:
            login(request, user)
            return redirect('top')
        else:
            d = {'error': 'ユーザー名かパスワードが正しくありません。'}
            return render(request, 'login.html', d)
    return render(request, 'login.html', {})


@login_required
# トップページ
def top_func(request):
    user = request.user.last_name
    today = datetime.now()
    if today.month == 12:
        nextmonth = 1
        nextyear = today.year + 1
    else:
        nextmonth = today.month + 1
        nextyear = today.year
    d = {
        'user': user,
        'thisyear': today.year,
        'thismonth': today.month,
        'nextyear': nextyear,
        'nextmonth': nextmonth
    }
    if request.user.is_staff == True:
        d['staff'] = True
    return render(request, 'top.html', d)


# ログアウト
def logout_func(request):
    logout(request)
    return redirect('login')


# シフト登録
def registshift_func(request, year, month):
    if not ShiftBaseModel.objects.filter(year=year, month=month):
        d = {
            'error': "このシフトは登録できません。"
        }
        d.update(prevnextmonth_dic(year, month))
        return render(request, 'registshift.html', d)
    elif month < datetime.now().month:
        d = {
            'error': "シフト登録期間外です。"
        }
        d.update(prevnextmonth_dic(year, month))
        return render(request, 'registshift.html', d)

    if request.method == "POST":
        list = request.POST.getlist('checked')
        loginuserid = request.user.id
        ShiftModel.objects.filter(user_id=loginuserid, year=year, month=month).delete()
        for i in list:
            ShiftModel.objects.create(user_id=loginuserid, year=year, month=month, base_id=i)
        return redirect('top')

    cllist = month_calendar(year, month)
    model = ShiftBaseModel.objects.filter(year=year, month=month)
    modellist = shiftbase_list(cllist, model)
    d = {'modellist': modellist,
         'weekday': WEEKDAY}
    d.update(prevnextmonth_dic(year, month))
    return render(request, 'registshift.html', d)


# シフト募集日程登録
def registshiftbase_func(request, year, month):
    if not request.user.is_staff:
        return render(request, 'foully.html', {})

    if month > datetime.now().month + 2 or month < datetime.now().month - 2:
        d = {
            'error': "シフト登録期間外です。"
        }
        d.update(prevnextmonth_dic(year, month))
        return render(request, 'registshiftbase.html', d)

    if request.method == "POST":
        list = request.POST.getlist('checked')
        model = ShiftBaseModel.objects.filter(year=year, month=month)
        for obj in model:
            obj.check = False
            obj.two = False
            obj.duty = ""
            obj.save()
        for i in list:
            obj = ShiftBaseModel.objects.get(pk=i)
            if obj.check == True:
                obj.two = True
            else:
                obj.check = True
            obj.save()
        return redirect('top')

    cllist = month_calendar(year, month)
    modellist = []
    if ShiftBaseModel.objects.filter(year=year, month=month):
        model = ShiftBaseModel.objects.filter(year=year, month=month)
        modellist = shiftbase_list(cllist, model)
    else:
        for week in cllist:
            list = [week]
            for i in range(3):
                periodtimelist = []
                for day in week:
                    if day != '-':
                        periodtimelist.append(
                            ShiftBaseModel.objects.create(check=False, year=year, month=month, two=False))
                    else:
                        periodtimelist.append(
                            ShiftBaseModel.objects.create(check=False, year=year, month=month, two=False))

                list.append(periodtimelist)
            modellist.append(list)
    d = {'modellist': modellist,
         'weekday': WEEKDAY}
    d.update(prevnextmonth_dic(year, month))
    return render(request, 'registshiftbase.html', d)


# シフト選択
def choiceshift_func(request, year, month):
    if not request.user.is_staff:
        return render(request, 'foully.html', {})
    if not ShiftBaseModel.objects.filter(year=year, month=month):
        d = {
            'error': "このシフトは登録できません。"
        }
        d.update(prevnextmonth_dic(year, month))
        return render(request, 'choiceshift.html', d)
    elif month < datetime.now().month - 2:
        d = {
            'error': "シフト登録期間外です。"
        }
        d.update(prevnextmonth_dic(year, month))
        return render(request, 'choiceshift.html', d)

    dict = {}
    if request.method == "POST":
        basemodel = ShiftBaseModel.objects.filter(check=True, year=year, month=month)
        list = request.POST.getlist('choice')
        list2 = request.POST.getlist('choice2')
        for data in basemodel:
            if len(list) == 0:
                break
            data.duty = list.pop(0)
            if data.two == True:
                data.duty = data.duty + " " + list2.pop(0)
            data.save()
        if 'regist' in request.POST:
            return redirect('top')
        else:
            list = request.POST.getlist('choice')
            for user in User.objects.all():
                dict[user.last_name] = list.count(user.last_name)

    basemodel = ShiftBaseModel.objects.filter(year=year, month=month)
    formlist = []
    for i in basemodel:
        if i.check == True:
            model = ShiftModel.objects.filter(base_id=i.id)
            choice = [('未定', ' ')]
            for j in model:
                user = User.objects.get(id=j.user_id)
                choice.append((user.last_name, user.last_name))
            form = DutyChoiceForm()
            form.fields['choice'].choices = choice
            if i.two == True:
                form.fields['choice2'].choices = choice
                if i.duty != "":
                    namelist = i.duty.split()
                    form.fields['choice'].initial = namelist[0]
                    form.fields['choice2'].initial = namelist[1]
            else:
                if i.duty != "":
                    form.fields['choice'].initial = i.duty
        else:
            form = ""
        formlist.append(form)
    cllist = month_calendar(year, month)
    formlist = shiftbase_list(cllist, formlist)
    d = {'formlist': formlist,
         'weekday': WEEKDAY,
         'countdic': dict}
    d.update(prevnextmonth_dic(year, month))
    return render(request, 'choiceshift.html', d)


# シフト表示
def viewshift_func(request, year, month):
    if not ShiftBaseModel.objects.filter(year=year, month=month):
        d = {
            'error': "シフトが作成されていません。"
        }
        d.update(prevnextmonth_dic(year, month))
        return render(request, 'viewshift.html', d)
    if request.method == "POST":
        return redirect('top')
    basemodel = ShiftBaseModel.objects.filter(year=year, month=month)
    formlist = []
    for i in basemodel:
        if i.check == True:
            model = ShiftModel.objects.filter(base_id=i.id)
            choice = [('未定', ' ')]
            for j in model:
                user = User.objects.get(id=j.user_id)
                choice.append((user.last_name, user.last_name))
            form = DutyChoiceForm()
            form.fields['choice'].choices = choice
            if i.two == True:
                form.fields['choice2'].choices = choice
                if i.duty != "":
                    namelist = i.duty.split()
                    form.fields['choice'].initial = namelist[0]
                    form.fields['choice2'].initial = namelist[1]
            else:
                if i.duty != "":
                    form.fields['choice'].initial = i.duty
        else:
            form = ""
        formlist.append(form)
    cllist = month_calendar(year, month)
    formlist = shiftbase_list(cllist, formlist)
    d = {'formlist': formlist,
         'weekday': WEEKDAY,
         'countdic': dict}
    d.update(prevnextmonth_dic(year, month))
    return render(request, 'viewshift.html', d)


def deleteuser_func(request):
    if not request.user.is_staff:
        return render(request, 'foully.html', {})
    if request.method == "POST":
        user = User.objects.get(pk=request.POST['userid'])
        user.delete()
        d = {
            'usermodel': User.objects.all(),
            'message': '削除しました。',
        }
        return render(request, 'delete.html', d)
    d = {
        'usermodel': User.objects.all()
    }
    return render(request, 'delete.html', d)


def changestaff_func(request):
    if not request.user.is_staff:
        return render(request, 'foully.html', {})
    if request.method == "POST":
        user = User.objects.get(pk=request.POST['userid'])
        user.is_staff = True
        user.save()
        user = User.objects.get(pk=request.user.id)
        user.is_staff = False
        user.save()
        return redirect('top')
    d = {
        'usermodel': User.objects.all()
    }
    return render(request, 'changestaff.html', d)