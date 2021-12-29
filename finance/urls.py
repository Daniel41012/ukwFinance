from rest_framework import routers
from finance import views
from django.urls import path, include




urlpatterns = [
    # path('api/',include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path("transactions/", views.transactionListView.as_view()),
    path("transaction/<int:pk>", views.transactionDetailView.as_view()),
    path("accounts/", views.userAccountListView.as_view()),
    path("account/<int:pk>", views.userAccountDetailView.as_view()),
]