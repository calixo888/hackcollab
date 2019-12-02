from . import models

def add_variable_to_context(request):
    hackathon_name = request.get_host().split(".")[0]

    # # Modifying team_id for each hackathon
    # profile = request.user.testhacks_profile
    # for hid in models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name):
    #     if models.TeamIdentification.objects.filter(team_id=hid.model_id, user_id=profile.id).exists():
    #         profile.team_id = models.TeamIdentification.objects.get(team_id=hid.model_id, user_id=profile.id).team_id
    #         profile.save()
    #     else:
    #         profile.team_id = None
    #         profile.save()

    try:
        # Getting current hackathon from subdomain
        hackathon = models.Hackathon.objects.get(name=hackathon_name)

        # # Seeing if user is in team
        # team = None
        # for hid in models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name):
        #     if models.TeamIdentification.objects.filter(team_id=hid.model_id, user_id=user_id).exists():
        #         tid = models.TeamIdentification.objects.get(team_id=hid.model_id, user_id=user_id)
        #         if models.HackathonIdentification.objects.filter(hackathon_name=hackathon_name, model_id=tid.team_id).exists():
        #             team = models.Team.objects.get(id=team_id)

        return {
            'hackathon': hackathon,
        }
    except:
        return {
            'hackathon': None
        }
