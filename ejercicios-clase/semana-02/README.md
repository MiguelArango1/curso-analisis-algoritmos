# Semana 02 — Configuración del entorno de trabajo

## Entorno virtual

Desde la raíz del repositorio se creó y activó un entorno virtual único para todo el curso:

\`\`\`bash
python -m venv venv
venv\Scripts\Activate
\`\`\`

Se verificó con `pip list` que el entorno estaba vacío antes de instalar dependencias, y se agregó `venv/` al `.gitignore` de la raíz.

## Reproducir el entorno

Cualquier persona que clone este repositorio puede recrear el mismo entorno ejecutando, desde la raíz:

\`\`\`bash
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
\`\`\`

Esto instala exactamente las mismas versiones registradas en `requirements.txt` (generado con `pip freeze`), incluyendo `matplotlib`.

## Archivos de esta carpeta

- `refactor_pep8.py`: script de cálculo de promedio refactorizado con PEP 8 y type hints.
- `clasificador_anios.py`: ejercicio integrador que clasifica años bisiestos.