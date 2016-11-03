
class Permit(object):
    def __init__(self,user):
        self.user=user
        
    def can_add(self):
        return True
    
    def can_del(self):
        return True
    
    def readonly_fields(self):
        return []
    
    def change_able_fields(self):
        return []