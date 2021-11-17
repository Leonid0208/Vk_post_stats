from django import forms
import requests
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class InputForm(forms.Form):
    group_name = forms.CharField(max_length=150, required=True)
    count = forms.IntegerField()

    def clean_group_name(self):
        data = self.cleaned_data['group_name']
        url = 'https://api.vk.com/method/utils.resolveScreenName?access_token=3856c68f3856c68f3856c68fda3825f7e5338563856c68f674ad39233c85c27cef2b46a&screen_name={}&v=5.131'.format(data)
        r = requests.get(url)
        json = r.json()
        if len(json['response']) == 0:
            raise ValidationError(_('Invalid name - here is no group yet'))
        else:
            if json['response']['type'] != 'group':
                raise ValidationError(_('It is not a group'))
            else:
               return json['response']['object_id']

    def clean_count(self):
        count = self.cleaned_data['count']
        data = self.cleaned_data['group_name']
        url_group = 'https://api.vk.com/method/wall.get?access_token=3856c68f3856c68f3856c68fda3825f7e5338563856c68f674ad39233c85c27cef2b46a&owner_id=-{}&v=5.131&count={}'.format(data, count)
        r = requests.get(url_group)
        json_group = r.json()
        count_from_form = int(json_group['response']['count'])
        if count_from_form < count < 1:
            raise ValidationError(_('Not correct posts count'))
        else:
            return count
