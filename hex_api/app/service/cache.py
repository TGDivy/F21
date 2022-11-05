from flask_caching import Cache
from flask import Flask

cache = Cache(config={
    'DEBUG': False,
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': f'/cache/flask/'
})
