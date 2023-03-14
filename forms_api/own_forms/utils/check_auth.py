def authorization(request):
    print(request.COOKIES.get("jwt"))