from base import *

TEMPLATE_DEBUG = True


DATABASES = {
    'default': {
        'NAME': 'insight',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'he123811',
        'HOST': '127.0.0.1', 
        'PORT': '3306',        
      },
    }



SITE_OPTION='hello.face'