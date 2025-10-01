from linkedin_crawler.format_emails import get_email

def test_email_format():
    name = "Jan de Vries"
    assert get_email("flast", "", name) == "jvries@"
    assert get_email("f.last", "", name) == "j.vries@"
    assert get_email("f.middlelast", "", name) == "j.devries@"
    assert get_email("first.last", "", name) == "jan.vries@"
    assert get_email("first.middle.last", "", name) == "jan.de.vries@"
    name = "J. de Vries"
    assert get_email("flast", "", name) == "jvries@"
    assert get_email("fmiddlelast", "", name) == "jdevries@"
    name = "Jan Jansen"
    assert get_email("flast", "", name) == "jjansen@"
    assert get_email("fmiddlelast", "", name) == "jjansen@"

def test_maiden_name():
    name = "Ingrid van den Berg-de Jong"
    assert get_email("flast", "", name) == "iberg@"
