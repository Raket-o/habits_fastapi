"""books routs processing module"""
from fastapi import APIRouter, Depends

from typing import Annotated, Dict, Any

from app.database.transactions import (
    delete_habit_db,
    get_list_habit_by_telegram_id_db,
    create_habit_db,
    patch_habit_db,
)
from app.schemas.habits_sch import CreateHabitSchemas, DeleteHabitSchemas, ListBooksSchemas, HabitSchemas, PatchHabitSchemas
from app.schemas.users_sch import InfoUserSchemas

from app.utils.depends import get_current_active_user


router = APIRouter(prefix="/habits", tags=["habits"])


@router.get(
    path="/",
    response_description="habits_sch.ListBooksSchemas",
    response_model=ListBooksSchemas,
    response_model_exclude_unset=True,
    status_code=200
)
async def get_habits(
    current_user: Annotated[InfoUserSchemas, Depends(get_current_active_user)],
):
    res = await get_list_habit_by_telegram_id_db(current_user.id)
    return {"habits": [habit[0].to_json() for habit in res]}


@router.post(
    path="/",
    response_description="habits_sch.Habit",
    response_model=HabitSchemas,
    status_code=201
)
async def create_habit(current_user: Annotated[InfoUserSchemas, Depends(get_current_active_user)], data: CreateHabitSchemas) -> None:
    """ """
    data = data.model_dump()
    data.update({"user_id": current_user.id})
    data["alert_time"] = data["alert_time"].replace(second=0, microsecond=0)
    habit = await create_habit_db(data)
    return habit.to_json()


@router.delete(path="/<int:id_habit>", status_code=204)
async def delete_habit(
        _: Annotated[InfoUserSchemas,
        Depends(get_current_active_user)],
        id_habit: int,
):
    """the function deletes the habit"""
    await delete_habit_db(id_habit)


@router.patch(path="/<int:id_habit>",
              response_description="habits_sch.HabitSchemas",
              response_model=HabitSchemas,
              status_code=201)
async def patch_book(
        _: Annotated[InfoUserSchemas,
        Depends(get_current_active_user)],
        id_habit: int,
        data: PatchHabitSchemas) -> dict[Any, Any] | bool:
    """the function updates the habit"""
    dict_data = data.model_dump()
    dict_data["alert_time"] = dict_data["alert_time"].replace(second=0, microsecond=0)
    res = await patch_habit_db(id_habit, dict_data)
    if not res:
        return {**{'id': 0, "count": 0}, **dict_data}
    return res
