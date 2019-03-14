from io import BytesIO
from xhtml2pdf import pisa
from course.models import Course
from student.models import Student
from django.http import HttpResponse
from django.forms import modelformset_factory
from .models import MarkSheet, MarkSheetDetail
from django.template.loader import get_template
from django.shortcuts import render, redirect, reverse
from django.views.generic import (View, ListView, DetailView, CreateView)
from .forms import MarkSheetForm, MarkSheetDetailForm, CreateMarkSheetForm, SubjectForm


class MarkSheetListView(ListView):
    context_object_name = 'students'
    model = MarkSheet


class MarkSheetDetailView(DetailView):
    context_object_name='markSheet_detail'
    model = MarkSheet
    template_name = 'markSheet_details.html'


class MarkSheetCreateView(CreateView):
    model = MarkSheet
    template_name = 'result/markSheet_form.html'
    form_class = MarkSheetForm

    def get_success_url(self):
        return reverse('result:marksheet_detail', args=(self.object.id,))


# load courses so user can view them in dropdown - dependant field
def load_courses(request):
    student_id = request.GET.get('student')
    student_obj = Student.objects.get(registrationNo=student_id)
    courses = student_obj.course.order_by('title')
    return render(request, 'course_dropdown_list_options.html', {'courses': courses})


def edit_marksheet_detail(request,pk):
    MarkSheetDetailFormSet = modelformset_factory(MarkSheetDetail, form=MarkSheetDetailForm, extra=0)
    data = request.POST or None
    marksheet_obj = MarkSheet.objects.get(id=pk)
    formset = MarkSheetDetailFormSet(data=data, queryset=MarkSheetDetail.objects.filter(markSheet=marksheet_obj))
    if request.method == 'POST' and formset.is_valid():
        formset.save()
        total = 0
        for obj in marksheet_obj.detail.all():
            total = total + obj.obtained_marks
        marksheet_obj.final_marks = total
        marksheet_obj.save()
        return redirect('home')

    return render(request, 'result/markSheetDetail_form.html', {'formset': formset})


# creates pdf
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# report page view. There are two forms on this page.
class Report(View):
    template_name = "pdf_report_form.html"

    def get(self, request, *args, **kwargs):
        # GET method
        m_form = CreateMarkSheetForm()
        s_form = SubjectForm()
        context = {"m_form": m_form, "s_form":s_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # POST method
        m_form = CreateMarkSheetForm(request.POST)
        if m_form.is_valid():
            student = m_form.cleaned_data['student']
            course = m_form.cleaned_data['course']
            marksheet_object = MarkSheet.objects.filter(student=student).filter(course__title__contains=str(course)).first()
            pdf = render_to_pdf('pdf_result.html', {'data':marksheet_object})
            m_form = CreateMarkSheetForm()
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            s_form = SubjectForm(request.POST)
            if s_form.is_valid():
                name = s_form.cleaned_data['name']
                subjects_list = MarkSheetDetail.objects.filter(subject__iexact=str(name))
                return render(request, 'web_report.html', {'subjects_list': subjects_list})

        m_form = CreateMarkSheetForm()
        s_form = SubjectForm()
        context = {"m_form": m_form, "s_form":s_form}
        return render(request, self.template_name, context)
