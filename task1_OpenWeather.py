from pyowm import OWM
from datetime import datetime, timedelta, timezone

# Подключение по API ключу
owm = OWM('d698604e2fc936020cb2749ce1e025d0')
mgr = owm.weather_manager()

reg = owm.city_id_registry()
# Нахождение местоположения города
list_of_tuples = reg.locations_for('Lyubertsy')
my_city = list_of_tuples[0]
lat = my_city.lat
lon = my_city.lon

days_range = 5  # Диапазон искомых дней
max_diff_temp = -1  # Максимальная разница значений
max_light_date = None  # Дата дня с максимальной разницей значений
max_temp_date = None
max_time_diff = timedelta(hours=0)  # Максимальная разница значений
# Проход по всем дням и подсчет разницы значений
# За время определении времени взято 2 часа ночи, как время близкое к самой низкой температуре за ночь
for i in range(days_range + 1):
    epoch = int((datetime.now().replace(hour=2, minute=0, second=0) - timedelta(days=i)).replace(
        tzinfo=timezone.utc).timestamp())
    one_call = mgr.one_call_history(lat=lat, lon=lon, dt=epoch)
    observed_weather = one_call.current
    temp_diff = abs(             # Подсчет разницы значений
        observed_weather.temperature('celsius')["temp"]
        - observed_weather.temperature('celsius')["feels_like"])
    # Если разница больше - запоминаем
    if int(temp_diff) > max_diff_temp:
        max_diff_temp = temp_diff
        max_temp_date = observed_weather.reference_time()
    daylight = datetime.fromtimestamp(observed_weather.sunset_time()) - datetime.fromtimestamp(
        observed_weather.sunrise_time())
    if daylight > max_time_diff:
        max_time_diff = daylight
        max_light_date = observed_weather.reference_time()
print(
    f"За последние {days_range} ночей максимальная разница между ощущаемой температурой и фактической"
    f" была {datetime.fromtimestamp(max_temp_date).strftime('%Y-%m-%d')}.")
print(
    f"Максимальная продолжительность светового дня за последние {days_range} дней "
    f" была {datetime.fromtimestamp(max_light_date).strftime('%Y-%m-%d')} и составляла время - {max_time_diff}.")

