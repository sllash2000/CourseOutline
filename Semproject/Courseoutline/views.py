from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render ,get_list_or_404
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.views.generic import *
from django.views.generic.edit import *
from .forms import *
from datetime import datetime
from django.urls import reverse_lazy

# Create your views here.

def IndexMenu(request,template_name='Courseoutline/index.html'):
    return render(request,'Courseoutline/index.html')

#### CURICULUM


def CurriculumCreate(request,template_name='Courseoutline/curriculum_Detail.html'):
    curriculumForm = CreateCurriculumForm()
    currentcurriculum = Curriculum.objects.all()
    if request.method == 'POST':
        curriculumForm = CreateCurriculumForm(request.POST)
        if curriculumForm.is_valid():
            curriculumForm.save()
        return redirect('indexmenu')
    context = {'curriculumForm': curriculumForm,'title':'Curriculum','currentcurriculum':currentcurriculum}
    return render(request,'Courseoutline/curriculum_Detail.html',context)


def CurriculumDelete(request,curriculum_id):
    obj = get_object_or_404(Curriculum,pk=curriculum_id)
    if request.method == "POST":
        obj.delete()
        return redirect('indexmenu')
    return render(request,'curriculum_Detail.html')

class CurriculumUpdate(UpdateView):
    model = Curriculum
    form_class = CreateCurriculumForm
    template_name = 'Courseoutline/curriculum_Detail.html'

    def get_object(self):
        CurriculumID = self.kwargs.get("id")
        return get_object_or_404(Curriculum, pk=CurriculumID)
    def get_success_url(self):
        return reverse_lazy('indexmenu')


#### COURSEOUTLINE
def CourseoutlineCreate(request,template_name='courseoutline/courseOutlineSection.html'):
    courseoutlineForm = CreateCourseOutlineForm()
    courseoutlines = CourseOutline.objects.all()

    if request.method == 'POST':
        courseoutlineForm = CreateCourseOutlineForm(request.POST)
        if courseoutlineForm.is_valid():
            new_courseoutline=courseoutlineForm.save()
        return HttpResponseRedirect(reverse(Courseoutlinesectionscreate, args=(new_courseoutline.pk,)))
    context = {'courseoutlineForm': courseoutlineForm,'title':'Course Outline','courseoutlines':courseoutlines}
    return render(request,'Courseoutline/courseOutlineSection.html',context)

def CourseoutlineView(request,courseoutline_id, tempalte_name = 'Courseoutline/courseOutlineView.html'):
    CourseOutline = get_object_or_404(CourseOutline,pk=courseoutline_id)
    Section1 = CourseOutlineSection1.objects.filter(CourseOutlineID=courseoutline_id).first()
    Section2 = CourseOutlineSection2.objects.filter(CourseOutlineID=courseoutline_id).first()
    Section3 = CourseOutlineSection3.objects.filter(CourseOutlineID=courseoutline_id).first()
    # Section4 = CourseOutlineSection1.list.filter(CourseOutlineID=courseoutline_id).first()
    # Section5 = CourseOutlineSection2.list.filter(CourseOutlineID=courseoutline_id).first()
    # Section6 = CourseOutlineSection3.list.filter(CourseOutlineID=courseoutline_id).first()

    context = {'CourseOutline' : CourseOutline,'Section1':Section1,'Section2' : Section2,'Section3' : Section3,
    # 'Section4' : Section4,'Section5' : Section5,'Section6' : Section6,
    }
    return render(request,'Courseoutline/courseOutlineView.html',context)


def CourseoutlineDelete(request,courseoutline_id):
    obj = get_object_or_404(CourseOutline,pk=courseoutline_id)
    if request.method == "POST":
        obj.delete()
        return redirect('indexmenu')
    return render(request,'courseOutlineSection.html')

class CourseoutlineUpdate(UpdateView):
    model = CourseOutline
    form_class = CreateCourseOutlineForm
    template_name = 'Courseoutline/courseOutlineSection.html'

    def get_object(self):
        CourseOutlineID = self.kwargs.get("id")
        return get_object_or_404(CourseOutline, pk=CourseOutlineID)
    def get_success_url(self):
        return reverse_lazy('indexmenu')


# Section Forms within 1 html page
def Courseoutlinesectionscreate(request,courseoutline_id,template_name='Courseoutline/courseOutlineSection1.html'):
    currentcourseoutlineobj = get_object_or_404(CourseOutline,pk = courseoutline_id)
    courseoutlineForm1 = CreateCourseOutlineForm1()
    courseoutlineForm2 = CreateCourseOutlineForm2()
    courseoutlineForm3 = CreateCourseOutlineForm3()

    if request.method == 'POST':
        courseoutlineForm1 = CreateCourseOutlineForm1(request.POST)
        courseoutlineForm2 = CreateCourseOutlineForm2(request.POST)
        courseoutlineForm3 = CreateCourseOutlineForm3(request.POST)
        if courseoutlineForm1.is_valid():
            tempcourseoutline = courseoutlineForm1.save(commit=False)
            tempcourseoutline.CourseOutlineID =currentcourseoutlineobj
            tempcourseoutline.save()
            if courseoutlineForm2.is_valid():
                tempcourseoutline = courseoutlineForm2.save(commit=False)
                tempcourseoutline.CourseOutlineID = currentcourseoutlineobj
                tempcourseoutline.save()
                if courseoutlineForm3.is_valid():
                    tempcourseoutline = courseoutlineForm3.save(commit=False)
                    tempcourseoutline.CourseOutlineID = currentcourseoutlineobj
                    tempcourseoutline.save()
        
                    return redirect('courseoutlinesection4create',currentcourseoutlineobj.CourseOutlineID)
    context = {'courseoutlineForm1': courseoutlineForm1,'courseoutlineForm2': courseoutlineForm2,'courseoutlineForm3': courseoutlineForm3,
    'currentcourseoutlineobj':currentcourseoutlineobj,'title':'Course Outline','Course':currentcourseoutlineobj.CourseName,'CourseID':currentcourseoutlineobj.CourseCode}
    return render(request,'Courseoutline/courseOutlineSection1.html',context)

def Courseoutlinesectionslist(request,courseoutline_id,tempalte_name = 'Courseoutline/availablesections.html'):
    courseoutline = get_object_or_404(CourseOutline,pk=courseoutline_id)
    section1 = CourseOutlineSection1.objects.filter(CourseOutlineID=courseoutline_id).first()
    section2 = CourseOutlineSection2.objects.filter(CourseOutlineID=courseoutline_id).first()
    section3 = CourseOutlineSection3.objects.filter(CourseOutlineID=courseoutline_id).first()

    context = {'courseoutline' : courseoutline,'section1':section1,'section2' : section2,'section3' : section3,}
    return render(request,'Courseoutline/availablesections.html',context)

class CourseoutlineSection1Update(UpdateView):
    model = CourseOutlineSection1
    form_class = CreateCourseOutlineForm1
    template_name = 'Courseoutline/availablesections.html'
    def get_object(self):
        SectionID = self.kwargs.get("id")
        object1 = get_object_or_404(CourseOutlineSection1, SectionID=SectionID)
        return object1
    def get_success_url(self):
        return reverse_lazy('courseoutlinesectionlist', args = (self.object.CourseOutlineID.CourseOutlineID,))

class CourseoutlineSection2Update(UpdateView):
    model = CourseOutlineSection2
    form_class = CreateCourseOutlineForm2
    template_name = 'Courseoutline/availablesections.html'
    def get_object(self):
        SectionID = self.kwargs.get("id")
        object1 = get_object_or_404(CourseOutlineSection2, SectionID=SectionID)
        return object1
    def get_success_url(self):
        return reverse_lazy('courseoutlinesectionlist', args = (self.object.CourseOutlineID.CourseOutlineID,))

class CourseoutlineSection3Update(UpdateView):
    model = CourseOutlineSection3
    form_class = CreateCourseOutlineForm3
    template_name = 'Courseoutline/availablesections.html'
    def get_object(self):
        SectionID = self.kwargs.get("id")
        object1 = get_object_or_404(CourseOutlineSection3, SectionID=SectionID)
        return object1
    def get_success_url(self):
        return reverse_lazy('courseoutlinesectionlist', args = (self.object.CourseOutlineID.CourseOutlineID,))

def CourseoutlineSection4Create(request,courseoutline_id,template_name='Courseoutline/courseOutlineSection4.html'):
    currentcourseoutlineobj = get_object_or_404(CourseOutline,pk = courseoutline_id)
    courseoutlineForm4 = CreateCourseOutlineForm4()
        
    if request.method == 'POST' and 'savemultiple' in request.POST :
        courseoutlineForm4 = CreateCourseOutlineForm4(request.POST)
        if courseoutlineForm4.is_valid():
                tempcourseoutline = courseoutlineForm4.save(commit=False)
                tempcourseoutline.CourseOutlineID =currentcourseoutlineobj
                tempcourseoutline.save()
                return redirect('courseoutlinesection4create',courseoutline_id)
    else:
        courseoutlineForm4 = CreateCourseOutlineForm4(request.POST)
        if courseoutlineForm4.is_valid():
                tempcourseoutline = courseoutlineForm4.save(commit=False)
                tempcourseoutline.CourseOutlineID =currentcourseoutlineobj
                tempcourseoutline.save()
                return redirect('indexmenu')
    context = {'courseoutlineForm4': courseoutlineForm4,'currentcourseoutlineobj':currentcourseoutlineobj,'title':'Course Topics','Course':currentcourseoutlineobj.CourseName,'CourseID':currentcourseoutlineobj.CourseCode}
    return render(request,'Courseoutline/courseOutlineSection4.html',context)