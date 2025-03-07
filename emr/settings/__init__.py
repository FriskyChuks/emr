
# from .production import * # Heroku

try:
    from .local import *  # PG ADMIN 4
except:
    pass

# try:
#     from .base import *  # PG ADMIN 4
# except:
#     pass
