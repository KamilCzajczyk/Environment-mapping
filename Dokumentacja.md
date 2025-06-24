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

#### Metody
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



# Szczegóły techniczne

## 1. Algorytm odbić

### 1.1 Podstawy matematyczne

Algorytm odbić w tym systemie bazuje na **cube mapping** - technice renderowania, która wykorzystuje sześcienną mapę tekstur do symulacji odbić środowiska.

### 1.2 Implementacja w `utils.py`

#### Normalizacja wektora do długości 1 - Funkcja `normalize(v)` 
```python
def normalize(v):
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length == 0:
        return [0, 0, 0]
    return [v[0] / length, v[1] / length, v[2] / length]
```

**Proces:**
1. Oblicza długość wektora używając wzoru Euklidesa: `√(x² + y² + z²)`
2. Sprawdza czy długość nie jest zerowa (zabezpieczenie przed dzieleniem przez zero)
3. Dzieli każdy komponent przez długość wektora

#### Obliczenie wektora odbicja - Funkcja `reflect(incident, normal)`
```python
def reflect(incident, normal):
    dot = sum(i * n for i, n in zip(incident, normal))
    return [i - 2 * dot * n for i, n in zip(incident, normal)]
```

**Proces:**
1. Oblicza iloczyn skalarny wektora padającego i normalnej: `dot = incident · normal`
2. Stosuje wzór odbicia: `reflected = incident - 2 * (incident · normal) * normal`

**Wzór matematyczny:**
```
R = I - 2(I · N)N
gdzie:
- R = wektor odbicia
- I = wektor padający
- N = wektor normalny powierzchni
```

### 1.3 Proces generowania odbicia

Dla każdego wierzchołka obiektu:
1. **Obliczenie wektora widoku**
2. **Odwrócenie wektora widoku** 
3. **Wzór odbicia** 
4. **Wykorzystanie wynikowego wektora odbicia** 

## 2. Cube Map - struktura tekstur

### 2.1 Orientacja ścian
```
POSITIVE_X (px.jpg): Prawa ściana
NEGATIVE_X (nx.jpg): Lewa ściana
POSITIVE_Y (py.jpg): Górna ściana
NEGATIVE_Y (ny.jpg): Dolna ściana
POSITIVE_Z (pz.jpg): Przednia ściana
NEGATIVE_Z (nz.jpg): Tylna ściana
```

### 2.2 Próbkowanie
Wektor odbicia (3D) jest używany jako współrzędna tekstury, wskazując kierunek na sześcianie. OpenGL automatycznie:
1. Znajduje dominującą oś wektora
2. Wybiera odpowiednią ścianę cube mapy
3. Oblicza współrzędne UV na tej ścianie
4. Próbkuje kolor z tekstury

