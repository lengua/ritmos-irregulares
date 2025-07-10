
mds = [
    "PAGINA_VACIA.md",
    # "00-1 - Dedicatoria.md",
    "00 - Indice figuras y cuadros.md",
    "00-2 - Agradecimientos.md",
    "00-3 - Prefacio.md",
    "00-4 - Herramientas.md",
    "01 - Archipiélago colonial - La modernidad no nació en el Caribe.md",
    "02 - La voz es el centro de toda la música.md",
    "03 - La música juega con los ciclos sonoros.md",
    "04 - La velocidad de los ciclos en el ritmo.md",
    "05 - Las Claves Rítmicas (version 3).md",
    "06 - Unidades de medida de ciclos de tiempo.md",
    "07 - Los primeros números del ritmo.md",
    "08 - Las claves rítmicas simples.md",
    "09 - Claves rítmicas compuestas - Concatenar dos o más claves.md",
    "10 - Claves polirrítmicas - Superponer dos o más claves (versión 2).md",
    "11 - Las Claves de Paso.md",
    "12 - El Melisma Rítmico - El swing y el feel entre métricas.md",
    "13 - Análisis de ritmos del mundo real con el cifrado rítmico.md",
    "14 - Composición y Estrategias Creativas.md",
    "20 - Imagen separadora.md",
    "26 - Apéndice I - Fundamentación Matemática del Espacio de las Claves.md",
    "27 - Apéndice II - Guía de uso de la calculadora de Claves Rítmicas.md",
    "30 - Glosario.md",
    "25 - Bibliografia.md",
    "40 - Indice analitico.md",
    "49 - Colofon.md",
    "50 - Contraportada.md",
    # "20 - Postfacio 1 - Las Claves y el Baile.md",
    # "21 - Postfacio 2 - Miedo a la originalidad.md",
]

# joiner = '<div style="page-break-after: always"></div>\n'
joiner = '\\pagebreak\n'
# joiner = '\n'

output_file = "_FULL_DUMMY.md"

with open(output_file, "w", encoding="utf-8") as outfile:
    for i, md_file in enumerate(mds):
        with open(md_file, "r", encoding="utf-8") as infile:
            outfile.write(infile.read())
        if i < len(mds) - 1:
            outfile.write('\n' + joiner + '\n')

print(f"All files joined into {output_file}")