from weather import MockWeatherProvider, CachedWeatherProvider

def test_reproduction_bug_cache_mutation():
    mock_provider = MockWeatherProvider()
    cached_provider = CachedWeatherProvider(mock_provider)

    meteo_nord = cached_provider.get_meteo("NORD")
    assert meteo_nord.temperature == 38.5

    meteo_sud = cached_provider.get_meteo("SUD")
    assert meteo_sud.temperature == 42.0

    
    meteo_nord_apres = cached_provider.get_meteo("NORD")
    

    assert meteo_nord_apres.temperature == 38.5, (
        f"Attendu 38.5 pour le NORD, mais obtenu {meteo_nord_apres.temperature}"
    )