"""habits routs processing module"""
from fastapi import APIRouter, Depends

from typing import Annotated, Dict, Any, List

from app.database.transactions import (
    delete_habit_db,
    get_list_habit_by_telegram_id_db,
    create_habit_db,
    fulfilling_habit_db,
    patch_habit_db,
)
from app.schemas.habits_sch import CreateHabitSchemas, DeleteHabitSchemas, ListHabitsSchemas, FulfilHabitSchemas, HabitSchemas, PatchHabitSchemas
from app.schemas.users_sch import InfoUserSchemas

from app.utils.depends import get_current_active_user


router = APIRouter(prefix="/habits", tags=["habits"])

DEF_HABIT = {
    "id": 0,
    "name_habit": "name_habit",
    "description": "description",
    "alert_time": "00:00:00",
    "count": 0
}


@router.get(
    path="/",
    response_description="habits_sch.ListHabitsSchemas",
    response_model=ListHabitsSchemas,
    response_model_exclude_unset=True,
    status_code=200
)
async def get_habits(
    current_user: Annotated[InfoUserSchemas, Depends(get_current_active_user)]) -> dict[str, list[Any]]:
    res = await get_list_habit_by_telegram_id_db(current_user.id)
    return {"habits": [habit[0].to_json() for habit in res]}


@router.post(
    path="/",
    response_description="habits_sch.Habit",
    response_model=HabitSchemas,
    status_code=201
)
async def create_habit(
        current_user: Annotated[InfoUserSchemas, Depends(get_current_active_user)],
        data: CreateHabitSchemas
) -> dict:
    """ """
    data = data.model_dump()
    data.update({"user_id": current_user.id})
    data["alert_time"] = data["alert_time"].replace(second=0, microsecond=0)
    habit = await create_habit_db(data)
    return habit.to_json()


@router.delete(path="/<int:habit_id>", status_code=204)
async def delete_habit(
        current_user: Annotated[InfoUserSchemas, Depends(get_current_active_user)],
        habit_id: int,
) -> None:
    """the function deletes the habit"""
    await delete_habit_db(current_user.id, habit_id)


@router.patch(path="/<int:habit_id>",
              response_description="habits_sch.HabitSchemas",
              response_model=HabitSchemas,
              status_code=201)
async def patch_habit(
        current_user: Annotated[InfoUserSchemas, Depends(get_current_active_user)],
        habit_id: int,
        data: PatchHabitSchemas
) -> dict[str, int | str] | bool:
    """the function updates the habit"""
    dict_data = data.model_dump()
    if dict_data.get("alert_time"):
        dict_data["alert_time"] = dict_data["alert_time"].replace(second=0, microsecond=0)
    res = await patch_habit_db(current_user.id, habit_id, dict_data)
    if not res:
        return DEF_HABIT
    return res


@router.post(
    path="/fulfilling/<int:habit_id>",
    response_description="habits_sch.FulfilHabitSchemas",
    response_model=HabitSchemas,
    status_code=201
)
async def fulfilling_habit(
        current_user : Annotated[InfoUserSchemas,
        Depends(get_current_active_user)],
        habit_id: int,
) -> dict[Any, Any] | bool:
    """the function fulfilling a habit"""
    res = await fulfilling_habit_db(current_user.id, habit_id)
    if not res:
        return DEF_HABIT
    return res.to_json()