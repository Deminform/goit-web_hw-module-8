import traceback
import logging

logging.basicConfig(filename='app_errors.log', level=logging.ERROR)


def error_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            print(f"ValueError in {func.__name__}: {ve}")
            logging.error(f"ValueError in {func.__name__}: {ve}")
        except TypeError as te:
            print(f"TypeError in {func.__name__}: {te}")
            logging.error(f"TypeError in {func.__name__}: {te}")
        except KeyError as ke:
            print(f"KeyError in {func.__name__}: {ke}")
            logging.error(f"KeyError in {func.__name__}: {ke}")
        except Exception as e:
            print(f"Unexpected error in {func.__name__}: {e}")
            logging.error(f"Unexpected error in {func.__name__}: {traceback.format_exc()}")
        return None
    return wrapper
