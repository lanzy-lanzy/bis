from django.urls import path
from .views import (
    home, dashboard,
    people_list, person_search, person_create, person_detail, person_update, person_delete,
    barangay_list, barangay_search, barangay_create, barangay_detail, barangay_update, barangay_delete,
    id_card_list, id_card_search, id_card_create, id_card_detail, id_card_update, id_card_delete, id_card_data, id_card_print,
    id_card_direct_print
)

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),

    # People/Residents URLs
    path('dashboard/people/', people_list, name='people'),
    path('dashboard/people/search/', person_search, name='person_search'),
    path('dashboard/people/create/', person_create, name='person_create'),
    path('dashboard/people/<uuid:pk>/', person_detail, name='person_detail'),
    path('dashboard/people/<uuid:pk>/update/', person_update, name='person_update'),
    path('dashboard/people/<uuid:pk>/delete/', person_delete, name='person_delete'),

    # Barangay URLs
    path('dashboard/barangays/', barangay_list, name='barangays'),
    path('dashboard/barangays/search/', barangay_search, name='barangay_search'),
    path('dashboard/barangays/create/', barangay_create, name='barangay_create'),
    path('dashboard/barangays/<int:pk>/', barangay_detail, name='barangay_detail'),
    path('dashboard/barangays/<int:pk>/update/', barangay_update, name='barangay_update'),
    path('dashboard/barangays/<int:pk>/delete/', barangay_delete, name='barangay_delete'),

    # ID Cards URLs
    path('dashboard/id-cards/', id_card_list, name='id_cards'),
    path('dashboard/id-cards/search/', id_card_search, name='id_card_search'),
    path('dashboard/id-cards/create/', id_card_create, name='id_card_create'),
    path('dashboard/id-cards/<int:pk>/', id_card_detail, name='id_card_detail'),
    path('dashboard/id-cards/<int:pk>/update/', id_card_update, name='id_card_update'),
    path('dashboard/id-cards/<int:pk>/delete/', id_card_delete, name='id_card_delete'),
    path('dashboard/id-cards/<int:pk>/data/', id_card_data, name='id_card_data'),
    path('dashboard/id-cards/<int:pk>/print/', id_card_print, name='id_card_print'),
    path('dashboard/id-cards/<int:pk>/direct-print/', id_card_direct_print, name='id_card_direct_print'),
]
