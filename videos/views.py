from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Category, Quiz, Videos, Yangi, Instrument, Termin, Kitoblar, QuizResult
from django.views.generic import ListView, TemplateView, DetailView
from .forms import ContactForm
from django.utils.decorators import method_decorator


# Create your views here.


def videos_list(request):
    videos_list = Videos.objects.filter(status=Videos.Status.Published)
    context = {
        "videos_list": videos_list
    }

    return render(request, "videos/videos_list.html", context)


def homePageView(request):
    categories = Category.objects.all()
    videos_list = Videos.objects.filter(status=Videos.Status.Published).order_by('-publish_time')[:5]
    context = {
        'videos_list': videos_list,
        'categories': categories,
    }

    return render(request, 'videos/home.html', context)


class ContactPageView(TemplateView):
    template_name = 'videos/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'videos/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect("contact_page")
        context = {
            "form": form
        }
        return render(request, 'videos/contact.html', context)


class BlogPageView(TemplateView):
    template_name = 'videos/blog.html'


class AboutPageView(TemplateView):
    template_name = 'videos/error.html'


#     # Дополнительные методы, если нужно, можно также разместить в этом базовом классе
class BaseSubadminView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login_page')  # Задаем URL для перенаправления

    def test_func(self):
        user = self.request.user
        return user.is_active

    def handle_no_permission(self):
        if not self.request.user.is_active:
            return redirect(self.login_url)  # Перенаправление неактивного пользователя на login_page
        return super().handle_no_permission()


class NetworkSecurityView(BaseSubadminView):
    model = Videos
    template_name = 'videos/network_security.html'
    context_object_name = 'networksecurity'

    def get_queryset(self):
        return Videos.objects.filter(
            status=Videos.Status.Published,
            category__name='NetworkSecurity'
        )


class PentestingView(BaseSubadminView):
    model = Videos
    template_name = 'videos/pentesting.html'
    context_object_name = 'pentesting'

    def get_queryset(self):
        return Videos.objects.filter(
            status=Videos.Status.Published,
            category__name='Pentesting'
        )


class OperationSystemSecurityView(BaseSubadminView):
    model = Videos
    template_name = 'videos/operation_system_security.html'
    context_object_name = 'operationsystemsecurity'

    def get_queryset(self):
        return Videos.objects.filter(
            status=Videos.Status.Published,
            category__name='OperationSystem'
        )


class CyberCriminalisticView(BaseSubadminView):
    model = Videos
    template_name = 'videos/cyber_criminalistic.html'
    context_object_name = 'cybercriminalistic'

    def get_queryset(self):
        return Videos.objects.filter(
            status=Videos.Status.Published,
            category__name='CyberCriminal'
        )


# def videos_detail(request, id):
#     videos = get_object_or_404(Videos, id=id, status=Videos.Status.Published)
#
#     context = {
#         "videos": videos
#     }
#     return render(request, "videos/videos_detail.html", context)

# class VideoDetailView(BaseSubadminView, DetailView):
#     model = Videos
#     template_name = 'videos/videos_detail.html'
#     context_object_name = 'videos'
#
#     def get_queryset(self):
#         return Videos.objects.filter(
#             status=Videos.Status.Published,
#             category__name='CyberCriminal'
#         )

def videos_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('login_page')  # Перенаправление на страницу входа, если пользователь не авторизован

    if not request.user.is_active:
        return HttpResponseForbidden("Ваш аккаунт неактивен. Пожалуйста, свяжитесь с администратором.")

    videos = get_object_or_404(Videos, id=id, status=Videos.Status.Published)

    context = {
        "videos": videos
    }
    return render(request, "videos/videos_detail.html", context)


class QuizListView(View):
    def get(self, request):
        quizzes = Quiz.objects.all()
        return render(request, 'videos/quiz_list.html', {'quizzes': quizzes})


class QuizView(View):
    @method_decorator(login_required(login_url='login_page'))
    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        request.session['start_time'] = timezone.now().timestamp()
        return render(request, 'videos/quiz.html', {
            'quiz': quiz,
            'questions': questions,
            'time_limit': quiz.time_limit  # Берем время из базы
        })

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        questions = quiz.questions.all()
        score = 0
        total_questions = questions.count()

        start_time = request.session.get('start_time')
        elapsed_time = int(timezone.now().timestamp() - start_time)
        time_limit = quiz.time_limit  # Берем лимит времени из базы

        # Сообщение о статусе завершения теста
        if elapsed_time > time_limit:
            result_message = "Vaqt tugadi."
        else:
            result_message = "Test yakunlandi."

        # Подсчет правильных ответов
        for question in questions:
            selected_answer = request.POST.get(f"question_{question.id}")
            if selected_answer and int(selected_answer) == question.correct_answer:
                score += 1

        # Рассчет оценки в процентах
        grade = round((score / total_questions) * 100)

        # Сохранение результата
        QuizResult.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            grade=grade,
            time_spent=elapsed_time
        )

        return render(request, 'videos/result.html', {
            'score': score,
            'total': total_questions,
            'grade': grade,
            'message': result_message
        })


@staff_member_required
def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    results = QuizResult.objects.filter(quiz=quiz).select_related('user')

    return render(request, 'videos/quiz_results.html', {
        'quiz': quiz,
        'results': results
    })


class CoursesView(TemplateView):
    template_name = 'videos/courses.html'


def yangi_list(request):
    yangi_list = Yangi.objects.filter(status=Yangi.Status.Published)
    paginator = Paginator(yangi_list, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }
    return render(request, "videos/blog.html", context)


class InstrumentView(ListView):
    model = Instrument
    template_name = 'videos/instruments.html'


class TerminView(ListView):
    model = Termin
    template_name = 'videos/termins.html'


def instrument_list(request):
    instrument_list = Instrument.objects.all()
    context = {
        "instrument_list": instrument_list
    }

    return render(request, "videos/instruments.html", context)


def termin_list(request):
    termin_list = Termin.objects.all()
    paginator = Paginator(termin_list, 15)  # 15 терминов на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }
    return render(request, "videos/termins.html", context)


def kitob_list(request):
    kitob_list = Kitoblar.objects.filter(status=Kitoblar.Status.Published)

    # Создаём пагинатор на 10 элементов на странице
    paginator = Paginator(kitob_list, 10)

    # Получаем текущую страницу из GET-запроса (по умолчанию 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }
    return render(request, "videos/kitoblar.html", context)


def page_not_found(request, exception):
    return render(request, 'videos/404.html', status=404)


class SearchResultView(ListView):
    model = Termin
    template_name = 'videos/search_result.html'
    context_object_name = 'barcha_terminlar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Termin.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
