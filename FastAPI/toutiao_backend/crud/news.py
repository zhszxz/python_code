"""
新闻相关CRUD
"""
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category, News


# 查询新闻分类列表
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()


# 查询新闻列表
async def get_news_list(db: AsyncSession, category_id, offset, page_size):
    result = await db.execute(select(News).where(News.category_id == category_id).offset(offset).limit(page_size))
    return result.scalars().all()


# 查询新闻数量
async def get_news_count(db: AsyncSession, category_id):
    result = await db.execute(select(func.count(News.id)).where(News.category_id == category_id))
    return result.scalar_one()


# 获取新闻详情
async def get_news_detail(db: AsyncSession, news_id):
    result = await db.execute(select(News).where(News.id == news_id))
    return result.scalar_one_or_none()


# 增加新闻浏览量
async def increase_news_views(db: AsyncSession, news_id):
    result = await db.execute(update(News).where(News.id == news_id).values(views=News.views + 1))
    await db.commit()
    return result.rowcount > 0


# 获取相关新闻
async def get_related_news(db: AsyncSession, news_id, category_id, limit=5):
    result = await db.execute(
        select(News)
        .where(News.id != news_id, News.category_id == category_id)
        .order_by(News.views.desc(), News.publish_time.desc())
        .limit(limit))
    return [{
        "id": related_news.id,
        "title": related_news.title,
        "content": related_news.content,
        "image": related_news.image,
        "author": related_news.author,
        "publishTime": related_news.publish_time,
        "categoryId": related_news.category_id,
        "views": related_news.views
    } for related_news in result.scalars().all()]
