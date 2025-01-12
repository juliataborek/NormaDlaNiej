import streamlit as st
import pandas as pd
from PIL import Image
import io
# import openpyxl

# WCZYTANIE DANYCH
# wczytanie danych z normami
data=pd.read_csv(r"C:\Users\julia\Documents\informatyka i ekonometria\semestr 3\inzynieria oprogramowania\norms_clean.csv",
                 sep=";")

# wczytanie danych z powiazanymi badaniami oraz specjalistami
data2=pd.read_excel(r"C:\Users\julia\Documents\informatyka i ekonometria\semestr 3\inzynieria oprogramowania\norms_powiazania.xlsx",
                      engine="openpyxl")

# załadowanie ikony
im = Image.open(r'C:\Users\julia\Documents\informatyka i ekonometria\semestr 3\inzynieria oprogramowania\ikona_app.jpg')

# USTAWIENIA STRONY APLIKACJI
st.set_page_config(page_title="NormaDlaNiej",
                   layout="wide",
                   page_icon = "🔬"
                   )

#usuniecie przycisku menu i ikony Streamlit
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

# USTAWIENIA STRONY STARTOWEJ
# Główny nagłówek z ikoną
col1, col2 = st.columns([1, 8])
with col1:
    st.image(im, width=100)
with col2:
    st.title("**NormaDlaNiej**")

# Link do GitHub w wierszu
st.markdown(
    """
    [![Star](https://img.shields.io/github/stars/nataliamachlus1501/LaboratoryTestAnalyzer.svg?logo=github&style=social)](https://github.com/nataliamachlus1501/LaboratoryTestAnalyzer)
    """,
    unsafe_allow_html=True,
)
# Opis działania
st.markdown(
    """
    <style>
        .intro-text {
            font-size: 18px;
            line-height: 1.6;
            color: #333333;
        }
        .highlight {
            font-weight: bold;
            color: #2b7a78;
        }
    </style>
    <div class="intro-text">
        Nasza aplikacja umożliwia szybkie i łatwe sprawdzenie wyników badań krwi pod kątem 
        ich zgodności z normami dla <span class="highlight">kobiet w wieku 18-26 lat</span>. 
        Po wprowadzeniu podstawowych danych, takich jak wiek, płeć oraz wyników badań, otrzymasz 
        <span class="highlight">informację, czy wyniki są prawidłowe</span>. Jeśli coś odbiega od normy, aplikacja 
        wskaże specjalistę, do którego warto udać się na konsultację. Dzięki temu możesz zadbać 
        o swoje zdrowie z większą pewnością i wygodą.
    </div>
    """,
    unsafe_allow_html=True,
)

# FUNKCJE DO WYODRĘBNIANIA GRANICY NORM
def extract_min(norm):
    """
    Funkcja wyodrębniająca minimalną wartość normy
    :param norm: zakres normy do sprawdzenia
    :return: minimalna granica normy
    """
    try:
        if '-' in norm:
            return float(norm.split('-')[0].strip())
        if '>' in norm:
            return float(norm.split('>')[1].split('[')[0].strip())
        if '<' in norm or '≤' in norm:
            return 0
        if '–' in norm:
            return float(norm.split('–')[0].strip())
    except:
        return None

def extract_max(norm):
    """
    Funkcja wyodrębnianiaca maksymalną wartość normy
    :param norm: zakres normy do sprawdzenia
    :return: górna granica normy
    """
    try:
        if '-' in norm:
            if '[' in norm:
                return float(norm.split('-')[1].split('[')[0].strip())
            else:
                return float(norm.split('-')[1].split('x')[0].strip())
        if '≤' in norm:
            return float(norm.split('≤')[1].split('[')[0].strip())
        if '<' in norm:
            return float(norm.split('<')[1].split('[')[0].strip())
        if '–' in norm:
            return float(norm.split('–')[1].split('[')[0].strip())
    except:
        return  None


def check_result_in_norm(result, norm_min, norm_max):
    """
    Funkcja zwracająca informację, czy wynik krwi jest w normie
    :param result: wynik badania krwi
    :param norm_min: dolna granica normy
    :param norm_max: górna granica normy
    :return: informacja, czy wynik jest w normie
    """
    if result < norm_min:
        return "⬇️ Poniżej normy"
    elif result > norm_max:
        return "⬆️ Powyżej normy"
    else:
        return "✅ W normie"

# PORZĄDKOWANIE TABELI Z DANYMI
# Tworzenie nowych kolumn
data['min'] = data['norm'].apply(extract_min)
data['max'] = data['norm'].apply(extract_max)
# połączenie kolumn z nazwami badania
data["combined"] = data["name"] + data["kind"].apply(lambda x: f" ({x})" if pd.notna(x) else "")
# usunięcie niepotrzebnego napisu '(Kobiety)'
data['combined'] = data['combined'].str.replace('(Kobiety)', '', regex=False)
data2['combined'] = data2['combined'].str.replace('(Kobiety)', '', regex=False)
data['combined'] = data['combined'].str.replace('(kobiety)', '', regex=False)
data2['combined'] = data2['combined'].str.replace('(kobiety)', '', regex=False)
data['combined'] = data['combined'].str.replace(' - Kobiety', '', regex=False)
data2['combined'] = data2['combined'].str.replace(' - Kobiety', '', regex=False)


# wybranie tylko uwzględnionych badań
data = data[data['combined'].isin(data2['combined'])]


# SEKCJA Z DANYMI O UŻYTKOWNIKU
st.header("Dane użytkownika", divider='grey')

# informacja o wieku i płci użytkownika
col1, col2 = st.columns(2)

with col1:
    # Wiek użytkownika z dynamiczną walidacją
    wiek = st.number_input(
        "Podaj swój wiek:",
        min_value=1,
        max_value=100,
        step=1,
        value=None,
        help="Wprowadź swój wiek w latach."
    )

with col2:
    # Wybór płci
    plec = st.radio(
        "Wybierz swoją płeć:",
        ["👩 Kobieta", "👨 Mężczyzna"],
        index=0,
        help="Wybierz odpowiednią płeć, aby dopasować normy wyników badań."
    )

# WALIDACJA UŻYTKOWNIKA ORAZ PROCES POBIERANIA WYNIKOW BADAN I SPRAWDZANIA NORM
if wiek is not None and plec is not None:
    # walidacja wieku i płci użytkownika
    if wiek not in range(18,27) or plec == "👨 Mężczyzna":
        # przypadek, gdy wiek i płeć nie jest taka jak oczekiwana
        st.markdown(
            """
            <div style="background-color: #f8d7da; padding: 20px; border-radius: 5px; border: 1px solid #f5c2c7;">
                <h4 style="color: #721c24;">Przykro nam, ale aplikacja nie jest skierowana do Ciebie.</h4>
                <p style="color: #721c24; font-size: 14px;">
                    Ta aplikacja została stworzona dla kobiet w wieku 18–26 lat, aby ułatwić analizę wyników badań krwi z tej grupy.
                    Jeśli nie spełniasz tych kryteriów, pamiętaj, że normy przedstawione w aplikacji mogą nie odpowiadać Twojej sytuacji zdrowotnej.
                    Mimo to, możesz zapoznać się z nimi, ale zalecamy, aby traktować te dane jako informacyjne, a nie diagnostyczne.
                    W razie wątpliwości skonsultuj się ze specjalistą!
                </p>
                <a href="/norms_page" target="_self" style="text-decoration: none; color: white; background-color: #dc3545; padding: 10px 20px; border-radius: 5px; font-size: 14px;">
                    Zobacz normy badań
                </a>
            </div>
            """, unsafe_allow_html=True
        )

    else:
        # przypadek, gdy użytkownikiem jest kobieta w wieku 18-26 lat

        st.header("Podaj wyniki badań", divider= 'grey')

        # przechowywanie wyników w słowniku
        results = {}

        opcje = list(data["combined"]) # Lista z możliwymi badaniami do wybrania
        opcje.insert(0, "Zaznacz wszystkie")  # Dodanie "Zaznacz wszystkie" na początku listy

        # Lista wielokrotnego wyboru
        wybrane_badania = st.multiselect(
            "Wybierz badania, których wyniki chcesz wprowadzić:",
            opcje,
            default=[],  # Domyślnie brak zaznaczenia
            help="Wybierz jedno lub więcej badań z listy."
        )

        # Logika dla "Zaznacz wszystkie"
        if "Zaznacz wszystkie" in wybrane_badania:
            wybrane_badania = opcje[1:]  # Zaznacz wszystkie opcje oprócz "Zaznacz wszystkie"


        # Interfejs w pętli
        for index, row in data.iterrows():
            if row["combined"] in wybrane_badania:
                # możliwość wprowadzenia wyniku wybranych badań
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(
                        f"Wprowadź wynik dla <span style='color:blue; font-weight:bold;'>{row['combined']}</span>:",
                        unsafe_allow_html=True
                    )
                    wynik = st.number_input(
                        f"",
                        key=f"wynik_{index}",
                        value=None,
                        min_value=0,
                        max_value=500,
                    )
                with col2:
                    st.markdown(
                        f"<p style='margin-top:40px;'>{row['units'].split(',')[0]}</p>",
                        unsafe_allow_html=True
                    )
                # Przechowaj wynik
                results[row['combined']] = wynik

        # Analiza wyników po kliknięciu
        if st.button("Przejdź do analizy wyników"):

            # Przygotowanie DataFrame z wynikami użytkownika
            user_results = pd.DataFrame({
                'Nazwa badania': results.keys(),
                'Norma' : None,
                'Twój wynik': results.values()
            })

            # Filtracja wierszy w data2, które są w data
            filtered_data2 = data2[data2['combined'].isin(user_results['Nazwa badania'])]

            # sprawdzenie poprawnosci wynikow
            user_results = user_results[user_results['Twój wynik'].notna()]

            # przejscie do analizy następuje, gdy co najmniej 1 wynik jest uzupełniony
            if len(user_results) > 0:

                status_badania = []
                normy = []
                lekarze = []
                powiazane_badania = []

                for index, row in user_results.iterrows():
                    badanie = row['Nazwa badania']
                    wynik = row['Twój wynik']

                    norm_min = data[data['combined'] == badanie]['min'].values[0]
                    norm_max = data[data['combined'] == badanie]['max'].values[0]

                    norma = data[data['combined'] == badanie]['norm'].values[0]
                    normy.append(norma)

                    status = check_result_in_norm(wynik, norm_min, norm_max)
                    status_badania.append(status)

                    # Dodaj wartości do kolumn 'Lekarz' i 'Powiązane badanie' tylko, gdy badanie nie jest w normie
                    if status != "✅ W normie":
                        # Filtruj dane dla danego badania
                        filtered_row = filtered_data2[filtered_data2['combined'] == badanie]

                        # Sprawdź, czy znaleziono dopasowanie
                        if not filtered_row.empty:
                            lekarz = filtered_row['medical'].values[0]  # Pobierz wartość, jeśli istnieje
                            badanie_powiazane = filtered_row['badanie'].values[0]  # Pobierz wartość, jeśli istnieje
                        else:
                            lekarz = ""  # Brak dopasowania - pusta wartość
                            badanie_powiazane = ""
                    else:
                        lekarz = ""  # W normie - pusta wartość
                        badanie_powiazane = ""

                    lekarze.append(lekarz)
                    powiazane_badania.append(badanie_powiazane)

                user_results['Norma 🧪'] = normy
                user_results['Status'] = status_badania
                user_results['Lekarz 🩺'] = lekarze
                user_results["Powiązane badanie 🩸"] = powiazane_badania

                # Zamiana NaN na pusty ciąg
                user_results_display = user_results.fillna("")

                # Wyświetlenie tabeli
                st.header("Analiza Twoich wyników badań", divider='grey')
                st.dataframe(user_results_display,
                             use_container_width=True,
                             hide_index=True)

                # Wyświetlenie informacji o ogólnym wyniku
                num_out_of_range = len(user_results[user_results['Status'] != "✅ W normie"])
                if num_out_of_range > 0:
                    st.info(
                        f"⚠️ W Twoich wynikach znaleziono {num_out_of_range} odchylenia od normy. "
                        "Pamiętaj, że drobne odchylenia od normy nie zawsze muszą być powodem do niepokoju – mogą wynikać z naturalnych wahań organizmu, diety czy stylu życia. "
                        "Jeśli jednak odczuwasz jakiekolwiek dolegliwości, zalecamy konsultację z lekarzem. Specjalista pomoże Ci zinterpretować wyniki w kontekście Twojego stanu zdrowia i, jeśli to konieczne, zleci dodatkowe badania lub leczenie.")
                else:
                    st.success("🎉 Wszystkie Twoje wyniki są w normie! Brawo!")
