from celery import Celery
from celery.schedules import crontab
from app.scraper import WebScraper, ToScrape
from app import models
from app.postgres_db import SessionLocal

from redbeat import RedBeatSchedulerEntry
from redbeat.schedules import rrule
from datetime import datetime


celery = Celery('tasks', broker='redis://localhost:6379')

celery.conf.broker_connection_retry_on_startup = True


@celery.task
def generate_posts(id):
    with SessionLocal() as db:
        webscraper = WebScraper(owner_id=id)
        # toscrape = ToScrape(user_id=user_data.id)
        webscraper.scrape()
        posts = webscraper.posts
        post_models = [models.Post(**newPost.dict()) for newPost in posts if newPost !=None]
        db.add_all(post_models)
        db.commit()



def create_autogenerated_posts(owner_id,topic):
    if topic == 'devices':
        scraper = WebScraper(owner_id)
    elif topic == 'books':
        scraper = ToScrape(owner_id)
    else:
        return 0
    scraper.scrape()
    posts = scraper.posts
    post_models = [models.Post(**newPost.dict()) for newPost in posts if newPost !=None]
    return post_models

@celery.task
def generate_daily_posts(user_id,topic):
    with SessionLocal() as db:
        autogenerated_posts = create_autogenerated_posts(user_id,topic)

        existing_posts = db.query(models.Post.title, models.Post.body).filter(
            models.Post.owner_id == user_id,
            models.Post.is_autogenerated == True
        ).all()

        existing_posts_set = set((title, body) for title, body in existing_posts)

        new_posts = [post for post in autogenerated_posts if (post.title, post.body) not in existing_posts_set]

        daily_posts = new_posts[:10]

        db.add_all(daily_posts)
        db.commit()

def add_or_update_periodic_task(user_id, topic):
    schedule_name = f'generate_daily_posts_{user_id}'

    try:
        current_entry = RedBeatSchedulerEntry.from_key("redbeat:"+ schedule_name,app=celery)
        current_entry.delete()
    except KeyError:
        current_entry = None

    if topic == None:
        return 0


    dt = datetime.utcnow()
    interval = rrule(freq='MINUTELY',interval=2, dtstart=dt)
    entry = RedBeatSchedulerEntry(schedule_name,'app.tasks.generate_daily_posts',interval, args=(user_id, topic), app=celery)
    entry.save()