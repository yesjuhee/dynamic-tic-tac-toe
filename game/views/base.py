from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def change_player(player):
    if player == "X":
        return "O"
    else:
        return "X"
