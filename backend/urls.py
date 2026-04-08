from django.urls import path
from backend import views

urlpatterns = [
    # ── JSON REST API ────────────────────────────────────────────────────────
    path('fiestas', views.fiestas, name='api_fiestas'),
    path('invitados', views.invitados, name='api_invitados'),
    path('invitados/<int:invitado_id>/estado', views.invitado_estado, name='api_invitado_estado'),

    # ── Frontend Invitados (SSR) ─────────────────────────────────────────────
    path('invitados/', views.invitados_home, name='invitados_home'),
    path('invitados/fiesta/<int:fiesta_id>/', views.invitados_fiesta, name='invitados_fiesta'),

    # ── Frontend Localización (SSR) ──────────────────────────────────────────
    path('localizacion/', views.localizacion_home, name='localizacion_home'),
    path('localizacion/nueva/', views.localizacion_nueva, name='localizacion_nueva'),
]
