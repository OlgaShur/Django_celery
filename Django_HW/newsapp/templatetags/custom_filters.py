from django import template

register = template.Library()

cencored_list = ['редиска', 'вонючка']
cencored_stars = []
for word in cencored_list:
    word = word.replace(word[1:], '*' * (len(word)-1))
    cencored_stars.append(word)

@register.filter()
def censor(text):
    for i in range(len(cencored_list)):
        text = text.lower().replace(cencored_list[i], cencored_stars[i])

    return text
