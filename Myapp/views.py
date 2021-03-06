from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Topic, Course, Student, Order
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .forms import InterestForm, OrderForm, LoginForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
import json
'''
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of tpoics: ' + '</p>'
    response.write(heading1)
    for topic in top_list:
        para = '<p>' + str(topic.id) + ': ' + str(topic) + '</p>'
        response.write(para)
    return response
'''

'''
#for Lab3
def index(request):
    courses_list = Course.objects.all().order_by('-price')[:5]
    response = HttpResponse()
    head = '<p>' + 'List of Courses: ' + '</p>'
    response.write(head)
    i = 1
    for course in courses_list:
        des = 'This Course is For Everyone!'
        if not course.for_everyone:
            des = 'This Course is Not For Everyone!'
        para = '<p>' + str(i) + '\t' + str(course.name) + '\t ' + str(course.price) + '\t' + des + '</p>'
        response.write(para)
        i = i + 1
    return response
'''
#for Lab4
def index(request):
    if 'last_login' not in request.session:
        return HttpResponse('Your last login was more than one hour ago')
    top_list = Topic.objects.all().order_by('id')[:10]
    last_login = request.session['last_login']
    # test 'None' top_list = None
#   return render(request, 'Myapp/index0.html', {'top_list': top_list})
    return render(request, 'Myapp/index.html', {'top_list': top_list, 'last_login': last_login})
'''
#for Lab3
def about(request):
    response = HttpResponse()
    response.write("<p> This is an E-learning website! </p> <p> Search our Topics to find all available Courses. </p>")

    return response
'''
#for Lab4
def about(request):
#    return render(request, 'Myapp/about0.html')
    ct = request.session.get('about_visits???', 0)
    request.session['about_visits???'] = ct+1
    #?????????????????????????????????????????????value????????????????????????????????????,???????????????????????????value??????????????????
    request.session.set_expiry(300)
    return render(request, 'Myapp/about.html', {'about_visits': ct})
#for lab4
def detail(request, top_on):
    topic = get_object_or_404(Topic, id=top_on)
    course_list = Course.objects.filter(topic__name=topic.name).order_by('-price')
    topic_ctgry = topic.get_category_display()
    #return render(request, 'Myapp/detail0.html', {'topic': topic, 'course_list': course_list, 'topic_ctgry':topic_ctgry})
    return render(request, 'Myapp/detail.html', {'topic': topic, 'course_list': course_list, 'topic_ctgry':topic_ctgry})


'''
#for lab3
def detail(request, top_on):
    try:
        tpc = Topic.objects.get(id=top_on)
    except Topic.DoesNotExist:
        raise Http404("No such model")
    response = HttpResponse()
    if not tpc:
        response.write("<p> On such a topic, please correct the input </p>")
        return response

    # ??? get_xxx_display()??????????????????????????????????????????
    #head = '<p>' + str(tpc.name) + 'The category of ' + str(tpc.name) + ' is ' + str(tpc.get_category_display()) + '</p>'
    head = '<p>' + 'Topic is : '+ str(tpc.name) + '</p>' + '<p>' + 'Category is : ' + str(tpc.get_category_display()) + '</p>'
    response.write(head)
    courses = Course.objects.filter(topic__name=tpc.name)
    for cos in courses:
        li = '<li>' + cos.name + '  ' + str(cos.price) + '</li>'
        response.write(li)
    return response
'''


'''
#for lab3
def detail(request, top_on):

    tpc = get_object_or_404(Topic, id=top_on)
    response = HttpResponse()

    # ??? get_xxx_display()??????????????????????????????????????????
    head = '<p>' + 'Topic is : '+ str(tpc.name) + '</p>' + '<p>' + 'Category is : ' + str(tpc.get_category_display()) + '</p>'
    response.write(head)
    courses = Course.objects.filter(topic__name=tpc.name)
    for cos in courses:
        li = '<li>' + cos.name + '  ' + str(cos.price) + '</li>'
        response.write(li)
    return response
'''

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'Myapp/courses.html', {'courlist': courlist})

def place_order(request):
    msg = ""
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                price = order.course.price
                if price >= 150:
                    order.order_price = order.course.discount()
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'Myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'Myapp/place_order.html', {'form': form, 'msg': msg, 'courlist': courlist})

#comments ???level?????????????????????????????????
def coursedetail(request, cour_id):
    cur = get_object_or_404(Course, id=cour_id)
    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            cur.interested = cur.interested+1
            cur.save()
            #????????????????????????????????????????????????????????????????????????????????????,??????????????????index
            return index(request)
            #return render(request, "Myapp/index.html")
    else: #include GET and others in case
        form = InterestForm()
    return render(request, 'Myapp/coursedetail.html', {'form': form, 'cur': cur})
'''
def coursedetail(request, cour_id):
    cur = get_object_or_404(Course, id=cour_id)
    return render(request, 'Myapp/coursedetail.html', { 'cur': cur})
'''
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            now = timezone.localtime(timezone.now())
            json_str = json.dumps({'created_at': now}, default=str)
            #session ???????????????????????????string??? ???????????????
            request.session['last_login'] = json_str
            # It is easier to test via setting 2 seconds
            request.session.set_expiry(3600)
            if user.is_active:
                login(request, user)
                # HttpResponseRedirect ?????????????????????URL???????????????reverse??????naming space?????????????????????HttpResponseRedirect
                return HttpResponseRedirect(reverse('Myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'Myapp/login.html', {'loginForm': LoginForm})

@login_required
def user_logout(request):
    del request.session['last_login']
    #logout(request)
    return HttpResponseRedirect(reverse('Myapp:index'))

@login_required
def myaccount(request):
    usr = request.user
    #???????????????????????????????????????student???????????????????????????username????????????????????????????????????????????????
    #Student ?????????????????????user????????????????????? python????????????????????????????????????
    if Student.objects.get(username=usr.username):
        ord_list = Order.objects.filter(student=usr)
        tpc_list = Topic.objects.filter(student=usr)
        cur_list = []
        for odr in ord_list:
            crs = odr.course.name
            if crs not in cur_list:
                cur_list.append(crs)
        return render(request, 'Myapp/myaccount.html', {'firstname': usr.first_name, 'lastName': usr.last_name,
                                                        'course_list': cur_list, 'topic_list': tpc_list})
    else:
        msg = 'You are not a registered student.'
        return render(request, 'Myapp/order_response.html', {'msg': msg})

def testCookie(request):
    if request.method == "GET":
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse("Cookie is active in you browser")
        else:
            request.session.set_test_cookie()
            return HttpResponse("Please enable cookies and try again")
    return render(request, 'Myapp/index.html')


def test(request):
    form = InterestForm()
    return render(request, 'Myapp/test.html', {'form': form})

