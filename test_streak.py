from main import errechne_streak

def test_streak_zaehlt_aufeinanderfolgende_tage_korrekt():
    eintraege = [
        {"datum": "2026-05-01", "meditation": "y", "sauna": "y", "kraftsport": "y", "coding": "y"},
        {"datum": "2026-05-02", "meditation": "y", "sauna": "y", "kraftsport": "y", "coding": "y"},
        {"datum": "2026-05-03", "meditation": "y", "sauna": "y", "kraftsport": "y", "coding": "y"},
        {"datum": "2026-05-04", "meditation": "y", "sauna": "n", "kraftsport": "y", "coding": "y"},
        {"datum": "2026-05-05", "meditation": "y", "sauna": "y", "kraftsport": "y", "coding": "y"},
    ]
    assert errechne_streak(eintraege, "meditation") == 5
    assert errechne_streak(eintraege, "sauna") == 1
    assert errechne_streak(eintraege, "kraftsport") == 5
    assert errechne_streak(eintraege, "coding") == 5
    assert errechne_streak(eintraege, "invalid") == 0 
