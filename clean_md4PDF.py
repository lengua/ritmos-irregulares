import os
import argparse

# Define your replacements here
replacements = {
    "“": '"',
    "”": '"',
    "—": "-",
    "–": "-",
    "‘": "'",
    "’": "'",
    "…": "...",
    "«": '"',
    "»": '"',
    "𝅘𝅥𝅮": "♪",
    "♩": "♩",
    # "𝄟": "𝄞",
    "∼": "~",
    # ":": "&colon;",
    
    "♪": "![♪](./octavenote.png){height=\"12pt\"}",
    "♩": "![♩](./quarternote.png){height=\"12pt\"}",
    "𝅗𝅥": "![𝅗𝅥](./halfnote.png){height=\"12pt\"}",
    "𝅝": "![𝅝](./wholenote.png){height=\"12pt\"}",
    
    # "♪": "&#9834;",
    # "♩": "&#9833;",
    # "𝅗𝅥": "&#119070;",
    # "𝅝": "&#119071;",
    # "𝄞": "&#x1D11E;",
    # "𝄞": "&MUSICSYMB;",
    
    "₂": "&#x2082;",
    "₀": "&#x2080;",
    "ᵣ": "&#x1D63;",
    "₋": "&#8331;",
    "₁": "&#x2081;",
    "∈": "&isin;",
    "ʳ": "&#x02B3;",
    "⊕": "&oplus;",
    "∧": "&and;",
    "ₚ": "&#x209A;",
    "ⱼ": "&#x2C7C;",
    "∪": "&cup;",
    "₌": "&#8332;",
    "≠": "&ne;",
}

def replace_line(line, replacements):
    for old, new in replacements.items():
        line = line.replace(old, new)
    return line

def process_file(input_path, replacements):
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_filtrado{ext}"

    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            new_line = replace_line(line, replacements)
            outfile.write(new_line)
    print(f"Archivo filtrado: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reemplazar caracteres en un archivo markdown")
    parser.add_argument("input_file", help="Ruta del archivo markdown de entrada")
    args = parser.parse_args()
    process_file(args.input_file, replacements)