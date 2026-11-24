"""
Script para generar el dataset original de ventas de videojuegos físicos y digitales:
data/videojuegos_ventas_original.csv
Incluye >= 900 filas, 11 variables y anomalías controladas (nulos, duplicados, negativos).
"""

import os
import random
import numpy as np
import pandas as pd

def generate_videojuegos_dataset():
    np.random.seed(42)
    random.seed(42)

    titulos_base = [
        ("Grand Theft Auto VI", "Acción", "Take-Two"),
        ("Call of Duty: Modern Warfare III", "Shooter", "Activision"),
        ("EA Sports FC 24", "Deportes", "EA Sports"),
        ("The Legend of Zelda: Tears of the Kingdom", "Aventura", "Nintendo"),
        ("Super Mario Bros. Wonder", "Plataformas", "Nintendo"),
        ("Marvel's Spider-Man 2", "Acción", "Sony Interactive"),
        ("Elden Ring", "RPG", "Bandai Namco"),
        ("Hogwarts Legacy", "Aventura", "Warner Bros"),
        ("Baldur's Gate 3", "RPG", "Larian Studios"),
        ("Cyberpunk 2077: Phantom Liberty", "RPG", "CD Projekt"),
        ("Diablo IV", "RPG", "Blizzard"),
        ("Starfield", "RPG", "Bethesda"),
        ("Final Fantasy XVI", "RPG", "Square Enix"),
        ("Resident Evil 4 Remake", "Acción", "Capcom"),
        ("Street Fighter 6", "Peleas", "Capcom"),
        ("Mortal Kombat 1", "Peleas", "Warner Bros"),
        ("Alan Wake 2", "Aventura", "Epic Games"),
        ("Armored Core VI", "Acción", "Bandai Namco"),
        ("Lies of P", "RPG", "Neowiz"),
        ("Forza Motorsport", "Carreras", "Xbox Game Studios"),
        ("Gran Turismo 7", "Carreras", "Sony Interactive"),
        ("God of War Ragnarök", "Acción", "Sony Interactive"),
        ("Horizon Forbidden West", "Aventura", "Sony Interactive"),
        ("Halo Infinite", "Shooter", "Xbox Game Studios"),
        ("Minecraft Legends", "Estrategia", "Mojang"),
        ("Sea of Stars", "RPG", "Sabotage Studio"),
        ("Dave the Diver", "Indie", "Mintrocket"),
        ("Cocoon", "Indie", "Annapurna"),
        ("Hollow Knight: Silksong", "Indie", "Team Cherry"),
        ("Hades II", "Indie", "Supergiant"),
        ("Dead Space Remake", "Acción", "EA"),
        ("Assassin's Creed Mirage", "Aventura", "Ubisoft"),
        ("The Crew Motorfest", "Carreras", "Ubisoft"),
        ("Payday 3", "Shooter", "Deep Silver"),
        ("Lord of the Rings: Gollum", "Aventura", "Daedalic"),
        ("Redfall", "Shooter", "Bethesda"),
        ("Forspoken", "Acción", "Square Enix"),
        ("Skull and Bones", "Aventura", "Ubisoft"),
        ("Suicide Squad: Kill the Justice League", "Acción", "Warner Bros"),
        ("Star Wars Jedi: Survivor", "Aventura", "EA"),
        ("NBA 2K24", "Deportes", "2K Games"),
        ("Madden NFL 24", "Deportes", "EA Sports"),
        ("WWE 2K23", "Deportes", "2K Games"),
        ("Mario Kart 8 Deluxe", "Carreras", "Nintendo"),
        ("Super Smash Bros. Ultimate", "Peleas", "Nintendo"),
        ("Pokémon Escarlata y Púrpura", "RPG", "Nintendo"),
        ("Metroid Prime Remastered", "Aventura", "Nintendo"),
        ("Pikmin 4", "Estrategia", "Nintendo"),
        ("Xenoblade Chronicles 3", "RPG", "Nintendo"),
        ("Fire Emblem Engage", "Estrategia", "Nintendo"),
    ]

    plataformas = ["PlayStation 5", "PlayStation 4", "Xbox Series X/S", "Xbox One", "Nintendo Switch", "PC"]
    regiones_prioritarias = ["Norteamérica", "Europa", "Japón", "Latinoamérica", "Global"]

    data = []
    n_registros = 920

    for i in range(1, n_registros + 1):
        # Elegir o combinar nombres para crear variedad
        base = random.choice(titulos_base)
        sufijo = f"Edición {random.choice(['Estándar', 'Deluxe', 'Coleccionista', 'Digital Gold', 'Temporada', 'GOTY'])}"
        titulo = f"{base[0]} - {sufijo}" if i > 50 else base[0]
        genero = base[1]
        distribuidora = base[2]
        plataforma = random.choice(plataformas)
        anio = random.choice([2019, 2020, 2021, 2022, 2023, 2024])

        # Definir 4 perfiles arquetípicos para el negocio:
        # Perfil 1: Blockbusters / Superventas masivas (altas físicas y digitales)
        # Perfil 2: Éxitos Digitales e Indies (altas digitales, bajas físicas)
        # Perfil 3: Éxitos de Consola / Físico fuerte (altas físicas, moderadas digitales)
        # Perfil 4: Fracasos comerciales o títulos de nicho bajo (bajas en ambos)
        perfil = np.random.choice([1, 2, 3, 4], p=[0.20, 0.35, 0.20, 0.25])

        if perfil == 1: # Blockbuster
            ventas_fis = round(float(np.random.normal(8.5, 2.5)), 2)
            ventas_dig = round(float(np.random.normal(12.0, 3.5)), 2)
            precio = round(float(np.random.choice([59.99, 69.99, 79.99])), 2)
            calif = int(np.clip(np.random.normal(88, 5), 75, 98))
            horas = int(np.clip(np.random.normal(45, 15), 15, 120))
        elif perfil == 2: # Éxito Digital / Indie / Shooter online
            ventas_fis = round(float(np.clip(np.random.normal(0.6, 0.4), 0.05, 2.0)), 2)
            ventas_dig = round(float(np.random.normal(7.8, 2.2)), 2)
            precio = round(float(np.random.choice([19.99, 29.99, 39.99, 49.99])), 2)
            calif = int(np.clip(np.random.normal(82, 6), 68, 95))
            horas = int(np.clip(np.random.normal(30, 20), 8, 100))
        elif perfil == 3: # Físico fuerte (Nintendo / Coleccionistas)
            ventas_fis = round(float(np.random.normal(6.5, 1.8)), 2)
            ventas_dig = round(float(np.random.normal(2.5, 1.0)), 2)
            precio = round(float(np.random.choice([49.99, 59.99, 69.99])), 2)
            calif = int(np.clip(np.random.normal(84, 5), 72, 96))
            horas = int(np.clip(np.random.normal(35, 12), 12, 80))
        else: # Fracaso comercial o bajo rendimiento
            ventas_fis = round(float(np.clip(np.random.normal(0.4, 0.3), 0.01, 1.2)), 2)
            ventas_dig = round(float(np.clip(np.random.normal(0.5, 0.4), 0.02, 1.5)), 2)
            precio = round(float(np.random.choice([39.99, 49.99, 59.99, 69.99])), 2)
            calif = int(np.clip(np.random.normal(54, 10), 30, 68))
            horas = int(np.clip(np.random.normal(18, 8), 5, 40))

        ventas_fis = max(0.01, ventas_fis)
        ventas_dig = max(0.02, ventas_dig)
        ventas_tot = round(ventas_fis + ventas_dig, 2)

        data.append({
            "id_juego": f"GAME-{i:04d}",
            "titulo": titulo,
            "genero": genero,
            "plataforma": plataforma,
            "distribuidora": distribuidora,
            "anio_lanzamiento": anio,
            "ventas_fisicas_millones": ventas_fis,
            "ventas_digitales_millones": ventas_dig,
            "ventas_totales_millones": ventas_tot,
            "precio_lanzamiento_usd": precio,
            "calificacion_critica": calif,
            "horas_juego": horas
        })

    df = pd.DataFrame(data)

    # Introducir imperfecciones controladas para evidenciar proceso de minería:
    # 1. 8 duplicados exactos
    indices_dup = [12, 45, 102, 230, 315, 450, 600, 750]
    duplicados = df.iloc[indices_dup].copy()
    df = pd.concat([df, duplicados], ignore_index=True)

    # 2. Valores nulos controlados en variables clave
    indices_nulos_precio = [20, 85, 190, 340, 520, 710]
    df.loc[indices_nulos_precio, "precio_lanzamiento_usd"] = np.nan

    indices_nulos_calif = [35, 140, 280, 490, 680, 830]
    df.loc[indices_nulos_calif, "calificacion_critica"] = np.nan

    indices_nulos_dig = [50, 210, 400, 610, 790]
    df.loc[indices_nulos_dig, "ventas_digitales_millones"] = np.nan

    # 3. Valores negativos causados por errores humanos de captura
    df.loc[77, "precio_lanzamiento_usd"] = -59.99
    df.loc[188, "ventas_fisicas_millones"] = -2.50

    os.makedirs("data", exist_ok=True)
    out_path = "data/videojuegos_ventas_original.csv"
    df.to_csv(out_path, index=False)
    print(f"Dataset original creado: {out_path} con {len(df)} filas y {len(df.columns)} columnas.")

if __name__ == "__main__":
    generate_videojuegos_dataset()
