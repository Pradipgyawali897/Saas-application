from django.shortcuts import render,HttpResponse
def home_section_view(request,*args, **kwargs):
    user=request.user
    print('subscriptions.pro',user.has_perm('subscriptions.pro'))
    print('subscriptions.advanced',user.has_perm('subscriptions.advanced'))
    print('subscriptions.basic',user.has_perm('subscriptions.basic'))

    return render(request,'snippets/home.html')