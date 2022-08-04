from celery import shared_task
import time
from django.core.mail import send_mail
from .models import Category, Post
from typing import Set


@shared_task
def sending_weekly_category(instance: Post, pk_set: Set[int], model: Category, **kwargs):
    users = {}
    url = f'http://localhost:8000{instance.get_absolute_url()}'

    for category_id in pk_set:
        category = model.objects.get(id=category_id)
        for user in category.subscribers.all():
            if user not in users:
                users[user] = set()
            users[user].add(category.name.title())
    print('sending mail', users)

    for user, categories in users.items():
        _categories = ', '.join(categories)
        send_mail(subject=f'Новая статья в разделе {_categories}',
                  message='\n'.join((f'Здравствуй, {user.username}',
                                    f'Новая статья в разделе {_categories}',
                                     url,
                                     *instance.description[:50].split('\n'))),
                  recipient_list=[user.email],
                  from_email=None)
