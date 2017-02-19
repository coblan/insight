import json
from models import KVModel

def get_value(key,value=None):
    try:
        return json.loads( KVModel.objects.get(key=key).value)
    except KVModel.DoesNotExist:
        return value


def set_value(key,value):
    opt,_ = KVModel.objects.get_or_create(key=key)
    if not opt.value or json.loads(opt.value) != value:
        opt.value=json.dumps(value)
        opt.save()
        