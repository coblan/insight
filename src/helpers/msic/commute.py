# encoding=utf-8

def get_argment(request):
    if request.method=='POST':
        if request.POST.keys():
            args=request.POST
        else:
            args = json.loads( request.body)
    else:
        args=request.GET    
    return args