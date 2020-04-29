from datetime import timedelta as datetime_timedelta
SECRET_KEY = 'yandexlyceum_secret_key'
CSRF_ENABLED = True
PERMANENT_SESSION_LIFETIME = datetime_timedelta(minutes=15)
DEBUG = False

RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
