from core.tabel import ModelTable

from models import BasicInfo

def get_table_scope():
    return {
        'basicinfo':BasicInfoTable
    }

 
class BasicInfoTable(ModelTable):
    model = BasicInfo
    # sortable=['name','label']
    # include= ['name','label']
    # search_fields=['name']
    # per_page=2