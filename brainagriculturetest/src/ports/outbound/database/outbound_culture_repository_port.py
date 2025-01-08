from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from brainagriculturetest.src.ports.outbound.database.models import Culture

class OutboundCultureRepositoryPort:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_culture(self, culture_name: str) -> Culture:
        result = await self.session.execute(select(Culture).where(Culture.name == culture_name))
        culture = result.scalar_one_or_none()
        if not culture:
            culture = Culture(name=culture_name)
            self.session.add(culture)
            await self.session.commit()
            await self.session.refresh(culture)
        return culture