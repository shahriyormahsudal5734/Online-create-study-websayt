
from .models import Oquv_Markaz1,Kurs,Category,Ariza,Viloyat1
from django.http import HttpResponse
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm
from django.views.generic.edit import UpdateView
from .filters import ProductFilter
def homepage(request):
    pagecheck = 'home'
    kurs = Oquv_Markaz1.objects.all().order_by('-id')
    dars = ProductFilter(request.GET, queryset=Kurs.objects.all())
    if request.user.is_active == True:
        users = request.user.oquv_markaz1_set.all()
    else:
        users=''
    if request.method == 'POST' and request.user.is_active == True:
        newmarkaz = Oquv_Markaz1.objects.create(
            user=request.user,
            title = request.POST.get('qtitle'),
            body = request.POST.get('qbody'),
            img = request.FILES.get('qimg'),
            number = request.POST.get('qnumber'),
            checking=False,
            telegram = request.POST.get('qtelegram'),
            instagram = request.POST.get('qinstagram'),
            facebook = request.POST.get('qfacebook'),
            youtobe = request.POST.get('qyoutobe'),
            manzil = request.POST.get('qmanzil'),
            viloyat1 = Viloyat1.objects.get(id=request.POST.get('qviloyat1')),
        )
        newmarkaz.save()
        return redirect('room',newmarkaz.id)
    context ={
        'kurs':kurs,
        'users':users,
        'dars':dars,
        'pagecheck':pagecheck,
        'all_viloyat':Viloyat1.objects.all().order_by('-id')
    }


    return render(request,'index.html',context)

def markaz(request,id):
    pagecheck = 'detail'
    room = Oquv_Markaz1.objects.get(id=id)
    categ = Category.objects.all().order_by('-id')
    kurslar = room.kurs_set.all().order_by('-id')
    allapply = 0
    for x in  room.kurs_set.all():
      if len(str(x.applys)) > 0:
        allapply += int(x.applys)
    room.applys = allapply
    room.save()

    if request.method == 'POST':
          getcategory = Category.objects.get(id=request.POST.get('kcategory'))
          kurs =  Kurs.objects.create(
          markaz=room,
          viloyatlar=room.viloyat1,
          title=request.POST.get('ktitle'),
          body=request.POST.get('kbody'),
          img=request.FILES.get('kimg'),
          davomiyligi=request.POST.get('kdavomiyligi'),
          price=request.POST.get('kprice'),
          category = getcategory,
          )
          kurs.save()
          return redirect('detailkurs',kurs.id)
    else:
        pass

    context ={
        'room':room,
        'kurslar':kurslar,
        'pagecheck':pagecheck,
        'categ':categ,
        'all_apply':Ariza.objects.all().order_by('-id'),
    }

    return render(request,'topics-detail.html',context)



class Updateoquv(UpdateView):
    model = Oquv_Markaz1
    template_name = "oquvupdate.html"
    fields = ['title','body','img','number','telegram','instagram','facebook','youtobe','viloyat1','manzil']






def oquv_true(request,id):
    data = Oquv_Markaz1.objects.get(id=id)
    data.checking = True
    data.save()
    return redirect('all_shcoll')

def delete_true(request,id):
    data = Oquv_Markaz1.objects.get(id=id)
    if len(data.img) > 0:
        os.remove(data.img.path)
    data.delete()
    return redirect('all_shcoll')


def removekurs(request,id):
    kurs_info = Kurs.objects.get(id=id)
    
    if len(kurs_info.img) > 0:
        os.remove(kurs_info.img.path)
    else:
        pass
    kurs_info.delete()
    return redirect('room',kurs_info.markaz.id)

def ariza_true(request,id):
    kurs_info = Ariza.objects.get(id=id)
    kurs_info.ariza_chek = True
    kurs_info.save()
    return redirect('room',kurs_info.category.markaz.id)
def ariza_false(request,id):
    kurs_info = Ariza.objects.get(id=id)
    kurs_info.ariza_chek = False
    kurs_info.save()
    return redirect('room',kurs_info.category.markaz.id)
def detailkurs(request,id):
    pagecheck = 'detail'
    show = 'true'
    kurs_info = Kurs.objects.get(id=id)
    requestname = f'{kurs_info.id}'
    kurs_info.applys =  kurs_info.ariza_set.all().count() 
    kurs_info.save()
    
    if request.COOKIES.get(requestname) == None:
        show = 'true'
    else:
        show = 'false'
    
    

    if request.method=='POST':
        response = redirect('detailkurs',kurs_info.id)
        response.set_cookie(requestname,'1')
        Ariza.objects.create(
            category=kurs_info,
            title=request.POST.get('atitle'),
            body=request.POST.get('abody'),
            img=request.FILES.get('aimg'),
            age=request.POST.get('aage'),
            number=request.POST.get('anumber'),
            ariza_chek=False,
        )
        

        return  response
    
        

    context ={
        'kurs_info':kurs_info,
        'pagecheck':pagecheck,
        'show':show,
        'all_ariza':kurs_info.ariza_set.all(),
    }
    return render(request,'detailkurs.html',context)
def all_shcoll(request):

    data1 = Oquv_Markaz1.objects.all().order_by('-id')
    context ={
        'data1':data1
    }
    return render(request,'topics-listing.html',context)

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')