from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from .forms import StudentForm,Editstudent,ClassForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login as loginfun,logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime
# Create your views here.
def home(request):
    return render(request,'home.html')
def apply(request):
    form=StudentForm(request.POST or None , request.FILES or None)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect(home)

    return render(request,'apply.html',{'form':form})

def login(request):
    loginform=AuthenticationForm(request,request.POST or None)
    if request.method=="POST":
        if loginform.is_valid():
            username=loginform.cleaned_data.get('username')
            password=loginform.cleaned_data.get('password')

            user=authenticate(username=username,password=password)
            if user is not None:
                print(user)
                loginfun(request,user)
                return redirect(home)
            else:
                messages.error(request,'invalid username or password')
                return redirect(login)
    return render(request,'login.html',{'login':loginform})
@login_required()
def logoutfun(request):
    logout(request)
    return redirect(login)
@login_required()
def manageStudent(request):
    data={}
    data['student']=Student.objects.filter(isApproved=True)
    return render(request,'admin/managestudent.html',data)

def manageAdmission(request):
    data={}
    data['student']=Student.objects.filter(isApproved=False)
    return render (request,'admin/managestudent.html',data)

@login_required()
def delete(request,id):
    std=Student.objects.get(pk=id)
    std.delete()
    return redirect(manageStudent)

@login_required
def edit(request,id):
    std=Student.objects.get(pk=id)
    form=Editstudent(request.POST or None or request.FILES or None,instance=std)

    if(request.method=="POST"):
        if form.is_valid():
         form.save()
         return redirect(manageStudent)
    return render(request,'admin/editstudent.html',{'form':form})

def viewstudent(request,id):
   student=Student.objects.get(pk=id)
   payments=Payment.objects.filter(student=student)
   return render(request,'admin/view.html',{'students':student,'payment':payments})

def approve(request,id):
    student=Student.objects.get(id=id,isApproved=False)
    current_month=datetime.now().month
    for month in range(-1,12):
        p= Payment()
        p.student=student
        p.month=MONTH[month][0]
        p.amount=800
        p.save()
    student.isApproved=True
    student.save()
    return redirect(manageStudent)

def manageClasses(r):
    form = ClassForm(r.POST or None)
    data = {}
    data['title'] = "Manage Classes"
    data['form'] = form 
    data['classes'] = Classes.objects.all()
    

    if r.method == "POST":
        if form.is_valid():
            form.save()
            return redirect(manageClasses)

    return render(r, "admin/manageClasses.html",data)
# def viewstudent_classby(request,id):
#     data={}
#     data['student']=Student.objects.filter(className=id)
    
#     return render(request,'admin/manageclasses.html',data)
def viewClassWise(r,className):
    data = {}
    print(className)
    data['student']=Student.objects.filter(className__class_name=className,isApproved=True)
   
    return render(r, "admin/manageStudent.html", data)

def scanRfCode(r):
    code=r.GET.get('code')
    
    
    student=get_object_or_404(Student,rf_code=code)
    return redirect(viewstudent,student.id)

def dashboard(r):
    data={}
    data['student_count']=Student.objects.filter(isApproved=True).count()
    data['addmission_count']=Student.objects.filter(isApproved=False).count()
    data['payment_count']=Payment.objects.all().count()
    return render(r,'admin/dashboard.html',data)   

       