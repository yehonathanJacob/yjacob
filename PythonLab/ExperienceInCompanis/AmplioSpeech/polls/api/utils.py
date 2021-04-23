from django.apps import apps
from django.forms.models import model_to_dict

def success_response(**kwargs)->dict:
    return {
        'status': 'success',
        **kwargs
    }

def failed_response(error_message:str)->dict:
    return {
        'status': 'failed',
        'error': error_message
    }

def list_all_instances(model_name:str)->list:
    model = apps.get_model(f'api.{model_name}')
    return [
        model_to_dict(instance)
        for instance in model.objects.all()
    ]