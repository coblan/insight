from base import *

TEMPLATE_DEBUG = True
LANGUAGE_CODE = 'zh-hans'


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


LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)