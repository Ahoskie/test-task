import os

NUMBER_OF_USERS = int(os.getenv('NUMBER_OF_USERS'))
MAX_POSTS_PER_USER = int(os.getenv('MAX_POSTS_PER_USER'))
MAX_LIKES_PER_USER = int(os.getenv('MAX_LIKES_PER_USER'))

AUTH_SERVICE_API_URL = os.getenv('AUTH_SERVICE_API_URL')
SOCIAL_NETWORK_SERVICE_API_URL = os.getenv('SOCIAL_NETWORK_SERVICE_API_URL')
RANDOM_NAMES_API_URL = 'http://names.drycodes.com/'  # Add to the end of string an amount of names you want to get
