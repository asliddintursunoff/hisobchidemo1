from django.shortcuts import render,HttpResponse,redirect
from .forms import *
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from .decorators import *
from .models import *
import json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Value
from django.db.models.functions import Concat
from calendar import month_name
from django.db.models import Sum,F,Q,When,Case
from .extra import *
from django.core.serializers.json import DjangoJSONEncoder
from datetime import date
from datetime import datetime
from .to_excel import *
now = datetime.now()

@admin_or_worker
def homepage(request):
    return render(request,"index.html")


@is_user_authenticated
def register(request):
    
   
    companyForm = CompanyForm()
    userCreationForm = UserCreation()
    workerCreationForm = UserCreationWorker() 
    CompanyCode = CompanyID()
    workerform= WorkerForm()
    if request.method=="POST":
        user_type = request.POST.get("user_type")
        if user_type == "admin":
            companyForm = CompanyForm(request.POST)
            userCreationForm = UserCreation(request.POST)
           
            
            if companyForm.is_valid() and userCreationForm.is_valid():
                company = companyForm.save()          
                user =  userCreationForm.save(commit=False)
                user.company = company
                user.save()
                group = Group.objects.get(name = "admin")
                user.groups.add(group) 
                username = userCreationForm.cleaned_data["username"]
                password = userCreationForm.cleaned_data["password1"]
                check = authenticate(request,username =username , password = password )
    
                if check is not None:
                    login(request,check)
                    return redirect("adminpage")
                else:
                    return HttpResponse("something went wrong")
                
        elif user_type == "worker":   #it is for workers
            workerCreationForm = UserCreationWorker(request.POST) 
            CompanyCode = CompanyID(request.POST)
            workerform= WorkerForm(request.POST)
            if workerCreationForm.is_valid() and CompanyCode.is_valid() and workerform.is_valid():   
                company_id = CompanyCode.cleaned_data["code"]
                id = Company.objects.get(unique_id = company_id)
            
                if id is not None:        
                    worker =  workerCreationForm.save(commit=False)
                    worker.company = id
                    worker.save()
                    group = Group.objects.get(name = "worker")
                    worker.groups.add(group)
                    worker_name = workerform.cleaned_data["name"]
                    worker_family = workerform.cleaned_data["last_name"]
                    Worker.objects.create(user = worker,name = worker_name,last_name = worker_family,company = id )
                   
                    username1 = workerCreationForm.cleaned_data["username"]
                    password1 = workerCreationForm.cleaned_data["password1"]
                    checking = authenticate(request,username =username1 , password = password1 )
                    if checking is not None:
                        login(request,checking)
                        return HttpResponse("registerde")
                    else:
                        return HttpResponse("something went wrong")
                else:
                    return HttpResponse("error code")
            else:
                print("workerCreationForm Errors:", workerCreationForm.errors)
                print("CompanyCode Errors:", CompanyCode.errors)
                print("workerform Errors:", workerform.errors)

                return HttpResponse("not valid")
            
            
            
    context = {
        "companyForm":companyForm,
        "userCreationForm": userCreationForm,
        "worker":workerCreationForm,
        "company": CompanyCode, 
        "workerform":workerform,       
    }
    return render(request, "register.html",context)


@is_user_authenticated
def userlogin(request):
    if request.method=="POST":
       
        username123 = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username = username123,password=password)
        if user is not None:
            login(request, user)
            gr = user.groups.first()
      
            if gr and gr.name == "admin":
                return redirect("adminpage")
            elif gr and gr.name == "worker":
                return redirect("homepage")
            else:
                messages.info(request, "You do not have permission to access this system.")
                return redirect("login")
        else:
            messages.info(request,"Username or Password is incorrect")
    return render(request, "login.html")


def userlogout(request):
    logout(request)
    return redirect("homepage")



@allowed_pages("admin")
def adminpagedates(request):
    
    company= request.user.company
    date_list = []
    dates = DateforProgress.objects.filter(company = company)
    date_list = [{"date": date , "types": Progresstype.objects.filter(date = date) ,"month":date.date.month,"year":date.date.year} for date in dates  ]
 
    context = {
        "dates":date_list
    }
    return render(request, "admin/adminpagedate.html", context)


def adminpagedates_add_date(request):
    company = request.user.company
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            year = data.get("year")
            month = data.get("month")
            copy_date_id = data.get("copy_value_id")
            print("🙏",copy_date_id)
            new_type = data.get("productname")
            date_form = date(year=year,month=month,day=1)
            d = DateforProgress.objects.create(date = date_form,company=company)
            if new_type is not None:
                pro1=Progresstype.objects.create(date = d,type = new_type)
            
            if copy_date_id is not None:
                date_data = DateforProgress.objects.get(id = copy_date_id)
                types = Progresstype.objects.filter(date = date_data)
                for type1 in types:
                    
                    a_type = Progresstype.objects.create(type = type1.type,date = d) 
                
                    for progress in Progress.objects.filter(work__types = type1):
                        
                        try:
                            is_exist = Work.objects.get(work_name = progress.work.work_name,company=company,price = progress.work.price,types = a_type)
                        except Work.DoesNotExist:
                            is_exist=None
                        if is_exist is not None:
                            work = Work.objects.get(work_name = progress.work.work_name,company=company,price = progress.work.price,types = a_type) 
                        else:
                            work = Work.objects.create(work_name = progress.work.work_name,company=company,price = progress.work.price,types = a_type )
                        print("💕")
                        p = Progress.objects.create(worker = progress.worker,work = work,updated_at = d)
                        print("💕1")
                        ProgressItem.objects.create(progress = p,number = 0,date = date_form)
                        print("💕2")
                return  JsonResponse({"success":True})
                
                       
                
            return JsonResponse({"succes":True})
        except Exception as e:
            return JsonResponse({"succes":False,"error":str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})
        
        
@allowed_pages("admin")
@csrf_exempt
def adminpagedates_delete_full(request,pk):
    element = get_object_or_404(DateforProgress,id = pk)
    if  request.method == "DELETE":
        element.delete()
        return JsonResponse({"success": True, "worker_id": pk})
    return JsonResponse({"error": "Invalid request"}, status=400)
        
    
def adminpage(request,year,month,typeid):  
    company = request.user.company
    
    worker = Worker.objects.filter(company = company)
    types = Progresstype.objects.filter(
        Q(date__date__year = year) ,
        Q(date__date__month = month),
        date__company = company,)
    t = types.get(id = typeid)
    works = Work.objects.filter(company = company,types = t)
    progress_filtered = Progress.objects.filter(
        Q(items__date__year = year) ,
        Q(items__date__month = month),
        worker__company = company,
        work__types = t,
        
        )
    progress = progress_filtered.annotate(
        total_work_done = Sum("items__number")
    )
    works1 = progress_filtered.values("work__id", "work__work_name", "work__price").distinct()
    worker1 = progress_filtered.values("worker__id", "worker__name", "worker__last_name").distinct()
    name_of_month=int_to_month_string_uz(month)
    #calculating total work done
    sum_info = calculating_total_sum(worker,progress,ProgressItem)
    works_json = json.dumps([{"id": w.id, "name": w.work_name, "price": w.price} for w in works])
    #calculating total work
    total_work = total_work_number(works=works,progress=progress)
    #total_money
    total_sum = total_sum_money(sum_info)
    
    
    context = {

        "progress":progress,
        "year":year,
        "month_name":month,
        "sum_info":sum_info,
        "types":types,
        "t":t,
        "name_of_month":name_of_month,
        "works1":works1,
        "worker1":worker1,
        "works":works,
        "works_json": works_json,
        "total_work":total_work,
        "total_sum":total_sum
        
    }    
    return render(request, "admin/adminindex.html",context)

def admin_add_work(request):
    company = request.user.company
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            work_name = data.get("work_name")
            price = data.get("price")
            product_id = data.get("types")
          
            product = Progresstype.objects.get(id = product_id)
            if not isinstance(price,int):
                return JsonResponse({"success": False, "error": "Narx son qiymatida emas!"})
            Work.objects.create(types=product,company=company,work_name=work_name,price=price)
            return JsonResponse({"success":True,"new_work_name":work_name,"new_price":price})
        except Exception as e:
            return JsonResponse({"success":False,"error":str(e)})
        
    return JsonResponse({"success": False, "error": "Invalid request"})
        

@csrf_exempt  
def admin_create_worker(request):
    if request.method == "POST":
        name = request.POST.get("name")
        last_name = request.POST.get("last_name")
        work_ids = request.POST.getlist("work")  
        company = request.user.company
        worker = Worker.objects.create(company = company,name=name, last_name=last_name)
        year = int(request.POST.get("year1"))
        month = int(request.POST.get("month1"))

        vaqt = datetime(year=year, month=month, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
        for work_id in work_ids:
            work = Work.objects.get(id=work_id)
            pro = Progress.objects.create(worker=worker, work=work,updated_at = vaqt)
            ProgressItem.objects.create(progress = pro,number = 0,date=vaqt)

        return JsonResponse({"message": "Worker and Progress objects created!"}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)

def admin_createtype(request):
    company = request.user.company
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            type_name = data.get("type_name")
            items_id = data.get("type_id")
            
            type_d = data.get("type_date")
            
            
            type_date = Progresstype.objects.get(id = type_d).date
            
            year3 = type_date.date.year
            month3= type_date.date.month
            exact_date = datetime(year=year3, month=month3, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
            progress_type = Progresstype.objects.create(date = type_date,type = type_name)
            
            if  items_id  != "None":
                a_type = Progresstype.objects.get(id = items_id)
                
                for progress in Progress.objects.filter(work__types = a_type):
                    try:
                        is_exist = Work.objects.get(work_name = progress.work.work_name,company=company,price = progress.work.price,types = progress_type)
                    except Work.DoesNotExist:
                        is_exist=None
                    if is_exist is not None:
                        work = Work.objects.get(work_name = progress.work.work_name,company=company,price = progress.work.price,types = progress_type) 
                    else:
                        work = Work.objects.create(work_name = progress.work.work_name,company=company,price = progress.work.price,types = progress_type )
                   
                    p = Progress.objects.create(worker = progress.worker,work = work,updated_at = exact_date)
                    ProgressItem.objects.create(progress = p,number = 0,date = exact_date)
                return  JsonResponse({"message": "Yangi mahsulot turi qo'shildi!"}, status=201)
            return  JsonResponse({"message": "Yangi mahsulot turi qo'shildi!"}, status=201)
            
            
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"message": "send POST request not GET"}) 
        
  
@csrf_protect  
@require_POST
def progressitemadd(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            progress_id = data.get("progress_id")
            progress_value = data.get("progress_value")
            year2 = int(data.get("year2"))
            month2 = int(data.get("month2"))
            d = datetime(year=year2, month=month2, day=now.day, hour=now.hour, minute=now.minute, second=now.second)
            if not isinstance(progress_value, int):
                return JsonResponse({"success": False, "error": "Invalid input. Must be an integer!"})

            progress = Progress.objects.get(id=progress_id)
            progress_item = ProgressItem.objects.create(progress = progress , number = progress_value,date = d)
            
            return JsonResponse({"success": True, "new_value": progress_item.number})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})

def showworkers(request):
    company = request.user.company
    workers = Worker.objects.filter(company = company)
    context = {
        "workers":workers
    }
    return render(request,"admin/showworkers.html",context)
def add_worker(request):
    pass
def delete_worker(request,pk):
   
    if request.method == "DELETE":
        worker = get_object_or_404(Worker , id = pk)
        worker.delete()
        return JsonResponse({"success": True, "worker_id": pk})
    return JsonResponse({"error": "Invalid request"}, status=400)
    
def update_worker(request):
    pass

def add_work(request):
    pass
def delete_work(request):
    pass
def update_work(request):
    pass


def history(request):
    company = request.user.company
    progress1 = ProgressItem.objects.filter(progress__work__company = company,progress__worker__company = company)
    progress = progress1.annotate(
        sum_of_work = F("number")*F("progress__work__price")
    )
   
    context = {
        "history":progress,
       
    }
    return render(request,"admin/history.html",context)


def delete_history(request ,pk):
    progressitem = get_object_or_404(ProgressItem,id = pk)
    if request.method == "DELETE":
        progressitem.delete()
        return JsonResponse({"success": True, "progress_id": pk})
    return JsonResponse({"error": "Invalid request"}, status=400)

def change_history(request,pk):
    progressitem = get_object_or_404(ProgressItem,id = pk)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            number = data.get("number")
            date = data.get("date")
           
            
            if not isinstance(number, int):
                return JsonResponse({"success": False, "error": "Invalid input. Must be an integer!"})
            progressitem.number = number
            progressitem.date = date
            
            progressitem.save()
            return JsonResponse({"success": True, "new_number": progressitem.number,"new_date":progressitem.date,})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})

       