import os



def key():
    os.environ['GOOGLE_API'] = 'Secret'
    env_var = os.environ.get('GOOGLE_API')
    return env_var



