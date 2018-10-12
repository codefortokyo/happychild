from services.forms.searches import SearchLocationForm, SearchTypeForm, SearchFeatureForm
from services.entities import SearchNurseryEntity


def transform_forms_to_search_nursery(location_form: SearchLocationForm, type_form: SearchTypeForm,
                                      feature_form: SearchFeatureForm) -> SearchNurseryEntity:
    return SearchNurseryEntity(
        city_id=location_form.cleaned_data.get('city'),
        ward_id=location_form.cleaned_data.get('ward'),
        station_id=location_form.cleaned_data.get('station'),
        latitude=location_form.cleaned_data.get('latitude'),
        longitude=location_form.cleaned_data.get('longitude'),
        age_id=type_form.cleaned_data.get('age'),
        license_id=type_form.cleaned_data.get('license'),
        school_type_id=type_form.cleaned_data.get('school_type'),
        is_opening=feature_form.cleaned_data.get('is_opening'),
        stable_food=feature_form.cleaned_data.get('stable_food'),
        temporary_childcare=feature_form.cleaned_data.get('temporary_childcare'),
        overnight_childcare=feature_form.cleaned_data.get('overnight_childcare'),
        allday_childcare=feature_form.cleaned_data.get('allday_childcare'),
        evaluation=feature_form.cleaned_data.get('evaludation')
    )
