from fastapi import HTTPException
from sqlalchemy import select, delete, func, join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from models.favorite import Favorite
from models.news import News


# 判断新闻是否被收藏
async def is_news_favorite(db: AsyncSession, id, news_id):
    result = await db.execute(select(Favorite).where(Favorite.user_id == id, Favorite.news_id == news_id))
    return result.scalar_one_or_none() is not None


# 添加收藏
async def add_news_favorite(db: AsyncSession, id, news_id):
    result = await db.execute(select(Favorite).where(Favorite.user_id == id, Favorite.news_id == news_id))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="已经收藏过了呦")
    favorite = Favorite(user_id=id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


# 删除收藏
async def remove_news_favorite(db: AsyncSession, id, news_id):
    result = await db.execute(delete(Favorite).where(Favorite.user_id == id, Favorite.news_id == news_id))
    await db.commit()
    return result.rowcount > 0


# 获取收藏列表
async def get_favorite_list(db: AsyncSession, id, page, page_size):
    total_result = await db.execute(select(func.count()).where(Favorite.user_id == id))
    total = total_result.scalar_one()

    offset = (page - 1) * page_size
    list_query = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
                  .join(Favorite, Favorite.news_id == News.id)
                  .where(Favorite.user_id == id)
                  .order_by(Favorite.created_at.desc())
                  .offset(offset).limit(page_size))
    list_result = await db.execute(list_query)
    return list_result.all(), total


# 删除所有收藏
async def remove_all_favorites(db: AsyncSession, id):
    result = await db.execute(delete(Favorite).where(Favorite.user_id == id))
    return result.rowcount
