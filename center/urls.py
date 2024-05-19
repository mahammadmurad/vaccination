from django.urls import path
from center import views

app_name = 'center'

urlpatterns = [
    path("", views.center_list, name="list"),
    path("<int:pk>/", views.center_detail, name="detail"),
    path("create/", views.create_center, name="create"),
    path("update/<int:pk>/", views.update_center, name="update"),
    path("delete/<int:pk>/", views.delete_center, name="delete"),
    # Storage
    path("<int:center_id>/storage/", views.StorageList.as_view(), name="storage_list"),
    path("storage/<int:pk>/", views.StorageDetail.as_view(), name="storage_detail"),
    path(
        "<int:center_id>/storage/create/",
        views.StorageCreate.as_view(),
        name="storage_create",
    ),
    path(
        "storage/update/<int:pk>/", views.StorageUpdate.as_view(), name="storage_update"
    ),
    path(
        "storage/delete/<int:pk>/", views.StorageDelete.as_view(), name="storage_delete"
    ),
]
