import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('MYSQL_HOST'),
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
    'primary': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('MYSQL_HOST'),
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
    'replica': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('MYSQL_HOST'),
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
}
