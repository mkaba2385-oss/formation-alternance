from functools import wraps
import os 


# dictionnaire global des plugins 
PLUGINS = {}

def register(nom):

    def decorateur(fun):
        PLUGINS["nom"] = func
        return func
    return decorateur


def run_plugins(nom, *args, **kwargs):
    if nom not in PLUGINS:
        raise ValueError(f"le plugins {nom} n'existe pas")
    return PLUGINS[nom](*args, **kwargs)

def only_if_env(env) :
    def decorateur(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.getenv("ENV") == env :
                return func(*args, **kwargs)

            print(f"Plugin désactivé (ENV={os.getenv('ENV')})")
        return wrapper
    return decorateur

# Plugin SMS de test (désactivé en production)

@register("sms")
@only_if_env("dev")
def envoyer_sms(numero, message):
    print(f"SMS envoyé à {numero}")
    print(f"Message : {message}")
    