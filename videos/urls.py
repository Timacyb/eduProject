from django.urls import path

from .views import videos_list, homePageView, ContactPageView, BlogPageView, AboutPageView, \
    NetworkSecurityView, OperationSystemSecurityView, CyberCriminalisticView, PentestingView, videos_detail, \
    QuizListView, QuizView, CoursesView, yangi_list, instrument_list, termin_list, kitob_list, quiz_results

urlpatterns = [
    path('all/', videos_list, name='all_videos_list'),
    path('<int:id>/', videos_detail, name='videos_detail_page'),
    path('', homePageView, name='home_page'),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    path('blog/', yangi_list, name='blog_page'),
    path('about/', AboutPageView.as_view(), name='about_page'),
    path('operation-system/', OperationSystemSecurityView.as_view(), name='operation_system_page'),
    path('network/', NetworkSecurityView.as_view(), name='network_page'),
    path('cyber-criminalistic/', CyberCriminalisticView.as_view(), name='cyber_criminalistic_page'),
    path('pentesting/', PentestingView.as_view(), name='pentesting_page'),
    path('quiz_list/', QuizListView.as_view(), name='quiz_list'),
    path('quiz/<int:quiz_id>/', QuizView.as_view(), name='quiz'),
    path('courses/', CoursesView.as_view(), name='cours_page'),
    path('instruments/', instrument_list, name="instrument_page"),
    path('termins/', termin_list, name="termin_list"),
    path('kitob/', kitob_list, name="kitoblar_page"),
    path('quiz/<int:quiz_id>/results/', quiz_results, name='quiz_results'),
]
