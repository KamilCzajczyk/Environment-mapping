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

Algorytm odbić w tym systemie bazuje na **cube mapping** - technice renderowania, która wykorzystuje sześcienny mape tekstur do symulacji odbić środowiska.

### 1.2 Implementacja w `utils.py`

#### Funkcja `normalize(v)`
```python
def normalize(v):
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length == 0:
        return [0, 0, 0]
    return [v[0] / length, v[1] / length, v[2] / length]
```

**Cel:** Normalizacja wektora do długości 1
**Proces:**
1. Oblicza długość wektora używając wzoru Euklidesa: `√(x² + y² + z²)`
2. Sprawdza czy długość nie jest zerowa (zabezpieczenie przed dzieleniem przez zero)
3. Dzieli każdy komponent przez długość wektora

#### Funkcja `reflect(incident, normal)`
```python
def reflect(incident, normal):
    dot = sum(i * n for i, n in zip(incident, normal))
    return [i - 2 * dot * n for i, n in zip(incident, normal)]
```

**Cel:** Oblicza wektor odbicia na podstawie wektora padającego i normalnej powierzchni
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
1. **Oblicz wektor widoku** - od wierzchołka do kamery
2. **Odwróć wektor widoku** - aby uzyskać wektor "padający"
3. **Zastosuj wzór odbicia** - używając normalnej powierzchni
4. **Użyj wektora odbicia** - jako współrzędnych tekstury dla cube mapy

## 2. Renderowanie obiektów

### 2.1 Struktura renderowania

Wszystkie obiekty używają tego samego schematu:
1. Włączenie cube map tekstury
2. Obliczenie współrzędnych odbicia dla każdego wierzchołka
3. Renderowanie geometrii z odpowiednimi współrzędnymi tekstury

### 2.2 Funkcja `draw_reflective_cube()`

```python
def draw_reflective_cube(cube_map_id, camera_pos):
    glPushMatrix()
    glEnable(GL_TEXTURE_CUBE_MAP)
    glBindTexture(GL_TEXTURE_CUBE_MAP, cube_map_id)
    
    # Definicja geometrii
    size = 1.5
    vertices = [
        # 6 ścian sześcianu, każda jako 4 wierzchołki
        [[-size, -size, size], [size, -size, size], [size, size, size], [-size, size, size]], # front
        [[size, -size, -size], [-size, -size, -size], [-size, size, -size], [size, size, -size]], # back
        # ... pozostałe ściany
    ]
    normals = [[0,0,1], [0,0,-1], [0,1,0], [0,-1,0], [1,0,0], [-1,0,0]]
    
    # Renderowanie
    glBegin(GL_QUADS)
    for face_verts, normal in zip(vertices, normals):
        glNormal3fv(normal)
        for vertex in face_verts:
            # Oblicz wektor widoku
            view_vec = utils.normalize([camera_pos[i] - vertex[i] for i in range(3)])
            # Oblicz wektor odbicia
            refl_vec = utils.reflect([-v for v in view_vec], normal)
            # Użyj jako współrzędne tekstury
            glTexCoord3fv(refl_vec)
            glVertex3fv(vertex)
    glEnd()
```

**Kluczowe elementy:**
- **Geometria:** Sześcian o krawędzi 3.0 (±1.5)
- **Normalne:** Stałe dla każdej ściany
- **Odbicia:** Obliczane per wierzchołek dla każdej ściany

### 2.3 Funkcja `draw_reflective_sphere()`

```python
def draw_reflective_sphere(cube_map_id, camera_pos):
    glPushMatrix()
    glTranslatef(3, 0, 0)  # Przesunięcie pozycji
    
    # Parametry sfery
    radius, slices, stacks = 1.2, 32, 16
    
    # Generowanie geometrii sferycznej
    for i in range(stacks):
        lat1 = math.pi * (-0.5 + float(i) / stacks)      # Szerokość geograficzna 1
        lat2 = math.pi * (-0.5 + float(i + 1) / stacks)  # Szerokość geograficzna 2
        
        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * math.pi * float(j) / slices  # Długość geograficzna
            
            for lat in [lat1, lat2]:
                # Współrzędne sferyczne → kartezjańskie
                x = radius * math.cos(lat) * math.cos(lng)
                y = radius * math.sin(lat)
                z = radius * math.cos(lat) * math.sin(lng)
                
                # Pozycja w świecie (z przesunięciem)
                world_pos = [x + 3, y, z]
                # Normalna = znormalizowana pozycja lokalna
                normal = utils.normalize([x, y, z])
                # Wektor widoku
                view_vec = utils.normalize([camera_pos[k] - world_pos[k] for k in range(3)])
                # Wektor odbicia
                refl_vec = utils.reflect([-v for v in view_vec], normal)
                
                glNormal3fv(normal)
                glTexCoord3fv(refl_vec)
                glVertex3f(x, y, z)
        glEnd()
```

**Charakterystyka:**
- **Geometria:** Sfera o promieniu 1.2, pozycja (3, 0, 0)
- **Tesselacja:** 32 slices × 16 stacks
- **Normalne:** Obliczane jako znormalizowane współrzędne lokalne
- **Renderowanie:** QUAD_STRIP dla efektywności

### 2.4 Funkcja `draw_reflective_torus()`

```python
def draw_reflective_torus(cube_map_id, camera_pos):
    glPushMatrix()
    torus_pos = [-3.0, 0.0, 0.0]
    glTranslatef(torus_pos[0], torus_pos[1], torus_pos[2])
    
    # Parametry torusa
    major_radius = 1.0  # Promień główny
    minor_radius = 0.4  # Promień mały
    rings = 40          # Pierścienie
    sides = 20          # Boki
    
    for i in range(rings):
        u1 = (i / rings) * 2 * math.pi
        u2 = ((i + 1) / rings) * 2 * math.pi
        
        glBegin(GL_QUAD_STRIP)
        for j in range(sides + 1):
            v = (j / sides) * 2 * math.pi
            
            # Dla każdego z dwóch punktów (u1, u2)
            for u in [u1, u2]:
                # Współrzędne torusa
                x = (major_radius + minor_radius * math.cos(v)) * math.cos(u)
                y = minor_radius * math.sin(v)
                z = (major_radius + minor_radius * math.cos(v)) * math.sin(u)
                
                # Normalna torusa
                nx = math.cos(v) * math.cos(u)
                ny = math.sin(v)
                nz = math.cos(v) * math.sin(u)
                normal = utils.normalize([nx, ny, nz])
                
                # Pozycja w świecie
                world_pos = [x + torus_pos[0], y + torus_pos[1], z + torus_pos[2]]
                # Wektor widoku i odbicia
                view_vec = utils.normalize([camera_pos[k] - world_pos[k] for k in range(3)])
                refl_vec = utils.reflect([-val for val in view_vec], normal)
                
                glNormal3fv(normal)
                glTexCoord3fv(refl_vec)
                glVertex3f(x, y, z)
        glEnd()
```

**Charakterystyka:**
- **Geometria:** Torus o promieniu głównym 1.0 i małym 0.4, pozycja (-3, 0, 0)
- **Tesselacja:** 40 rings × 20 sides
- **Równania parametryczne torusa:**
  - `x = (R + r*cos(v)) * cos(u)`
  - `y = r * sin(v)`
  - `z = (R + r*cos(v)) * sin(u)`
- **Normalne:** Obliczane analitycznie z pochodnych parametrycznych

### 2.5 Funkcja `draw_skybox()`

```python
def draw_skybox(cube_map_id, camera_pos):
    glPushMatrix()
    # Wyłączenie testów głębi i culling
    glDisable(GL_CULL_FACE)
    glDepthMask(GL_FALSE)
    glDepthFunc(GL_LEQUAL)
    glDisable(GL_LIGHTING)
    
    # Przesunięcie skybox do pozycji kamery
    glTranslatef(camera_pos[0], camera_pos[1], camera_pos[2])
    
    # Renderowanie sześcianu
    s = 100.0  # Duży rozmiar
    # Współrzędne wierzchołków i tekstury
    v = [[-s,-s,s], [s,-s,s], [s,s,s], [-s,s,s], [-s,-s,-s], [s,-s,-s], [s,s,-s], [-s,s,-s]]
    t = [[-1,-1,1], [1,-1,1], [1,1,1], [-1,1,1], [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1]]
    
    # Renderowanie 6 ścian
    faces = [(0,1,2,3), (5,4,7,6), (3,2,6,7), (4,5,1,0), (1,5,6,2), (4,0,3,7)]
    for face in faces:
        for j in face:
            glTexCoord3f(t[j][0], t[j][1], t[j][2])
            glVertex3f(v[j][0], v[j][1], v[j][2])
    
    # Przywrócenie stanów
    glEnable(GL_LIGHTING)
    glDepthFunc(GL_LESS)
    glDepthMask(GL_TRUE)
    glEnable(GL_CULL_FACE)
    glPopMatrix()
```

**Kluczowe elementy:**
- **Pozycja:** Zawsze w centrum kamery (iluzja nieskończonej odległości)
- **Rozmiar:** 200×200×200 jednostek
- **Współrzędne tekstury:** Bezpośrednio kierunki 3D
- **Stany OpenGL:** Specjalne ustawienia dla tła
## 3. Cube Map - struktura tekstur

### 3.1 Orientacja ścian
```
POSITIVE_X (px.jpg): Prawa ściana
NEGATIVE_X (nx.jpg): Lewa ściana
POSITIVE_Y (py.jpg): Górna ściana
NEGATIVE_Y (ny.jpg): Dolna ściana
POSITIVE_Z (pz.jpg): Przednia ściana
NEGATIVE_Z (nz.jpg): Tylna ściana
```

### 3.2 Próbkowanie
Wektor odbicia (3D) jest używany jako współrzędna tekstury, wskazując kierunek na sześcianie. OpenGL automatycznie:
1. Znajduje dominującą oś wektora
2. Wybiera odpowiednią ścianę cube mapy
3. Oblicza współrzędne UV na tej ścianie
4. Próbkuje kolor z tekstury





### Modyfikacja parametrów
Wszystkie kluczowe parametry znajdują się w `config.py`:
- Prędkość kamery
- Czułość myszy
- Rozdzielczość
- Kolory tła
- Parametry projekcji
