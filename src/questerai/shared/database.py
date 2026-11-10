from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from questerai.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)