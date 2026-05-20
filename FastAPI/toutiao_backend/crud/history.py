from datetime import datetime

from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


# 添加浏览历史
async def add_history(db: AsyncSession, id, news_id):
    result = await db.execute(select(History).where(History.user_id == id, History.news_id == news_id))
    history = result.scalar_one_or_none()
    if history:
        history.view_time = datetime.now()
        await db.commit()
        await db.refresh(history)
        return history
    else:
        history = History(user_id=id, news_id=news_id)
        db.add(history)
        await db.commit()
        await db.refresh(history)
        return history


# 查询浏览历史列表
async def get_history_list(db: AsyncSession, id, page, page_size):
    count_result = await db.execute(select(func.count(History.id)).where(History.user_id == id))
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    list_query = (select(News, History.view_time.label("view_time"), History.id.label("history_id"))
                  .join(History, History.news_id == News.id)
                  .where(History.user_id == id)
                  .order_by(History.view_time.desc())
                  .offset(offset).limit(page_size))
    list_result = await db.execute(list_query)

    return list_result.all(), total


# 删除浏览历史
async def delete_history(db: AsyncSession, id, news_id):
    result = await db.execute(delete(History).where(History.user_id == id, History.news_id == news_id))
    await db.commit()
    return result.rowcount > 0


# 清空浏览历史
async def clear_history(db: AsyncSession, id):
    result = await db.execute(delete(History).where(History.user_id == id))
    await db.commit()
    return result.rowcount
