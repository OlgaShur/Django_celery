from django.contrib.auth.models import User
from django.forms import ModelForm
from allauth.socialaccount.forms import SignupForm
from django.contrib.auth.models import Group


class UpdateProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class SocialSignupForm(SignupForm):

    def save(self, request):
        user = super(SocialSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
