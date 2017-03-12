from base import *

#STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)
#MEDIA_ROOT= os.path.join( os.path.dirname(BASE_DIR),'media')

TEMPLATE_DEBUG = True


import os
if os.environ.get('TEST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }  
else:
    DATABASES = {
        'default': {
            'NAME': 'insight',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': '127.0.0.1', 
            'PORT': '3306',        
          },
        }





SITE_OPTION='hello.face'