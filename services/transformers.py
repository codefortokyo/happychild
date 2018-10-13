import datetime
from typing import List

from infrastructure.models import Nursery, Age
from infrastructure.consts import (
    NOT_ONE_AGE_ID,
    ONE_YEAR_OLD_AGE_ID,
    TWO_YEAR_OLD_AGE_ID,
    THREE_YEAR_OLD_AGE_ID,
    FOUR_YEAR_OLD_AGE_ID,
    EXTENT_AGE_ID
)
from services.forms.searches import SearchLocationForm, SearchTypeForm, SearchFeatureForm
from services.forms.admins import NurseryFreeNumForm
from services.entities import SearchNurseryEntity, NurseryFreeNumEntity


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


def transform_free_num_form_to_free_num(form: NurseryFreeNumForm, nursery_id: int) -> List[NurseryFreeNumEntity]:
    nursery = Nursery.objects.get(pk=nursery_id)
    modified_date = datetime.datetime.now().date()

    nursery_free_nums = []
    if 'free_num_not_one' in form.cleaned_data:
        nursery_free_nums.append(NurseryFreeNumEntity(
            nursery=nursery,
            age=Age.objects.get(pk=NOT_ONE_AGE_ID),
            free_num=form.cleaned_data['free_num_not_one'],
            modified_date=modified_date
        ))
    if 'free_num_one_year_old' in form.cleaned_data:
        nursery_free_nums.append(NurseryFreeNumEntity(
            nursery=nursery,
            age=Age.objects.get(pk=ONE_YEAR_OLD_AGE_ID),
            free_num=form.cleaned_data['free_num_one_year_old'],
            modified_date=modified_date
        ))
    if 'free_num_two_year_old' in form.cleaned_data:
        nursery_free_nums.append(NurseryFreeNumEntity(
            nursery=nursery,
            age=Age.objects.get(pk=TWO_YEAR_OLD_AGE_ID),
            free_num=form.cleaned_data['free_num_two_year_old'],
            modified_date=modified_date
        ))
    if 'free_num_three_year_old' in form.cleaned_data:
        nursery_free_nums.append(NurseryFreeNumEntity(
            nursery=nursery,
            age=Age.objects.get(pk=THREE_YEAR_OLD_AGE_ID),
            free_num=form.cleaned_data['free_num_three_year_old'],
            modified_date=modified_date
        ))
    if 'free_num_four_year_old' in form.cleaned_data:
        nursery_free_nums.append(NurseryFreeNumEntity(
            nursery=nursery,
            age=Age.objects.get(pk=FOUR_YEAR_OLD_AGE_ID),
            free_num=form.cleaned_data['free_num_four_year_old'],
            modified_date=modified_date
        ))
    if 'free_num_extent' in form.cleaned_data:
        nursery_free_nums.append(NurseryFreeNumEntity(
            nursery=nursery,
            age=Age.objects.get(pk=EXTENT_AGE_ID),
            free_num=form.cleaned_data['free_num_extent'],
            modified_date=modified_date
        ))
    return nursery_free_nums
