# Environment Mapping - Cube Map

## Opis projektu

Aplikacja 3D implementująca mapowanie środowiska (environment mapping) przy użyciu cube map w OpenGL z biblioteką Pygame. Program renderuje skybox oraz obiekty z odbiciami środowiska, takie jak sześcian, sfera i torus.

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

### config.py
Plik konfiguracyjny aplikacji:
- **Parametry okna**: rozdzielczość, tytuł, FPS
- **Ustawienia kamery**: prędkość, czułość myszy, ograniczenia
- **Parametry renderowania**: kolory, clipping planes, FOV
- **Listy cube map**: dostępne zestawy tekstur

### engine/camera.py
System kamery pierwszoosobowej

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
System renderowania aplikacji.

#### Klasa CubeMapRenderer
Zarządza całym procesem renderowania:

##### Główna pętla
- `_handle_events()`: Obsługa zdarzeń (zamknięcie, przełączanie cube map)
- `_render_frame()`: Renderowanie jednej klatki
- `_switch_cubemap()`: Przełączanie między różnymi środowiskami

### engine/objects.py
Zawiera funkcje renderowania obiektów 3D.

#### Funkcje renderowania

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

#### Funkcja `_create_fallback_face(face_target, filename)`
Tworzy kolorową teksturę zastępczą dla brakujących plików.

### engine/utils.py
Funkcje matematyczne pomocnicze.

#### `normalize(v)`
Normalizuje wektor 3D do długości jednostkowej.

#### `reflect(incident, normal)`
Oblicza wektor odbity na podstawie wektora padającego i normalnej powierzchni.



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


### Modyfikacja parametrów
Wszystkie kluczowe parametry znajdują się w `config.py`:
- Prędkość kamery
- Czułość myszy
- Rozdzielczość
- Kolory tła
- Parametry projekcji
