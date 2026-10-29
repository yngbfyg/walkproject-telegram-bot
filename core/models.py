"""Модели DTO для представления данных мест и данных сессии пользователя."""

from typing import Dict, List, Tuple

from pydantic import BaseModel, Field


class PlaceDTO(BaseModel):
    """DTO для описания места интереса."""

    name: str = Field(..., description="Название места")
    lat: float = Field(..., description="Широта")
    lon: float = Field(..., description="Долгота")
    category: str = Field(..., description="Категория (кафе, музей и т.д.)")
    price: float = Field(
        ..., ge=0, description="Средняя стоимость посещения, Руб"
    )
    tags: List[str] = Field(
        ..., description="Список тегов (indoor, outdoor и т.д.)"
    )
    avg_visit_time: int = Field(
        ..., ge=0, description="Среднее время визита в минутах"
    )
    weather: str = Field(
        ..., description="При какой погоде рекомендуется посещать"
    )
    work_time_dict: Dict[str, Tuple[str, str]] = Field(
        ..., description="Словарь времени работы по дням"
    )


class SessionData(BaseModel):
    """DTO для хранения данных сессии пользователя."""

    telegram_id: int = Field(..., description="ID пользователя в Telegram")
    location: Tuple[float, float] = Field(
        ..., description="Координаты (lat, lon)"
    )
    budget: int = Field(..., ge=0, description="Бюджет пользователя в €")
    max_time: int = Field(
        ..., ge=0, description="Желаемая длительность прогулки в минутах"
    )
