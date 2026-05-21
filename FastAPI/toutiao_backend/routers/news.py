"""
新闻模块控制器
"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from utils.result import Result
from crud import news, news_cache

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """
    获取新闻分类列表
    """
    categories = await news_cache.get_categories(db, skip, limit)
    return Result.success(categories)


@router.get("/list")
async def get_news_list(
        category_id: int = Query(..., alias="categoryId"),
        page: int = 1,
        page_size: int = Query(10, alias="pageSize", le=100),
        db: AsyncSession = Depends(get_db)
):
    """
    获取新闻列表
    """
    offset = (page - 1) * page_size
    news_list = await news_cache.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_count(db, category_id)
    has_more = (offset + len(news_list)) < total
    return Result.success({
        "list": news_list,
        "total": total,
        "hasMore": has_more
    })


@router.get("/detail")
async def get_news_detail(news_id: int = Query(..., alias="id"), db: AsyncSession = Depends(get_db)):
    """
    获取新闻详情
    """
    news_detail = await news_cache.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    await news.increase_news_views(db, news_detail.id)
    related_news = await news_cache.get_related_news(db, news_detail.id, news_detail.category_id)
    news_detail.__setattr__("relatedNews", related_news)
    return Result.success(news_detail)
