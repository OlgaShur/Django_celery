import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import send_mail
from datetime import datetime, timedelta
from Django_HW.newsapp.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    emails = {}
    week_ago = datetime.now() - timedelta(days=7)
    url = 'https://localhost:8000'
    logger.info('starting job')

    for category in Category.objects.all():
        _category = category.name.title()
        news = Post.objects.filter(category=category,
                                       publication_date__gte=week_ago)
        logger.info(f'Нашли новые статьи в {category}\n{news}')
        if not news:
            continue
        for user in category.subscribers.all():
            if user not in emails:
                emails[user] = {}
            if _category not in emails[user]:
                emails[user][_category] = set()
            emails[user][_category].update(news)
    logger.info('sending mail', emails)

    for user, categories in emails.items():
        message = []
        for category, news in categories.items():
            message.extend((category, *(
                f'{post.name}: {url}/{post.get_absolute_url()}'
                for post in news)))
        send_mail('New articles of this week', '\n'.join(message), None,
                  [user.email])


# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
