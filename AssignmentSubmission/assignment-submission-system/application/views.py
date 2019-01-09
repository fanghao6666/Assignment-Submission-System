from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import SolutionForm, UserProfileForm, UserForm,AssignmentForm,SolCreditForm
from .models import Assignment, Solution, UserProfile,Course
import datetime
from django.shortcuts import redirect,reverse

# Create your views here.
def index(request):
	if not request.user.is_authenticated:
		return render(request, 'application/index.html')
	else:
		return redirect('application:profile')

def detail(request, assign_id):
	if not request.user.is_authenticated:
		return render(request, 'application/index.html', {'error_message': "You must be logged in!!"})
	else:
		user = request.user
		assign = get_object_or_404(Assignment, pk=assign_id)
		return render(request, 'application/details.html', {'assignment': assign, 'user': user,'course':assign.course.name})

def detail_t(request, assign_id):
	if not request.user.is_authenticated:
		return render(request, 'application/index.html', {'error_message': "You must be logged in!!"})
	else:
		user = request.user
		assign = get_object_or_404(Assignment, pk=assign_id)
		sol_set=Solution.objects.filter(assignment__id=assign_id)

		return render(request, 'application/details_t.html', {'assignment': assign,'sol_set':sol_set, 'user': user,'course':assign.course.name})

def sol_detail_t(request,sol_id):
	if not request.user.is_authenticated:
		return render(request, 'application/index.html', {'error_message': "You must be logged in!!"})
	else:
		sol=get_object_or_404(Solution,pk=sol_id)
		if request.method=='POST':

			stt=request.POST['comments']
			sol.comments=stt
			sol.points=request.POST['points']
			sol.save()
			return redirect('application:profile_t', course=sol.assignment.course)


		return render(request,'application/sol_details_t.html',{'sol':sol})




def profile(request,course):
	if not request.user.is_authenticated:
		return render(request, 'application/index.html')
	else:

		usr_profile = UserProfile.objects.get(user=request.user)
		usr_assign = Assignment.objects.filter(year=usr_profile.year,course__name=course)
		now=datetime.date.today()
		dead = []
		idx=[]
		asset = []
		cut = 1
		while True:
			usr_assign = Assignment.objects.filter(year=usr_profile.year,course__name=course,
												   num=cut)
			if len(usr_assign) == 0:
				break
			else:
				idx.append(cut)
				if usr_assign[0].deadline<now:
					dead.append(0)
				else:
					dead.append(1)

				asset.append(usr_assign)
				cut = cut + 1
		usr_soln = Solution.objects.filter(student=usr_profile)
		asset.reverse()
		dead.reverse()
		idx.reverse()

		return render(request, 'application/profile.html', {
			'asset': zip(asset,dead,idx),
			'solutions': usr_soln,
			'course':course,
		})

def profile_t(request,course):
	if not request.user.is_authenticated:
		return render(request, 'application/index.html')
	else:

		usr_profile = UserProfile.objects.get(user=request.user)
		now=datetime.date.today()
		idx=[]
		dead=[]
		asset=[]
		cut=1
		while True:

			usr_assign = Assignment.objects.filter(year=usr_profile.year, course__name=course, teacher=usr_profile, num=cut)
			if len(usr_assign)==0:
				break
			else:
				idx.append(cut)
				if usr_assign[0].deadline<now:
					dead.append(0)
				else:
					dead.append(1)
				asset.append(usr_assign)
				cut=cut+1
		asset.reverse()
		dead.reverse()
		idx.reverse()
		return render(request, 'application/profile_t.html', {
			'asset': zip(asset,dead,idx),
			'course':course,
		})



def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/application/')

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		identity=request.POST['identity']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				# usr_year = UserProfile.objects.get(user=request.user).year
				# usr_assign = Assignment.objects.filter(year=year)
				# rno = UserProfile.objects.get(user=request.user).roll_no
				user_profile=UserProfile.objects.get(user=user,identity=identity)
				if user_profile is not None:
					if identity=='student':
						return redirect('application:s_courses')
					else:
						return redirect('application:t_courses')

			else:
				return render(request, 'application/index.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'application/index.html', {'error_message': 'Invalid login'})
	return render(request, 'application/index.html')

def s_courses(request):
	user_profile=UserProfile.objects.get(user=request.user)
	if user_profile is None:
		return render(request, 'application/index.html')
	else:
		courses=user_profile.courses
		course_list=courses.split('-')
		if course_list is not None:
			return render(request,'application/courses.html',{'course_list':course_list})


def t_courses(request):
	user_profile=UserProfile.objects.get(user=request.user)
	if user_profile is None:
		return render(request, 'application/index.html')
	else:
		courses=user_profile.courses
		course_list=courses.split('-')
		if course_list is not None:
			return render(request,'application/courses_t.html',{'course_list':course_list})

def register(request):
	# context = RequestContext(request)
	if request.user.is_authenticated:
		return render(request, 'application/profile.html', {'error_message':"You are already registered!!"})
	else:
		user_form = UserForm(request.POST or None)
		profile_form = UserProfileForm(request.POST or None)
		registered = False
		if request.method == 'POST':
			if user_form.is_valid() and profile_form.is_valid():
				user = user_form.save(commit=False)
				username = user_form.cleaned_data['username']
				password = user_form.cleaned_data['password']
				user.set_password(user.password)
				user.save()
				profile = profile_form.save(commit=False)
				profile.user = user
				profile.save()
				registered = True
				user = authenticate(username=username, password=password)
				if user is not None:
					if user.is_active:
						login(request, user)
						return redirect('application:profile')

		context = {
			"pform": profile_form,
			"uform": user_form,
		}
		return render(request, 'application/register.html', context)


def submit(request,assignment_id):
	if not request.user.is_authenticated:
		return render(request, 'application/index.html')
	else:
		assignment=Assignment.objects.get(id=assignment_id)
		if request.method == 'POST':

			print(request.POST['title'])
			form = SolutionForm(user=request.user,course=assignment.course, data=request.POST)
			if form.is_valid():
				solution = form.save(commit=False)
				solution.student = UserProfile.objects.get(user=request.user)
				solution.assignment=assignment

				pre_sol=Solution.objects.filter(assignment__id=assignment_id,student=solution.student).all()
				pre_sol.delete()
				solution.save()

				return redirect('application:profile',course=assignment.course)

		else:
			print("###########")
			# print(request.user)
			# usr_year = UserProfile.objects.get(user=request.user).year
			# usr_assign = Assignment.objects.filter(year=usr_year)
			form = SolutionForm(user=request.user,course=assignment.course)
		return render(request, 'application/sol_submit.html', {'form': form,'course':assignment.course})

def add_t(request,course):
	if not request.user.is_authenticated:
		return render(request, 'application/index.html')
	else:
		if request.method == 'POST':
			form = AssignmentForm(data=request.POST)
			if form.is_valid():
				ass = form.save(commit=False)
				course=Course.objects.get(name=course)
				ass.teacher = UserProfile.objects.get(user=request.user)
				ass.course=course
				ass.save()

				return redirect('application:profile_t',course=course)

		else:
			print("###########")
			# print(request.user)
			# usr_year = UserProfile.objects.get(user=request.user).year
			# usr_assign = Assignment.objects.filter(year=usr_year)
			form = AssignmentForm()
		return render(request, 'application/add_t.html', {'form': form,'course':course})

