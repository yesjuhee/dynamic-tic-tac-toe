from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def change_player():
    global current_player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"
