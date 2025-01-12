import streamlit as st
import pandas as pd
from PIL import Image


# WCZYTANIE DANYCH
# załadowanie ikony
im = Image.open(r'C:\Users\julia\Documents\informatyka i ekonometria\semestr 3\inzynieria oprogramowania\ikona_app.jpg')

# wczytanie danych z normami
data=pd.read_csv(r"C:\Users\julia\Documents\informatyka i ekonometria\semestr 3\inzynieria oprogramowania\norms_clean.csv",
                 sep=";")

# wczytanie danych z powiazanymi badaniami oraz specjalistami
data2=pd.read_excel(r"C:\Users\julia\Documents\informatyka i ekonometria\semestr 3\inzynieria oprogramowania\norms_powiazania.xlsx",
                      engine="openpyxl")

# przekształcenie danych
data["combined"] = data["name"] + data["kind"].apply(lambda x: f" ({x})" if pd.notna(x) else "")
data = data[data['combined'].isin(data2['combined'])]

# USTAWIENIA STRONY APLIKACJI
st.set_page_config(page_title="NormaDlaNiej",
                   layout="wide",
                   page_icon = "🔬"
                   )

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
    ## Normy badań laboratoryjnych

    **Ważne informacje dotyczące norm i wyników badań:**

    1. **Indywidualność wyników**  
       Normy badań laboratoryjnych to zakresy referencyjne, które pomagają w interpretacji wyników. Należy jednak pamiętać, że:
       - Wartości referencyjne mogą różnić się w zależności od laboratorium, sprzętu i metod analitycznych.
       - Różne czynniki, takie jak wiek, płeć, dieta, aktywność fizyczna czy aktualny stan zdrowia, mogą wpływać na wyniki.

    2. **Dlaczego normy się różnią?**  
       W przypadku wielu badań normy mogą być inne w zależności od populacji, dla której zostały opracowane. Na przykład normy mogą być inne dla kobiet, mężczyzn, dzieci, osób starszych czy sportowców.
       Normy ukazane na tej stronie zostały opracowane dla kobiet w wieku 18-26 lat. 

    3. **Jak korzystać z norm?**  
       - Wynik mieszczący się w normie zazwyczaj nie wymaga dalszej diagnostyki, chyba że występują objawy wskazujące na problem zdrowotny.
       - Wynik poza normą nie zawsze oznacza problem zdrowotny – może być efektem przejściowych zmian w organizmie lub błędu laboratoryjnego.

    4. **Zawsze konsultuj wyniki z lekarzem!**  
       Interpretacja wyników badań powinna być przeprowadzona przez specjalistę, który uwzględni Twój ogólny stan zdrowia, historię chorób oraz styl życia. Nie polegaj wyłącznie na normach, ponieważ w medycynie każdy przypadek jest inny.

    **Pamiętaj:**  
    - Ta strona służy jedynie celom edukacyjnym i informacyjnym.  
    - W razie jakichkolwiek wątpliwości lub złego samopoczucia skontaktuj się z lekarzem pierwszego kontaktu lub specjalistą.

    ---
    """,
    unsafe_allow_html=True
)
# Wyswietlanie tabeli z normami
data = data.fillna("")
data = data.drop('combined', axis = 1)
st.dataframe(data,
             column_config={
                 "name" : "Nazwa badania 🩸",
                 "kind" : "Rodzaj",
                 "units" : "Jednostka",
                 "norm" : "Norma 🧪"
             },
             use_container_width = True,
             hide_index=True,
             height=3220)
