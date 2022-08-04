from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Category, Post
from typing import Set


@receiver(m2m_changed, sender=Post.category.through)
def notify_category_update(action: str, instance: Post, reverse: bool,
                           pk_set: Set[int], model: Category,
                           **kwargs) -> None:
    if action != 'post_add' or reverse:
        return

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
