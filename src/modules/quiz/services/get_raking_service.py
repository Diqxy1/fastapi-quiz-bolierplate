from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.quiz.models import RankingResponseModel, RankingItemModel
from src.modules.users.repositories import UserRepository


class GetRankingService:
    def __init__(self, db: AsyncSession):
        self._db = db
        self._repo = UserRepository(db)

    async def execute(self, category_uuid: str = None) -> RankingResponseModel:
        if category_uuid:
            data = await self._repo.get_category_ranking(category_uuid)
            
            return RankingResponseModel(
                category_uuid=category_uuid,
                ranking=[RankingItemModel(username=row.username, score=row.score) for row in data]
            )
        
        data = await self._repo.get_general_ranking()
        
        return RankingResponseModel(
            ranking=[RankingItemModel(username=user.username, score=user.total_score) for user in data]
        )