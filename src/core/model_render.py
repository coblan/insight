from django.shortcuts import render,Http404

def render_table(request,scope,name,temp):
    table_cls = scope.get(name)
    if table_cls:
        table = table_cls.parse_request(request)
        return render(request,temp,table.get_context())
    else:
        raise Http404()