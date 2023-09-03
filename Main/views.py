from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import models
from datetime import datetime
from django.http import JsonResponse		# To send JSON object

# This packages used to generate PDF
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
##

#To fetch system datetime
date = datetime.now().date()

def index(request):
	return redirect('faculty_login')
	##

def home(request):
	# If user user is logged in
	if request.user.is_authenticated:
		user = request.user												# Get logged in user
		faculty = models.faculty.objects.get(user=user)					# Get faculty obj
		sub = models.subject.objects.get(faculty=faculty)				# Get subject of logged in faculty
		all_stud = models.student.objects.all().order_by('roll_no')		# Fetch all students
		all_att = models.attendance.objects.filter(date=date).filter(subject=sub)	# Fetch all today's attendance of current subject

		# To store student id and attendance
		stud_att={}
		for i in all_att:
			stud_att[i.student.id]=int(i.is_present)
		
		# Context data passed to html page for display purpose
		context = {
			'today_date':date,
			'students':all_stud,
			'faculty':faculty,
			'attendance':stud_att,
			'subject':sub
		}
		return render(request,'Home.html',context)
	return redirect('faculty_login')
	##

# To fetch total presence of students
def total_presence(request):
	if request.user.is_authenticated:
		# Get logged in user, faculty and subject
		user = request.user
		faculty = models.faculty.objects.get(user=user)
		sub = models.subject.objects.get(faculty=faculty)
		# Count today's total presence of students
		total_pre = models.attendance.objects.filter(date=date, subject=sub, is_present=1).count()
		# Data stored in session
		request.session['total_presence'] = total_pre
		return redirect('home')
	return redirect('faculty_login')
	##

def faculty_login(request):
	# If cookie has variable uname then, get username and password from cookies
	# if request.COOKIES.get('uname'):
	# 	uname = request.COOKIES.get('uname')
	# 	passw = request.COOKIES.get('pass')

	# 	return render(request,'Faculty_login.html', {"uname":uname, "pass":passw})
	return render(request,'Faculty_login.html')
	##

# When submit login form this function is called
def post_login(request):
	if request.method=="POST":
		# Fetch required data from the login form
		uname = request.POST.get('uname')
		passw = request.POST.get('pass')
		rem_me = request.POST.get('remember')

		try:
			# If credentials are matched then, allowed to login
			auth_user = authenticate(username=uname, password=passw)
			u = User.objects.get(username=uname)
			faculty = models.faculty.objects.get(user=u)
			login(request, u)
		except:
			# Otherwise display alert message
			message = "Invalid username or password !!!"
			return render(request, 'Faculty_login.html', {'msg': message})

		response = redirect('home')
		# Store username and password in cookies if remember me is on
		if rem_me=="on":
			response.set_cookie("uname", uname)
			response.set_cookie("pass", passw)
		return response
	return redirect('faculty_login')
	##

def faculty_register(request):
	# Fetch all subjects
	all_sub = models.subject.objects.all()
	return render(request,'Faculty_registration.html', {'subjects':all_sub})
	##

def post_register(request):
	if request.method=="POST":
		# Fetch required data from the registration form
		name = request.POST['name']
		uname = request.POST['uname']
		email = request.POST['email']
		passw = request.POST['pass1']
		sub = request.POST.getlist('subject')       # to fetch multiple values from control

		# Create new user
		user = User.objects.create_user(uname, email, passw)
		user.save()

		# Create new faculty user
		new_user = models.faculty()
		new_user.fac_name = name
		new_user.email = email
		new_user.user = user
		new_user.save()

		# Fetch all selected subjects from database and assigned to faculty
		for s in sub:
			subject = models.subject.objects.get(id=int(s))
			subject.faculty = new_user
			subject.save()

	return redirect('faculty_login')
	##

def add_student(request):
	# If user user is logged in then open add student page otherwise, redirect to login page
	if request.user.is_authenticated:
		return render(request,'Add_student.html',{'today_date':date})
	else:
		return redirect('faculty_login')
	##

def post_add_student(request):
	if request.user.is_authenticated:
		if request.method=="POST":
			# Fetch required data from the form
			studid = request.POST['studid']
			rollno = request.POST['rollno']
			fullname = request.POST['fullname']
			email = request.POST['email']

			# Create new student
			new_stud = models.student()
			new_stud.stu_id = studid.upper()
			new_stud.roll_no = rollno
			new_stud.full_name = fullname
			new_stud.email = email
			new_stud.save()
		return redirect('add_student')
	return redirect('faculty_login')
	##

def faculty_logout(request):
	# If user is logged in, then logout and clear the session
	if request.user.is_authenticated:
		logout(request)
		request.session.clear()
	return redirect('faculty_login')
	##

def report(request):
	# If user is logged in, then open report page
	if request.user.is_authenticated:
		return render(request, "Reports.html", {'today_date':date})
	else:
		return redirect('faculty_login')
	##

def post_report(request):
	if request.user.is_authenticated:
		if request.method=="POST":
			# Fetch start date and end date from the form and
			# store in session to display in html page
			sdate = request.POST["startdate"]
			edate = request.POST["enddate"]

			request.session['sdate']=sdate
			request.session['edate']=edate

			# Fetch all students and all attendance between selected duration
			all_students = models.student.objects.all().order_by('roll_no')
			login_user = request.user
			login_fac = models.faculty.objects.get(user=login_user)
			sub = models.subject.objects.get(faculty=login_fac)
			attendance = models.attendance.objects.filter(date__gte=sdate, date__lte=edate, subject=sub)
			
			# Count total lectures between selected duration
			total_lecture = attendance.values('date').distinct().count()

			# Calculate total presents, absents and percentage
			total_present=[]
			total_absent=[]
			percent = []
			for stud in all_students:
				count_present = attendance.filter(student=stud, is_present=1).count()
				count_absent = attendance.filter(student=stud, is_present=0).count()
				total_present.append(count_present)
				total_absent.append(count_absent)
				if total_lecture > 0:
					percent.append((count_present/total_lecture)*100)
				else:
					percent.append(0.0)

			# Context data passed to html page for display purpose
			context = {
				"today_date":date,
				"records":zip(all_students, total_present, total_absent, percent),
				"total_lecture":total_lecture
			}
			return render(request, "Reports.html", context)
		return redirect('report')
	return redirect('faculty_login')
	##

# This function called by using AJAX
def attendance(request):
	if request.user.is_authenticated:
		# Fetch data from the form
		stud = models.student.objects.get(id=request.GET.get('stud_id'))
		sub = models.subject.objects.get(id=request.GET.get('sub_id'))

		try:
			# Update the attendance
			att_obj = models.attendance.objects.get(date=date, student=stud, subject=sub)
		except:
			# Create new obj of attendance
			att_obj = models.attendance()
			att_obj.date = date
			att_obj.subject = sub
			att_obj.student = stud

		if request.GET.get('is_present')=="1":
			att_obj.is_present = True
		else:
			att_obj.is_present = False

		att_obj.save()

		# Send success message to ajax function
		data={"success" : True}
		return JsonResponse(data)
	return redirect('faculty_login')
	##

def generate_report(request):
	# Fetch data from session
	sdate = request.session['sdate']
	edate = request.session['edate']

	# Fetch all students and all attendance between selected duration
	all_students = models.student.objects.all().order_by('roll_no')
	login_user = request.user
	login_fac = models.faculty.objects.get(user=login_user)
	sub = models.subject.objects.get(faculty=login_fac)
	attendance = models.attendance.objects.filter(date__gte=sdate, date__lte=edate, subject=sub)
	
	# Count total lectures between selected duration
	total_lecture = attendance.values('date').distinct().count()

	# Calculate total presents, absents and percentage
	total_present=[]
	total_absent=[]
	percent = []
	for stud in all_students:
		count_present = attendance.filter(student=stud, is_present=1).count()
		count_absent = attendance.filter(student=stud, is_present=0).count()
		total_present.append(count_present)
		total_absent.append(count_absent)
		if total_lecture > 0:
			percent.append((count_present/total_lecture)*100)
		else:
			percent.append(0.0)

	# Context data passed to html page for display purpose
	context = {
		"faculty" : login_fac.fac_name,
		"subject" : sub.sub_name,
		"today_date" : date,
		"records":zip(all_students, total_present, total_absent, percent),
		"total_lecture":total_lecture,
		"s_date" : sdate,
		"e_date" : edate
	}
	pdf = render_to_pdf('Attendence_report.html', context)
	return HttpResponse(pdf, content_type="application/pdf")
	##


# This function used to generate PDF
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
	##