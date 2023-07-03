from women.models import Women


def favorite_posts(request):
    user = request.user

    return {
        'favorite_posts': Women.objects.filter(favorited_by=user) if user.is_authenticated else [],
    }
