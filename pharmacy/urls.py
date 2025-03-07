from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import(
    create_item_view, 
    create_brand_view, 
    prescription_view, 
    search_drug_view, 
    view_prescription_view, 
    dispense_prescription_view,
    prescription_view1,
    dispensary_view,
    submit_dispensery_view
)


urlpatterns = [
    path("create_item/", create_item_view, name="create_item"),
    path("create_brand/", create_brand_view, name="create_brand"),
    path("prescription/<enc_id>", prescription_view, name="prescription"),
    path("prescription1/<enc_id>", prescription_view1, name="prescription1"),
    path("search_drug/", csrf_exempt(search_drug_view), name="search_drug_view"),
    path("view_prescription/<pid>", view_prescription_view, name="view_prescription"),
    path("dispense_prescription/<encounter_id>", dispense_prescription_view, name="dispense_prescription"),
    path("dispensary_item/submit/", submit_dispensery_view, name="submit_dispensary"),
    path("dispensary/<pid>/", dispensary_view, name="dispensary"),
]