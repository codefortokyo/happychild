from typing import Optional

from infrastructure.consts import (
    NURSERY_FREE_NUM_FMT,
    NOT_ONE_AGE_ID,
    ONE_YEAR_OLD_AGE_ID,
    TWO_YEAR_OLD_AGE_ID,
    THREE_YEAR_OLD_AGE_ID,
    FOUR_YEAR_OLD_AGE_ID,
    EXTENT_AGE_ID,
)
from infrastructure.models import Nursery, NurseryFreeNum, NurseryScore
from infrastructure.entities.nurseries import NurseryEntity


def get_nursery(nursery_id: int) -> Optional[NurseryEntity]:
    nursery = Nursery.get_nursery(nursery_id)
    if not nursery:
        return None

    free_nums = NurseryFreeNum.get_free_nums([nursery_id])
    last_updated_date = NurseryFreeNum.get_last_updated_date([nursery_id])

    scores = dict()
    year = 2018
    for age_id in [NOT_ONE_AGE_ID, ONE_YEAR_OLD_AGE_ID, TWO_YEAR_OLD_AGE_ID, THREE_YEAR_OLD_AGE_ID, FOUR_YEAR_OLD_AGE_ID, EXTENT_AGE_ID]:
        score = NurseryScore.get_last_year_score(nursery_id, age_id, year)
        if score:
            scores[age_id] = score.nursery_score
        else:
            scores[age_id] = '-'

    return NurseryEntity(
        id=nursery.id,
        license=nursery.license.name,
        school_type=nursery.school_type.name,
        name=nursery.name,
        postcode=nursery.postcode,
        address=nursery.address,
        station_info=nursery.station_info,
        url=nursery.url,
        image=nursery.thumbnail_url,
        latitude=float(nursery.latitude),
        longitude=float(nursery.longitude),
        open_time_weekday=nursery.default_open_time_weekday,
        open_time_saturday=nursery.open_time_saturday,
        accept_age=nursery.accept_age,
        stable_food=nursery.stable_food,
        temporary_childcare=nursery.temporary_childcare,
        overnight_childcare=nursery.overnight_childcare,
        allday_childcare=nursery.allday_childcare,
        evaluation=nursery.evaluation,
        organizer=nursery.organizer,
        event=nursery.default_event,
        service=nursery.default_service,
        policy=nursery.default_policy,
        promise=nursery.promise,
        free_num_url=nursery.free_num_url,
        free_num_url_title=nursery.free_num_url_title,
        free_num_not_one=free_nums.get(NURSERY_FREE_NUM_FMT.format(nursery.id, NOT_ONE_AGE_ID), '-'),
        free_num_one_year_old=free_nums.get(NURSERY_FREE_NUM_FMT.format(nursery.id, ONE_YEAR_OLD_AGE_ID), '-'),
        free_num_two_year_old=free_nums.get(NURSERY_FREE_NUM_FMT.format(nursery.id, TWO_YEAR_OLD_AGE_ID), '-'),
        free_num_three_year_old=free_nums.get(NURSERY_FREE_NUM_FMT.format(nursery.id, THREE_YEAR_OLD_AGE_ID), '-'),
        free_num_four_year_old=free_nums.get(NURSERY_FREE_NUM_FMT.format(nursery.id, FOUR_YEAR_OLD_AGE_ID), '-'),
        free_num_extent=free_nums.get(NURSERY_FREE_NUM_FMT.format(nursery.id, EXTENT_AGE_ID), '-'),
        free_num_updated_at=str(last_updated_date.get(nursery.id, '-')),
        score_not_one=scores[NOT_ONE_AGE_ID],
        score_one_year_old=scores[ONE_YEAR_OLD_AGE_ID],
        score_two_year_old=scores[TWO_YEAR_OLD_AGE_ID],
        score_three_year_old=scores[THREE_YEAR_OLD_AGE_ID],
        score_four_year_old=scores[FOUR_YEAR_OLD_AGE_ID],
        score_extent_year_old=scores[EXTENT_AGE_ID],
        score_updated_year=str(year),
    )
