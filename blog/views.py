from django.shortcuts import render, redirect
from .forms import InputForm
import requests
import json as m_json


def crate_wall(request):
    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data['group_name']
            count = form.cleaned_data['count']
            form = InputForm()
            url = 'https://api.vk.com/method/wall.get?access_token=3856c68f3856c68f3856c68fda3825f7e5338563856c68f674ad39233c85c27cef2b46a&owner_id=-{}&v=5.131&count={}'.format(data, count)
            r = requests.get(url)
            json = r.json()
            count_from_form = json['response']['count']
            list_data = []
            for item in json['response']['items']:
                info_for_stat = m_json.dumps(item)
                list_data.append({'id': item['id'], 'owner_id': data, 'hash': item['hash'], 'info': info_for_stat})

            return render(request, 'blog/posts.html', {'form': form, 'data': list_data, 'count': count_from_form})
    else:
        form = InputForm()
    return render(request, 'blog/wall.html', {'form': form})


def show_stat(request):
    if request.method == 'POST':
        # data_str = request.POST['post_info'].replace("\'", "\"")
        data = m_json.loads(request.POST['post_info'])
        return render(request, 'blog/stat.html', {'data': data})
    else:
        return redirect('main')
