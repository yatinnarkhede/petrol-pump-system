from datetime import datetime
from dateutil.relativedelta import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html")

def owner_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        pump_name = request.POST['pump_name']
        address = request.POST['address']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "owner_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        owner = Owner.objects.create(user=user, phone=phone, pump_name=pump_name, address=address, image=image)
        user.save()
        owner.save()
        alert = True
        return render(request, "owner_registration.html", {'alert':alert})
    return render(request, "owner_registration.html")

def customer_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "customer_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        customer = Customer.objects.create(user=user, phone=phone, image=image)
        user.save()
        customer.save()
        alert = True
        return render(request, "customer_registration.html", {'alert':alert})
    return render(request, "customer_registration.html")

def owner_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a pump owner!!")
            else:
                t = Owner.objects.get(user_id=user.id)
                request.session['cid'] = t.id
                return redirect("/owner_profile")
        else:
            alert = True
            return render(request, "owner_login.html", {'alert':alert})
    return render(request, "owner_login.html")

def customer_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a customer!!")
            else:
                t = Customer.objects.get(user_id=user.id)
                request.session['cid'] = t.id
                return redirect("/customer_profile")
        else:
            alert = True
            return render(request, "customer_login.html", {'alert':alert})
    return render(request, "customer_login.html")

def employee_login(request):
    if request.method == "POST":
        emp_id = request.POST['emp_id']
        password = request.POST['password']

        e = Employee.objects.filter(emp_no=emp_id, password=password).values()
        if e is not None:
            request.session['emp_no'] = emp_id
            e = Employee.objects.get(emp_no = emp_id)
            request.session['first_name'] = e.first_name
            request.session['last_name'] = e.last_name
            request.session['owner_id'] = e.owner_id
            return render(request,"employee_profile.html", {"emp" : e})
        else:
            alert = True
            return render(request, "employee_login.html", {'alert':alert})
    return render(request, "employee_login.html")

@login_required(login_url = '/owner_login')
def owner_profile(request):
    return render(request, "owner_profile.html")

@login_required(login_url = '/customer_login')
def customer_profile(request):
    return render(request, "customer_profile.html")

def employee_profile(request):
    e = Employee.objects.get(emp_no=request.session['emp_no'])
    return render(request, "employee_profile.html", {"emp":e})

def Logout(request):
    logout(request)
    return redirect ("/")

@login_required(login_url = '/owner_login')
def owner_change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "owner_change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "owner_change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "owner_change_password.html")


@login_required(login_url = '/customer_login')
def customer_change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "customer_change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "customer_change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "customer_change_password.html")

def employee_change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            e = Employee.objects.get(emp_no=request.session['emp_no'])
            if e.password == current_password:
                e.password = new_password
                e.save()
                alert = True
                return render(request, "employee_change_password.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "employee_change_password.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "employee_change_password.html")

@login_required(login_url = '/owner_login')
def owner_edit_profile(request):
    owner = Owner.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        pump_name = request.POST['pump_name']
        address = request.POST['address']

        owner.user.email = email
        owner.phone = phone
        owner.pump_name = pump_name
        owner.address = address
        owner.user.save()
        owner.save()
        alert = True
        return render(request, "owner_edit_profile.html", {'alert':alert})
    return render(request, "owner_edit_profile.html")

@login_required(login_url = '/customer_login')
def customer_edit_profile(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == "POST":
        customer.user.first_name = request.POST['first_name']
        customer.user.last_name = request.POST['last_name']
        customer.user.email = request.POST['email']
        customer.phone = request.POST['phone']
        customer.user.save()
        customer.save()
        alert = True
        return render(request, "customer_edit_profile.html", {'alert':alert})
    return render(request, "customer_edit_profile.html")

@login_required(login_url = '/owner_login')
def add_employee(request):
    if request.method == "POST":
        eid = request.POST['eid']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        birth_date = request.POST['birth_date']
        hire_date = request.POST['hire_date']
        salary = request.POST['salary']
        password = request.POST['password']
        image = request.FILES['image']
        owner_id = request.POST['uid']

        e = Employee.objects.create(emp_no=eid, first_name=first_name, last_name=last_name, gender=gender, email=email, phone=phone, address=address, hire_date=hire_date, birth_date=birth_date, salary=salary, image=image, password=password, owner_id=owner_id)
        e.save()
        alert = True
        return render(request, "add_employee.html", {'alert':alert})
    return render(request, "add_employee.html")


def add_supplier(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        owner_id = request.POST['uid']
        s = Supplier.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, address=address, owner_id=owner_id)
        s.save()
        alert = True
        return render(request, "add_supplier.html", {'alert':alert})
    return render(request, "add_supplier.html")

def add_machine(request):
    if request.method == "POST":
        mid = request.POST['mid']
        type = request.POST['type']
        company = request.POST['company']
        desc = request.POST['desc']
        price = request.POST['price']
        owner_id = request.POST['uid']
        m = Machine.objects.create(machine_no=mid, machine_type=type, machine_company=company, machine_desc=desc, machine_price=price, owner_id=owner_id)
        m.save()
        alert = True
        return render(request, "add_machine.html", {'alert':alert})
    return render(request, "add_machine.html")

@login_required(login_url = '/owner_login')
def view_employees(request):
    employees = Employee.objects.filter(owner_id=request.session['cid']).values()
    return render(request, "view_employees.html", {'employees':employees})

@login_required(login_url = '/owner_login')
def view_machines(request):
    machines = Machine.objects.filter(owner_id=request.session['cid']).values()
    return render(request, "view_machines.html", {'machines':machines})

@login_required(login_url = '/owner_login')
def view_suppliers(request):
    suppliers = Supplier.objects.filter(owner_id=request.session['cid']).values()
    return render(request, "view_suppliers.html", {'suppliers':suppliers})

@login_required(login_url = '/owner_login')
def view_customers(request):
    customers = Customer.objects.all()
    return render(request, "view_customers.html", {'customers':customers})

@login_required(login_url = '/customer_login')
def view_all_pumps(request):
    owners = Owner.objects.all()
    return render(request, "view_all_pumps.html", {'owners':owners})

@login_required(login_url = '/customer_login')
def view_all_pumps_feedback(request):
    owners = Owner.objects.all()
    return render(request, "view_all_pumps_feedback.html", {'owners':owners})

@login_required(login_url = '/owner_login')
def delete_employee(request, myid):
    e = Employee.objects.filter(emp_no=myid)
    e.delete()
    return redirect("/view_employees")

@login_required(login_url = '/owner_login')
def edit_employee(request, myid):
    e = Employee.objects.get(emp_no=myid)
    if request.method == "POST":
        e.emp_no = request.POST['eid']
        e.first_name = request.POST['first_name']
        e.last_name = request.POST['last_name']
        e.gender = request.POST['gender']
        e.email = request.POST['email']
        e.phone = request.POST['phone']
        e.address = request.POST['address']
        e.birth_date = request.POST['birth_date']
        e.hire_date = request.POST['hire_date']
        e.salary = request.POST['salary']
        e.password = request.POST['password']
        if 'image' in request.FILES:
            e.image = request.FILES['image']
        e.save()

        alert = True
        return render(request, "edit_employee.html", {'alert':alert})
    return render(request, "edit_employee.html", {'emp':e})

@login_required(login_url = '/owner_login')
def view_employee_details(request, myid):
    e = Employee.objects.get(emp_no=myid)
    return render(request, "view_employee_details.html", {'emp':e})

@login_required(login_url = '/owner_login')
def view_supplier_details(request, myid):
    s = Supplier.objects.get(id=myid)
    return render(request, "view_supplier_details.html", {'supplier':s})

@login_required(login_url = '/owner_login')
def view_machine_details(request, myid):
    m = Machine.objects.get(machine_no=myid)
    return render(request, "view_machine_details.html", {'machine':m})

@login_required(login_url = '/owner_login')
def view_customer_details(request, myid):
    c = Customer.objects.get(id=myid)
    return render(request, "view_customer_details.html", {'customer':c})

def employee_edit_profile(request):
    e = Employee.objects.get(emp_no=request.session['emp_no'])
    if request.method == "POST":
        e.emp_no = request.POST['eid']
        e.first_name = request.POST['first_name']
        e.last_name = request.POST['last_name']
        e.gender = request.POST['gender']
        e.email = request.POST['email']
        e.phone = request.POST['phone']
        e.address = request.POST['address']
        e.birth_date = request.POST['birth_date']
        e.hire_date = request.POST['hire_date']
        e.salary = request.POST['salary']
        e.password = request.POST['password']
        if 'image' in request.FILES:
            e.image = request.FILES['image']
        e.save()

        alert = True
        return render(request, "employee_edit_profile.html", {'alert':alert})
    return render(request, "employee_edit_profile.html", {'emp':e})

def view_all_suppliers(request):
    suppliers = Supplier.objects.filter(owner_id=request.session['owner_id']).values()
    return render(request, "view_all_suppliers.html", {'suppliers':suppliers})

def view_all_machines(request):
    machines = Machine.objects.filter(owner_id=request.session['owner_id']).values()
    return render(request, "view_all_machines.html", {'machines':machines})

def delete_employee_machine(request, myid):
    m = Machine.objects.filter(machine_no=myid)
    m.delete()
    return redirect("/view_all_machines")

def view_employee_machine_details(request, myid):
    m = Machine.objects.get(machine_no=myid)
    return render(request, "view_employee_machine_details.html", {'machine':m})

def edit_employee_machine(request, myid):
    m = Machine.objects.get(machine_no=myid)
    if request.method == "POST":
        m.machine_no = request.POST['mid']
        m.machine_type = request.POST['type']
        m.machine_company = request.POST['company']
        m.machine_desc = request.POST['desc']
        m.machine_price = request.POST['price']
        m.owner_id = request.POST['uid']
        m.save()

        alert = True
        return render(request, "edit_employee_machine.html", {'alert':alert})
    return render(request, "edit_employee_machine.html", {'machine':m})

def view_employee_supplier_details(request, myid):
    s = Supplier.objects.get(id=myid)
    return render(request, "view_employee_supplier_details.html", {'supplier':s})

def delete_employee_supplier(request, myid):
    s = Supplier.objects.filter(id=myid)
    s.delete()
    return redirect("/view_all_suppliers")

def edit_employee_supplier(request, myid):
    s = Supplier.objects.get(id=myid)
    if request.method == "POST":
        s.id = request.POST['sid']
        s.first_name = request.POST['first_name']
        s.last_name = request.POST['last_name']
        s.address = request.POST['address']
        s.phone = request.POST['phone']
        s.email = request.POST['email']
        s.owner_id = request.POST['uid']
        s.save()

        alert = True
        return render(request, "edit_employee_supplier.html", {'alert':alert})
    return render(request, "edit_employee_supplier.html", {'supplier':s})


@login_required(login_url = '/owner_login')
def add_booking_details(request, myid):
    if request.method == "POST":
        owner_id = request.POST['uid']
        slot_date = request.POST['slot_date']
        slot_time = request.POST['slot_time']
        slot_type = request.POST['slot_type']
        s = Slot.objects.create(slot_date=slot_date, slot_time=slot_time, slot_type=slot_type,owner_id=owner_id, customer_id = request.session['cid'])
        s.save()
        alert = True
        return render(request, "add_booking_details.html", {'alert':alert})
    return render(request, "add_booking_details.html", {'uid': myid})

@login_required(login_url = '/customer_login')
def view_all_slots(request):
    slots = Slot.objects.select_related('owner').filter(customer_id=request.session['cid'])
    return render(request, "view_all_slots.html", {'slots':slots})

@login_required(login_url = '/owner_login')
def add_feedback(request, myid):
    if request.method == "POST":
        owner_id = request.POST['uid']
        feedback_message = request.POST['feedback_message']
        f = Feedback.objects.create(feedback_message=feedback_message, owner_id=owner_id, customer_id = request.session['cid'])
        f.save()
        alert = True
        return render(request, "add_feedback.html", {'alert':alert})
    return render(request, "add_feedback.html", {'uid': myid})

@login_required(login_url = '/owner_login')
def add_puc(request, myid):
    if request.method == "POST":
        owner_id = request.POST['uid']
        vehicle_no = request.POST['vehicle_no']
        p = PUC.objects.create(vehicle_no=vehicle_no, owner_id=owner_id, customer_id = request.session['cid'])
        p.save()
        alert = True
        return render(request, "add_puc.html", {'alert':alert})
    return render(request, "add_puc.html", {'uid': myid})

@login_required(login_url = '/customer_login')
def view_all_puc(request):
    pucs = PUC.objects.select_related('owner').filter(customer_id=request.session['cid'])
    return render(request, "view_all_puc.html", {'pucs':pucs})

@login_required(login_url = '/owner_login')
def view_feedbacks(request):
    feedbacks = Feedback.objects.select_related('customer').filter(owner_id=request.session['cid'])
    return render(request, "view_feedbacks.html", {'feedbacks':feedbacks})

@login_required(login_url = '/owner_login')
def delete_feedback(request, myid):
    f = Feedback.objects.filter(id=myid)
    f.delete()
    return redirect("/view_feedbacks")

@login_required(login_url = '/owner_login')
def view_pucs(request):
    pucs = PUC.objects.select_related('customer').filter(owner_id=request.user.id)
    return render(request, "view_pucs.html", {'pucs':pucs})


@login_required(login_url = '/owner_login')
def generate_puc(request, myid):
    if request.method == "POST":
        id = request.POST['id']
        p = PUC.objects.get(id=id)
        p.date_of_issue = datetime.now()
        p.date_of_expiry = datetime.now() + relativedelta(months=+6)
        p.carbon_monoxide = request.POST['carbon_monoxide']
        p.hydro_carbon = request.POST['hydro_carbon']
        p.methane_hc = request.POST['methane_hc']
        p.reactive_hc = request.POST['reactive_hc']
        p.charges = request.POST['charges']
        p.status = 'Issued'
        p.save()
        alert = True
        return render(request, "generate_puc.html", {'alert':alert})
    return render(request, "generate_puc.html", {'id': myid})

@login_required(login_url = '/customer_login')
def view_puc(request, myid):
    p = PUC.objects.select_related('customer', 'owner').get(id=myid)
    return render(request, "view_puc.html", {'p':p})

def view_employee_bookings(request):
    slots = Slot.objects.select_related('customer').filter(owner_id=request.session['owner_id'])
    return render(request, "view_employee_bookings.html", {'slots':slots})

def accept(request, myid):
    s = Slot.objects.get(id=myid)
    s.status = 'Accepted'
    s.save()
    return redirect("/view_employee_bookings")

def reject(request, myid):
    s = Slot.objects.get(id=myid)
    s.status = 'Rejected'
    s.save()
    return redirect("/view_employee_bookings")
