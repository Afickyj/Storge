# StorgeProject

## Popis projektu

StorgeProject je e-shopová aplikace vyvinutá pomocí Django frameworku. Umožňuje uživatelům prohlížet, vyhledávat a nakupovat produkty, spravovat svůj profil a sledovat své objednávky. Aplikace také zahrnuje administrativní rozhraní pro správu produktů, kategorií a objednávek.

## Funkce

- **Registrace a přihlášení uživatelů**
- **Správa uživatelských profilů**
- **Prohlížení a vyhledávání produktů**
- **Kategorizace produktů**
- **Správa košíku a objednávek**
- **Administrativní rozhraní pro správu obsahu**
- **API endpointy pro produkty**
- **Testování modelů, formulářů a pohledů**

## Technologie použité

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Databáze:** SQLite (pro vývojové prostředí)
- **Další nástroje:** Django Extensions, Graphviz, dbdiagram.io

## Instalace

### Předpoklady

- **Python 3.8+**
- **Pip (Python package manager)**
- **Virtuální prostředí (doporučeno)**

### Krok za krokem

1. **Klonování repozitáře:**
    ```bash
    git clone https://github.com/vas-uzivatel/StorgeProject.git
    cd StorgeProject
    ```

2. **Vytvoření a aktivace virtuálního prostředí:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Pro macOS/Linux
    .venv\Scripts\activate     # Pro Windows
    ```

3. **Instalace závislostí:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Nastavení databáze:**
    ```bash
    python manage.py migrate
    ```

5. **Vytvoření superuživatele:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Spuštění vývojového serveru:**
    ```bash
    python manage.py runserver
    ```

7. **Přístup k aplikaci:**
    - Otevřete webový prohlížeč a přejděte na `http://localhost:8000/`
    - Pro administrativní rozhraní přejděte na `http://localhost:8000/admin/`

## Použití

### Nepřihlášený uživatel

- Prohlížení produktů a kategorií
- Vyhledávání produktů
- Přidávání produktů do košíku

### Přihlášený uživatel

- Registrace a přihlášení
- Správa a aktualizace profilu
- Vytváření objednávek
- Sledování stavu objednávek

### Administrátor

- Správa produktů, kategorií a objednávek
- Úprava skladové zásoby produktů
- Přístup k API endpointům pro produkty

## Databázové modely a ER Diagram

### Přehled Entit

- **User**: Reprezentuje uživatele systému.
- **Profile**: Rozšiřuje informace o uživateli.
- **Category**: Kategorie, do které mohou být zařazeny produkty.
- **Product**: Produkty v e-shopu.
- **Order**: Objednávky vytvořené uživateli.
- **OrderItem**: Položky v objednávce.

### ER Diagram

Níže je ER diagram zobrazující vztahy mezi jednotlivými entitami ve vašem projektu.

![ER Diagram](er_diagram.png)

*Poznámka: Diagram byl vytvořen pomocí [dbdiagram.io](https://dbdiagram.io/).*

### Vysvětlení ER Diagramu

1. **User ↔ Profile**:
    - **Typ:** One-to-One (1:1)
    - **Popis:** Každý uživatel má jeden profil a každý profil patří jednomu uživateli.

2. **Category ↔ Product**:
    - **Typ:** One-to-Many (1:N)
    - **Popis:** Jedna kategorie může obsahovat více produktů, ale každý produkt patří pouze do jedné kategorie.

3. **User ↔ Product**:
    - **Typ:** One-to-Many (1:N)
    - **Popis:** Jeden uživatel může být autorem (vlastníkem) více produktů.

4. **User ↔ Order**:
    - **Typ:** One-to-Many (1:N)
    - **Popis:** Jeden uživatel může vytvořit více objednávek.

5. **Order ↔ OrderItem**:
    - **Typ:** One-to-Many (1:N)
    - **Popis:** Jedna objednávka může obsahovat více položek objednávky.

6. **Product ↔ OrderItem**:
    - **Typ:** One-to-Many (1:N)
    - **Popis:** Jeden produkt může být součástí více položek objednávky.

7. **Category ↔ Category (Self-referential)**:
    - **Typ:** One-to-Many (1:N)
    - **Popis:** Kategorie může mít nadřazenou kategorii, což umožňuje vytváření hierarchie kategorií (např. Elektronika > Mobily).

## Testování

### Spuštění testů

Projekt obsahuje testy pro modely, formuláře a pohledy. Testy můžete spustit pomocí následujícího příkazu:

```bash
python manage.py test
