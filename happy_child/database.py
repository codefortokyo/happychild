import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('MYSQL_HOST') or '127.0.0.1',
        'NAME': os.getenv('MYSQL_DATABASE') or 'happy_child',
        'USER': os.getenv('MYSQL_USER') or 'root',
        'PASSWORD': os.getenv('MYSQL_PASSWORD') or 'z5gYmm6J',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
    'primary': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('MYSQL_HOST') or '127.0.0.1',
        'NAME': os.getenv('MYSQL_DATABASE') or 'happy_child',
        'USER': os.getenv('MYSQL_USER') or 'root',
        'PASSWORD': os.getenv('MYSQL_PASSWORD') or 'z5gYmm6J',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
    'replica': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('MYSQL_HOST') or '127.0.0.1',
        'NAME': os.getenv('MYSQL_DATABASE') or 'happy_child',
        'USER': os.getenv('MYSQL_USER') or 'root',
        'PASSWORD': os.getenv('MYSQL_PASSWORD') or 'z5gYmm6J',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    },
}
