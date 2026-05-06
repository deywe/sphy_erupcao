# Solar Eruption - Harpia Model

**A physically-based solar eruption simulation with cryptographic integrity verification.**

---

## Overview

This project simulates a **solar eruption** on a dynamic grid, inspired by the **Harpia Phase Engineering** model. 

Each frame is cryptographically signed with **SHA256**, allowing complete data integrity verification during visualization.

---

## Features

- Realistic solar surface simulation with wave propagation and shockwave
- Per-frame **SHA256** digital signature
- Real-time integrity validation during playback
- Efficient storage using Apache Parquet format
- Interactive 3D visualization with Ursina Engine

---

## Requirements

### Python Packages
```bash
python >= 3.8

pip install ursina numpy pandas pyarrow hashlib

Main Dependencies:ursina — 3D rendering and visualization
numpy — Numerical computations and vertex manipulation
pandas — Data handling
pyarrow — Reading and writing Parquet files
hashlib — (Built-in) SHA256 signature verification

Repository Contentssphy_erupcao_gerador.py — Headless dataset generator (creates signed Parquet)
sphy_erupcao_vizualizer.py — Visualization player with SHA256 validation
erupcao_solar.parquet — Pre-generated dataset (800 frames)

How to Use1. Generate the Dataset (optional)bash

python3 sphy_erupcao_gerador.py

2. Run the Visualizerbash

python3 sphy_erupcao_vizualizer.py

ControlsR → Restart animation
ESC → Quit application
Mouse + WASD / Arrow Keys → Move camera (EditorCamera)

Technical DetailsGrid Resolution: 60 × 60 vertices
Total Frames: 800
File Format: Apache Parquet (Zstd compression)
Integrity Protection: SHA256 per frame
Physics: Base oscillation + Gaussian shockwave

AuthorDeywe Okabe
Harpia Quantum DeeptechProject developed under "Coerência Gravitica" research.

