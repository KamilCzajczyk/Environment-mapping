# Environment Mapping - Cube Map

## Opis projektu

Aplikacja 3D implementująca mapowanie środowiska (environment mapping) przy użyciu cube map w OpenGL z biblioteką Pygame. Program renderuje skybox oraz obiekty z odbiciami środowiska, takie jak sześcian, sfera i torus.

## Struktura projektu

```
projekt/
├── main.py              # Punkt wejściowy aplikacji
├── config.py           # Konfiguracja aplikacji
├── engine/
│   ├── camera.py       # System kamery
│   ├── renderer.py     # Główny renderer
│   ├── objects.py      # Renderowanie obiektów 3D
│   ├── cubemap.py      # Ładowanie cube map
│   └── utils.py        # Funkcje pomocnicze
└── tekstury/           # Foldery z teksturami cube map
    ├── bridge/
    ├── yokohama2/
    ├── yokohama3/
    └── yokohama4/
```

## Funkcjonalności

### Główne cechy
- **Skybox**: Renderowanie tła 360° przy użyciu cube map
- **Odbicia środowiska**: Realistyczne odbicia na powierzchniach obiektów
- **Interaktywna kamera**: Sterowanie pierwszoosobowe z myszą i klawiaturą
- **Przełączanie środowisk**: Zmiana cube map w czasie rzeczywistym
- **Oświetlenie**: System oświetlenia OpenGL

### Obiekty z odbiciami
- **Sześcian odbijający**: Centralny obiekt z powierzchnią lustrzaną
- **Sfera odbijająca**: Sfera z gładkimi odbiciami
- **Torus odbijający**: Torus z zakrzywionymi odbiciami

## Pliki źródłowe

### main.py
Punkt wejściowy aplikacji. Inicjalizuje renderer i obsługuje błędy.

```python
# Uruchamia główną pętlę renderowania
renderer = CubeMapRenderer()
renderer.run()
```

### config.py
Centralna konfiguracja aplikacji zawierająca:
- **Parametry okna**: rozdzielczość, tytuł, FPS
- **Ustawienia kamery**: prędkość, czułość myszy, ograniczenia
- **Parametry renderowania**: kolory, clipping planes, FOV
- **Listy cube map**: dostępne zestawy tekstur

### engine/camera.py
Implementuje system kamery pierwszoosobowej:

#### Klasa Camera
- **Pozycja**: współrzędne kamery w przestrzeni 3D
- **Rotacja**: pitch (x) i yaw (y) kamery
- **Sterowanie**: 
  - WASD/strzałki - ruch
  - Mysz - rozglądanie
  - Spacja - ruch w górę
  - Shift/C - ruch w dół

#### Kluczowe metody
- `apply_transform()`: Aplikuje transformacje kamery do macierzy OpenGL
- `handle_input()`: Obsługuje input z klawiatury i myszy

### engine/renderer.py
Główny system renderowania aplikacji.

#### Klasa CubeMapRenderer
Zarządza całym procesem renderowania:

##### Inicjalizacja
- Konfiguracja okna Pygame
- Ustawienia OpenGL (depth test, culling, tekstury)
- Ładowanie początkowego cube map
- Inicjalizacja kamery i oświetlenia

##### Główna pętla
- `_handle_events()`: Obsługa zdarzeń (zamknięcie, przełączanie cube map)
- `_render_frame()`: Renderowanie jednej klatki
- `_switch_cubemap()`: Przełączanie między różnymi środowiskami

### engine/objects.py
Zawiera funkcje renderowania obiektów 3D.

#### Funkcje renderowania

##### `setup_lighting()`
Konfiguruje oświetlenie OpenGL z jednym źródłem światła.

##### `draw_skybox(cube_map_id, camera_pos)`
Renderuje skybox:
- Wyłącza depth writing i culling
- Centruje skybox na pozycji kamery
- Używa cube map jako tekstury tła

##### `draw_reflective_cube(cube_map_id, camera_pos)`
Renderuje odbijający sześcian:
- Oblicza wektory odbić dla każdego wierzchołka
- Używa cube map do teksturowania powierzchni

##### `draw_reflective_sphere(cube_map_id, camera_pos)`
Renderuje odbijającą sferę:
- Generuje geometrię sfery przez triangulację
- Oblicza odbicia na podstawie normalnych powierzchni

##### `draw_reflective_torus(cube_map_id, camera_pos)`
Renderuje odbijający torus:
- Proceduralne generowanie geometrii torusa
- Zaawansowane obliczenia normalnych dla zakrzywionej powierzchni

### engine/cubemap.py
Obsługuje ładowanie i tworzenie cube map.

#### Funkcja `create_cubemap_from_images(folder, face_files)`
- Ładuje 6 obrazów reprezentujących ściany sześcianu
- Tworzy teksturę cube map w OpenGL
- Implementuje fallback dla brakujących plików
- Konfiguruje parametry filtrowania tekstur

#### Funkcja `_create_fallback_face(face_target, filename)`
Tworzy kolorową teksturę zastępczą dla brakujących plików.

### engine/utils.py
Funkcje matematyczne pomocnicze.

#### `normalize(v)`
Normalizuje wektor 3D do długości jednostkowej.

#### `reflect(incident, normal)`
Oblicza wektor odbity na podstawie wektora padającego i normalnej powierzchni.

## Sterowanie

### Kamera
- **W/S lub ↑/↓**: Ruch do przodu/tyłu
- **A/D lub ←/→**: Ruch w lewo/prawo  
- **Spacja**: Ruch w górę
- **Shift/C**: Ruch w dół
- **Mysz + LPM**: Rozglądanie się

### Aplikacja
- **B**: Przełączanie między różnymi cube map
- **ESC/Zamknięcie okna**: Wyjście z aplikacji

## Wymagania techniczne

### Biblioteki Python
- `pygame`: System okien i input
- `PyOpenGL`: Bindingi OpenGL
- `PIL (Pillow)`: Ładowanie obrazów
- `numpy`: Operacje na tablicach

### Formaty tekstur
- Obsługiwane formaty: JPG, PNG
- Wymagane 6 plików na cube map:
  - `px.jpg` - Positive X (prawo)
  - `nx.jpg` - Negative X (lewo)
  - `py.jpg` - Positive Y (góra)
  - `ny.jpg` - Negative Y (dół)
  - `pz.jpg` - Positive Z (przód)
  - `nz.jpg` - Negative Z (tył)

## Szczegóły techniczne

### Algorytm odbić
Aplikacja implementuje environment mapping przez:

1. **Obliczenie wektora patrzenia**: od powierzchni do kamery
2. **Odbicie wektora**: względem normalnej powierzchni
3. **Próbkowanie cube map**: używając wektora odbicia jako współrzędnej tekstury

### Optymalizacje
- **Depth testing**: Efektywne usuwanie niewidocznych fragmentów
- **Face culling**: Pomijanie tylnych ścian obiektów
- **Skybox rendering**: Optymalizowane renderowanie tła
- **Texture filtering**: Liniowe filtrowanie dla gładkich odbić

### Przestrzeń współrzędnych
- System prawoskrętny
- Kamera patrzeącna ujemny Z
- Jednostki w metrach (przybliżone)

## Rozszerzenia i modyfikacje

### Dodawanie nowych obiektów
1. Implementuj funkcję renderowania w `objects.py`
2. Oblicz normalne powierzchni dla każdego wierzchołka
3. Użyj `utils.reflect()` do obliczenia odbić
4. Dodaj wywołanie w `renderer.py`

### Dodawanie nowych cube map
1. Utwórz folder z 6 obrazami
2. Dodaj nazwę folderu do `CUBEMAP_SETS` w `config.py`
3. Upewnij się, że pliki mają poprawne nazwy

### Modyfikacja parametrów
Wszystkie kluczowe parametry znajdują się w `config.py`:
- Prędkość kamery
- Czułość myszy
- Rozdzielczość
- Kolory tła
- Parametry projekcji

## Troubleshooting

### Brakujące tekstury
- Aplikacja automatycznie tworzy kolorowe zamienniki
- Sprawdź ścieżki do plików i ich nazwy
- Upewnij się, że obrazy są w formacie RGB

### Problemy z wydajnością
- Zmniejsz rozdzielczość tekstur
- Ogranicz liczbę wierzchołków w obiektach
- Sprawdź sterowniki graficzne

### Błędy OpenGL
- Upewnij się, że sterowniki obsługują wymagane rozszerzenia
- Sprawdź dostępność hardware'owego przyspieszenia

## Autor i licencja

Projekt implementujący zaawansowane techniki renderowania 3D w czasie rzeczywistym z użyciem OpenGL i Pythona.
