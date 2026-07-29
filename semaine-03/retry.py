from functools import wraps
import time 

def retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(Exception,)  ) :
    def decorateur(func):
        @wraps (func)
        def wrapper(*args, **kwargs) :
            current_delay = delay
            last_exception = None 

            for attempt in range(max_attempts):
                try :
                    return func(*args, **kwargs)
                except exceptions as e :
                    last_exception = e 
                    print(f"Tentative {attempt + 1}/ {max_attempts} échouée: {e}")
                    

                if attempt < max_attempts -1:
                    time.sleep(current_delay)
                    current_delay *= backoff
            raise last_exception

        return wrapper

    return decorateur

    