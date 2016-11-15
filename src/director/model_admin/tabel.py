# encoding:utf8

from __future__ import unicode_literals

from core.db_tools import to_dict,model_to_head,model_stringfy
import json
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from permit import Permit
from director.db_tools import model_to_name
#from forms import MobilePageForm


from django.core.paginator import Paginator


class PageNum(object):
    def __init__(self,query,perPage=30,pageNumber=1):
        self.pagenator = Paginator(query,perPage)
        self.query = query
        self.pageNumber = int(pageNumber)
        self.perPage=perPage
    
    def get_rows(self):
        return self.pagenator.page(self.pageNumber)
    
    def get_choice(self):
        """
        rt: {'choice':[1,2,3,4,...,100],
             'crt_page':2
            }
        """
        choice_len = len(self.pagenator.page_range)
        k=3
        a=-1
        while a < 1:
            a=self.pageNumber-k
            k-=1
        page_nums = range(a,min(choice_len,self.pageNumber+(5-k))+1)
        if page_nums[0] != 1:
            page_nums=[1,'...']+ page_nums
        if page_nums[-1] != choice_len:
            page_nums = page_nums +['...',choice_len]
        for i in range(len(page_nums)):
            num = page_nums[i]
        page_nums=[str(x) for x in page_nums]
        return {'choice':page_nums,'crt_page':self.pageNumber}    
    
class SearchQuery(object):
    names=[]
    def __init__(self,dc,user,allowed_names):
        self.search_args={}
        for k in self.names:
            v = dc.pop(k,None)
            if v:
                self.search_args[k]=v
        
        self.crt_user=user
        self._names=[x for x in self.names if x in allowed_names]
            
    def get_context(self):
        return 
    
    def get_query(self,query):
        return query


  
class ModelTable(object):
    """
    
    Getter Method:
    ===============
    get_heads(self):
        return [{name:'xxx',label:'xxx',sortable:true}]
        
    get_rows(self):
        return [{}]
    

    over-load Method:
    =================
    inn_filter(self,query):
        process inn filter logic . Get gid of ,Ex: user-ware ,group-ware data.
        these data will be used for sort and filter in front-end
        
    """
    model=''
    sortable=[]
    include=[]
    perPage=30
    search_names=[]
    filter_names=[]
    def __init__(self,page=1,row_sort=[],row_filter={},row_search={},crt_user=None):
        self.page=page
        self.row_sort=row_sort
        self.row_filter=row_filter 
        self.row_search = row_search
        self.crt_user=crt_user 
        #field_names = [x.name for x in self.model._meta.fields]
        self.row_filter=row_filter
        
        
        
    @classmethod
    def parse_request(cls,request):
        """
        传入参数的形式：
        row_search: key=value&..
        row_sort: _sort=key1,-key2
        page: _page=1
        row_filter:key=value&..
        """
        kw = request.GET.dict()
        page = kw.pop('_page','1')
        row_sort = kw.pop('_sort','').split(',')
        row_sort=filter(lambda x: x!='',row_sort)
        row_search={}
        for k in cls.search_names:
            arg=kw.pop(k,None)
            if arg:
                row_search[k]=arg
        
        row_filter={}
        for k in cls.filter_names:
            arg = kw.pop(k,None)
            if arg:
                row_filter[k]=arg
        return cls(page,row_sort,row_filter,row_search,request.user)    
        
    def get_context(self):
        return {
            'heads':self.get_heads(),
            'rows': self.get_rows(),
            'page_choice' : self.pagenum.get_choice(),
            # 'filters_options':self.get_options(),
            'filters':self.get_filters(),
            #'sort':self.get_sort(),
            #'q': self.q ,
            # 'placeholder':self.get_placeholder(),
            'model':model_to_name(self.model),
        }
       
    
    def get_filters(self):
        """
        rt:
        [{name:field_name,label:field_label,option:[{value:xxx,label:xxx},]}]
        """
        return {}
    
    def get_search(self):
        """
        rt:
        [{name:field_name,placeholder:xxx}]
        """
        return {}
    
    def permited_fields(self):
        self.permit=Permit(model=self.model, user=self.crt_user)
        return self.permit.readable_fields()
    
    def get_heads(self):
        """
        return:[{"name": "name", "label": "\u59d3\u540d"}, {"sortable": true, "name": "age", "label": "\u5e74\u9f84"}]
        """
        ls = self.permited_fields()
        heads = model_to_head(self.model,include=ls)
        for head in heads:
            if head.get('name') in self.sortable:
                head['sortable'] = True 
        return heads
    
    def get_rows(self):
        """
        return: [{"name": "heyul0", "age": "32", "user": null, "pk": 1, "_class": "user_admin.BasicInfo", "id": 1}]
        """
        query = self.inn_filter(self.model.objects.all())
        #query = self.out_filter(query)
        query = self.search_filter(query)
        query = self.sort_filter(query)
        query = self.page_filter(query)
        return [to_dict(x, include=self.permited_fields()) for x in query] 
        

    def page_filter(self,query):
        self.pagenum = PageNum(query,perPage=self.perPage, pageNumber=self.page)
        return self.pagenum.get_rows()
    
    def inn_filter(self,query):
        if not self.crt_user.is_superuser and not self.permit.readable_fields():
            raise PermissionDenied,'no permission to browse %s'%self.model._meta.model_name
        else:
            return query
    
    def search_filter(self,query):
        for field in self.search_fields:
            kw ={}
            kw['%s__icontains'%field] =self.row_search            
        return query
    
    def sort_filter(self,query):
        
        return query
    
    def out_filter(self,query):
        if self.search_fields and self.row_search:
            exp = None
            for field in self.search_fields:
                if isinstance(field,SearchQuery):
                    query=field.get_query(query,self.row_search,self.crt_user)
                else:
                    kw ={}
                    kw['%s__icontains'%field] =self.row_search
                    if exp is None:
                        exp = Q(**kw)
                    else:
                        exp = exp | Q(**kw)
            if exp:
                query= query.filter(exp)
        if self.row_sort:
            return query.filter(**self.row_filter).order_by(*self.row_sort)
        else:
            return query.filter(**self.row_filter)
    
    def get_options(self):
        query = self.inn_filter(self.model.objects.all())
        options=[]
        for name in self.filters:
            tmp = []
            option =[]
            field = self.model._meta.get_field(name)
            label = field._verbose_name
            value = self.row_filter.get(name,'')
            for x in query: # get rid of duplicated row
                if getattr(x,name) not in tmp:
                    tmp.append(getattr(x,name))
                    if value == getattr(x,name):
                        option.append({'label': '%s:%s'%(name,getattr(x,name)),'name':getattr(x,name)})
                    else:
                        option.append({'label': getattr(x,name),'name':getattr(x,name)})
            options.append({
                'name':name,
                'label':label,
                'value': value,
                'options':option,
            })
        return options    
    
    def get_placeholder(self):
        ls=[]
        for field in self.search_fields:
            if isinstance(field,SearchQuery):
                ls.append(field.get_placeholder())
            else:
                ls.append(self.model._meta.get_field(field).verbose_name)
        return ','.join(ls)
        # return ','.join([self.model._meta.get_field(name).verbose_name for name in self.search_fields])



# from models import MobilePage
# class PageTable(ModelTable):
    # model = MobilePage
    # sortable=['name','label']
    # filters = ['name','label']
    # include= ['name','label']
    # search_fields=['name']
    # per_page=2
  