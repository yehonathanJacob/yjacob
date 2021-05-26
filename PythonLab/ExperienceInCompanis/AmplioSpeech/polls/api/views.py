from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db import IntegrityError

from api.models import Poll, Choice, Vote
from api.utils import success_response, failed_response, list_all_instances



# Create your views here.
def test_connection(request):
    return JsonResponse({'status':'success'})

def set_new_poll(request):
    title = request.GET.get("title", None)
    if title is None:
        response = failed_response('expected title value')
    else:
        try:
            poll = Poll(title=title)
            poll.save()
            response = success_response(poll_id=poll.poll_id)
        except Exception as e:
            response = failed_response(str(e))

    return JsonResponse(response)

def get_all_instances(request, model_name):
    instances = list_all_instances(model_name)
    response = success_response(instances=instances)
    return JsonResponse(response)


def set_new_choice(request, poll_id):
    description = request.GET.get("description", None)
    if description is None:
        response = failed_response('expected description value')
    else:
        try:
            choice = Choice(poll_id = poll_id, description = description)
            choice.save()
            response = success_response(choice_id=choice.choice_id)
        except Exception as e:
            response = failed_response(str(e))

    return JsonResponse(response)

def get_poll_options(request, poll_id):
    try:
        poll = Poll.objects.get(poll_id=poll_id)
        choices = Choice.objects.filter(poll=poll)
    except Exception as e:
        response = failed_response(str(e))
        return JsonResponse(response)

    data = {'poll': model_to_dict(poll), 'choices':[
        model_to_dict(choice)
        for choice in choices
    ]}
    response = success_response(**data)
    return JsonResponse(response)

def set_new_vote(request, poll_id, choice_id):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        vote = Vote(poll_id=poll_id, choice_id=choice_id, user=request.user, ip=ip)
        vote.save()
        response = success_response(vote_id=vote.vote_id)
    except IntegrityError as e:
        if 'UNIQUE constraint' in e.args[0]:
            response = failed_response(f"The user {request.user} has been already voted for this poll")
        else:
            response = failed_response(str(e))
    except Exception as e:
        response = failed_response(str(e))
    return JsonResponse(response)

def get_poll_results(request, poll_id):
    votes = Vote.objects.select_related('poll').select_related('choice').select_related('user').filter(poll_id=poll_id)
    choices = Choice.objects.filter(poll_id=poll_id)
    results = {
        choice.choice_id:{**model_to_dict(choice),'number_of_vote':0}
        for choice in choices
    }
    for vote in votes:
        choice_id = vote.choice_id
        results[choice_id]['number_of_vote'] = results[choice_id]['number_of_vote'] + 1

    response = success_response(results=list(results.values()))
    return JsonResponse(response)
