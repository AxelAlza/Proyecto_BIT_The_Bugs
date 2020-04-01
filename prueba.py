import os



def key():
    os.environ['GOOGLE_API'] = 'AIzaSyBVIfuWRfCpm7l0qGw8KSaxD6YB4vGxSxo'
    env_var = os.environ.get('GOOGLE_API')
    return env_var



