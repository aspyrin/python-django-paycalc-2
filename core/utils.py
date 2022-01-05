from django.contrib.auth import authenticate, login

class MyUtils:

    @staticmethod
    def cur_user(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        return user
