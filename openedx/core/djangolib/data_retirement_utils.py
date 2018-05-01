from oauth2_provider.models import AccessToken, Application, Grant, RefreshToken

def delete_user_from(model, user_id):
    user_query_results = model.objects.filter(user_id=user_id)

    if not user_query_results.exists():
        return False

    user_query_results.delete()
    return True

def delete_from_oauth2_provider_accesstoken(user):
    return delete_user_from(model=AccessToken, user_id=user.id)

def delete_from_oauth2_provider_application(user):
    return delete_user_from(model=Application, user_id=user.id)

def delete_from_oauth2_provider_grant(user):
    return delete_user_from(model=Grant, user_id=user.id)

def delete_from_oauth2_provider_refreshtoken(user):
    return delete_user_from(model=RefreshToken, user_id=user.id)
