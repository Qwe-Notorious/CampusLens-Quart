from quart import Blueprint, render_template, request, redirect, url_for
from quart_auth import login_user, current_user, logout_user
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from CampusLens.models import Media, Base
import os

admin_blp = Blueprint("admin", __name__, template_folder='templates')

DATABASE_URL = "sqlite+aiosqlite:///media.db"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@admin_blp.before_app_serving
async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@admin_blp.route("/admin")
async def admin():
    return await render_template("admin.html")


@admin_blp.route("/mediaDB")
async def mediaDB():
    async with SessionLocal() as session1:
        # Получаем все записи Media, отсортированные по timestamp
        media_requests = await session1.execute(select(Media).order_by(Media.timestamp.desc()))
        medias = media_requests.scalars().all()
    return await render_template("mediaDB.html", medias=medias)


