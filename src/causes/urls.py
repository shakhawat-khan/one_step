from django.urls import path
from .views import CauseListView,CauseDetailView,CauseCreateView,CauseUpdateView,CauseDeleteView,causeDonate,causeByBudget

urlpatterns = [
    path('', CauseListView.as_view(), name='cause-list'),
    path('new/', CauseCreateView.as_view(), name='cause-create'),
    path('<int:pk>/', CauseDetailView.as_view(), name='cause-detail'),
    path('<int:pk>/update/', CauseUpdateView.as_view(), name='cause-update'),
    path('<int:pk>/delete/', CauseDeleteView.as_view(), name='cause-delete'),
    path('<int:pk>/donate/', causeDonate, name='cause-donate'),
    path('cause-by-budget', causeByBudget, name='cause-budget'),
]