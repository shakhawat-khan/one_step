from django.urls import path
from .views import EventListView,event_detail,EventCreateView,EventUpdateView,EventDeleteView,join_event

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('new/', EventCreateView, name='event-create'),
    path('<int:pk>/', event_detail, name='event-detail'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('join/', join_event, name='join_event'),
]