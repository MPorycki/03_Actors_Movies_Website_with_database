# 03_Actors_Movies_Website_with_databse - tasks description


Stwórz endpoint, który zwróci w JSON listę wszystkich nazw miast zawartych w tabelli city. Kolejność nazw miast powinna być alfabetyczna. Zapytanie na:
# 1. GET /cities
zwróci:

["A Corua (La Corua)", "Alessandria", ...]
Dodaj do endpointu wyświetlającego listę nazw miast obsługę parametru country_name. Parametr ma powodować wybranie miast tylko z podanego kraju. Kolejność nazw miast powinna być alfabetyczna tak jak w pkt. 1.
GET /cities?country_name=Poland
zwróci:

[
    "Bydgoszcz",
    "Czestochowa",
    "Jastrzebie-Zdrj",
    "Kalisz",
    "Lublin",
    "Plock",
    "Tychy",
    "Wroclaw"
]

# 2.
Przygotuj endpoint, który zwróci w JSON słownik gdzie kluczem będzie nazwa języka, a wartością liczba ról we wszystkich filmach w danym języku. Zakładamy, że dany aktor grał tylko jedną rolę w danym filmie.
Wskazówka: GROUP BY: https://www.sqlite.org/lang_select.html#resultset
Wskazówka: agregacja
zapytanie:

# 3. GET /lang_roles
Przykładowa odpowiedź:

{
   "English":  1092400,
   "Italian": 0,
   "Japanese": 0,
   "Mandarin": 0,
   "German": 0,
   "French": 0
}
# 4.
Przygotuj endpoint do dodawania nowych miast. W JSONie przesyłanym POSTem powinna znajdować się informacja o nazwie miasta oraz id kraju do którego należy dodawane miasto. Po dodaniu miasta należy zwrócić stworzony obiekt z kodem 200. Endpoint powinien zawierać prostą walidację (tzn. odrzucać próbę stworzenia miasta dla nieistniejącego kraju itp.). W przypadku błędu należy zwrócić kod 400 oraz JSONa z kluczem "error", który będzie zawierał krótki opis błędu (treść błędu nie będzie sprawdzana).
POST /cities

{
    "country_id": 76,
    "city_name": "Warszawa"
}
Przykładowa odpowiedź z sukcesem:

{
    "country_id": 76,
    "city_name": "Warszawa",
    "city_id": 601
}
Przykładowa odpowiedź z błędem:

{
    "error": "Invalid country_id"
}

# 5.
Dodaj do endpointu GET /cities możliwość dzielenia wyniku na strony. Endpoint powinien obsługiwać dodatkowe parametry w query stringu - per_page, czyli ile wyników ma się wyświetlać na jednej stronie i page, który mówi o tym, którą stronę chcemy aktualnie wyświetlić. Strony numerujemy od 1 w górę. Poprawne rozwiązanie powinno działać razem z filtrowaniem po nazwie kraju jeśli nazwa kraju będzie podana.
Wskazówka: LIMIT
Wskazówka: OFFSET
GET /cities?per_page=10&page=2
zwróci:

[
    "Akron",
    "Alessandria",
    "Allappuzha (Alleppey)",
    "Allende",
    "Almirante Brown",
    "Alvorada",
    "Ambattur",
    "Amersfoort",
    "Amroha",
    "Angra dos Reis"
]

# 6*. 
Na wykładzie Kuba wspominał o tym, że relacja wiele do wielu między tabelami film i category jest trochę na wyrost. Analiza danych z naszej bazy wykazuje, że każdy film ma tylko jedną kategorię. Chcielibyśmy się pozbyć nadmiarowej relacji wiele do wielu i zastąpić ją relację jeden do wielu. Proszę przygotować migrację. Do tabeli film należy dołożyć kolumnę category_id wskazującą na kategorie z tabeli category. Należy też usunąć nadmiarową tabelę film_category. Migracja nie może zmieniać danych, które już są wprowadzone do tabeli - wszystkie dotychczasowe powiązania filmu z kategorią powinny być odwzorowane po migracji. Migrację proszę przygotować jako skrypt SQL i wkleić jego zawartość do formularza.
Wskazówka: ALTER TABLE
Wskazówka: https://stackoverflow.com/questions/21772631/sqlite-update-query-using-a-subquery
Wskazówka: DROP TABLE
