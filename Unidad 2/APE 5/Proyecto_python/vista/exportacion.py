"""Exportación opcional de CSV y gráficas SVG sin bibliotecas externas."""
import csv
from pathlib import Path
from modelo.generador import M


def grafica_svg(r):
    puntos = " ".join(f"{70+i*880/max(1,len(r.valores)-1):.3f},{350-x/M*280:.3f}"
                      for i, x in enumerate(r.valores))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 430">
<rect width="1000" height="430" fill="white"/>
<g font-family="sans-serif" font-size="16" fill="#172b4d">
<text x="70" y="30">LCG: semilla {r.semilla}, {len(r.valores)} observaciones</text>
<text x="15" y="65">U(n)</text><text x="38" y="76">1</text>
<text x="38" y="355">0</text><text x="70" y="380">1</text>
<text x="925" y="380">{len(r.valores)}</text><text x="440" y="410">Observación n</text></g>
<path d="M70 70 V350 H950" fill="none" stroke="#172b4d"/>
<polyline points="{puntos}" fill="none" stroke="#2463b4" stroke-width="0.6"/>
</svg>'''


def exportar(resultados, carpeta):
    carpeta = Path(carpeta)
    nombres = [carpeta / 'secuencias_python.csv'] + [
        carpeta / f"secuencia_python_{i}_semilla_{r.semilla}.svg"
        for i, r in enumerate(resultados, 1)]
    if any(p.exists() for p in nombres):
        raise FileExistsError("Ya existen resultados en esa carpeta. Elige otra carpeta.")
    carpeta.mkdir(parents=True, exist_ok=True)
    a, b = resultados
    with nombres[0].open('x', encoding='utf-8', newline='') as archivo:
        escritor = csv.writer(archivo, lineterminator='\n')
        escritor.writerow(['n', f"X_semilla_{a.semilla}", f"U_semilla_{a.semilla}",
                           f"X_semilla_{b.semilla}", f"U_semilla_{b.semilla}"])
        for i, (x, y) in enumerate(zip(a.valores, b.valores), 1):
            escritor.writerow([i, x, f'{x/M:.12f}', y, f'{y/M:.12f}'])
    for nombre, r in zip(nombres[1:], resultados):
        with nombre.open('x', encoding='utf-8') as archivo:
            archivo.write(grafica_svg(r))
    print(f"CSV y gráficas SVG guardados en: {carpeta.resolve()}")
