# 可以在模版中使用(需要在setting的template中注册),也可以在视图函数中使用(无需注册)
# 获取的是远程访问者的ip  :request.META['REMOTE_ADDR']

def base_pic_url(request):
    add = request.META['HTTP_HOST']  # 获取的是本站点的ip
    return {'base_pic_url': 'http://' + add + '/media/'}


def ip_address(request):
    return {'ip_address': request.META['REMOTE_ADDR']}  # 访问者的ip
