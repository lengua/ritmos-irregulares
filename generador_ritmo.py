from PIL import Image, ImageDraw, ImageFont
import os # For path joining
import re
import sys
import json

# --- Configuration Constants ---
IMG_HEIGHT = 140
Y_CENTER = IMG_HEIGHT // 2
MAIN_LINE_THICKNESS = 1
SHOW_MAIN_LINE = True  # Mostrar/ocultar la línea principal horizontal
MAIN_LINE_PRE = 4 # Espacio antes de la línea principal
MAIN_LINE_POST = 14 # Espacio después de la línea principal

# Buenas letras x tamaño:
# 50 =>
#   5
# 55 =>
#   0, 1, 9, 16
# 60 => 
#   5, 19
# 75 =>
#   10
# 155 =>
#   7
letratam = {
    0: 55,
    1: 65,
    5: 55,
    7: 155,
    9: 55,
    10: 65,
    16: 55,
    19: 60,
}

if(len(sys.argv)>1 and sys.argv[1]):
    LETRA_NUMERO = int(sys.argv[1])
else:
    LETRA_NUMERO = 19

if LETRA_NUMERO not in letratam.keys():
    TIME_SIG_FONT_SIZE = 65
else:
    TIME_SIG_FONT_SIZE = letratam[LETRA_NUMERO]

FIGURE_VERTICAL_OFFSET = 20  # Ajusta este valor para subir/bajar las figuras musicales
FIGURE_TARGET_HEIGHT = 100  # Altura deseada para las figuras musicales (ajusta a tu gusto)

# Vertical gap between the main horizontal line and the time signature numbers
TIME_SIG_VERTICAL_PADDING_FROM_LINE = 0

SPACE_AFTER_CLOSING_BAR = 10

TARGET_NOTE_HEAD_DIAMETER = 36 # Desired visual diameter for note heads

DOT_DIAMETER = 12       # Augmentation dot
REPEAT_DOT_DIAMETER = 8 # Dots for repeat bars
# Vertical offset for repeat dots from Y_CENTER, relative to desired note head size
REPEAT_DOT_VERTICAL_OFFSET = TARGET_NOTE_HEAD_DIAMETER * 0.35

# --- Bar Lines ---
BAR_THICK_WIDTH = 8
BAR_THIN_WIDTH = 2
BAR_SPACING = [0,0,2,8]
BAR_HEIGHT = 100

# --- Horizontal Spacing ---
MARGIN_X = 15           # Reduced for a more compact look
SPACE_AFTER_TIME_SIG = 15
SPACE_BEFORE_START_BAR_DOTS = 6 # Reduced
SPACE_AFTER_START_BAR_DOTS = 26
SPACE_AFTER_START_BAR = 0 # Reduced

SPACE_BETWEEN_NOTES = 28 # Reduced
SPACE_NOTE_TO_AUG_DOT = 0

SPACE_BEFORE_END_BAR = 18 # Reduced
SPACE_END_BAR_DOTS_TO_BAR = 8

# --- Musical Figure Definitions ---
FIGURE_DEFINITIONS = {
    '1': 'small-octavenote.png',
    '2': 'small-quarternote.png',
    '3': 'small-quarternote-dot.png',
    '4': 'small-halfnote.png',
    '5': 'small-quarternote-quarternote-dot.png',
    '6': 'small-halfnote-dot.png',
    '7': 'small-halfnote-dot-dot.png',
    '8': 'small-wholenote.png',
}
fonts = [
    "./fonts/proclamate heavy.ttf",
    "./fonts/PyriformTonesNF.ttf",
    "./fonts/Quickier_Demo.ttf",
    "./fonts/RegencyScriptFLF.ttf",
    "./fonts/Respective_2.0.ttf",
    "./fonts/Ribeye-Regular.ttf",
    "./fonts/1645 Old Spanish.ttf",
    "./fonts/Adine Kirnberg.ttf",
    "./fonts/ALBATROB.TTF",
    "./fonts/Andada-Regular.ttf",
    "./fonts/AnnabelScript.ttf",
    "./fonts/BiedermeierKursiv.ttf",
    "./fonts/BodoniFLF-Bold.ttf",
    "./fonts/CenteriaScriptDemo.otf",
    "./fonts/Champignon.otf",
    "./fonts/CoelacanthDisplaySemibd.otf",
    "./fonts/EmilysCandy-Regular.ttf",
    "./fonts/Estrela Fulguria 1748.ttf",
    "./fonts/exmouth_.ttf",
    "./fonts/FrankRuhlLibre-Bold.ttf",
    "./fonts/Goudament.ttf",
    "./fonts/GoudyMediaeval-DemiBold.ttf",
    "./fonts/hacjiuza.otf",
    "./fonts/hacjiuza.ttf",
    "./fonts/Hultog.ttf",
    "./fonts/LaurenScript.ttf",
    "./fonts/Leadword-Regular.otf",
    "./fonts/LEVEFD__.TTF",
    "./fonts/LibreCaslonText-Regular.ttf",
    "./fonts/LouisaCP.otf",
    "./fonts/Mayflower Antique.ttf",
    "./fonts/PackardAntique-Bold.ttf",
    "./fonts/Primitive.ttf",
]

FONT_PATH_TEXT = fonts[LETRA_NUMERO]
try:
    # Using the same size for numerator and denominator for better balance
    time_sig_font = ImageFont.truetype(FONT_PATH_TEXT, TIME_SIG_FONT_SIZE)
except IOError:
    print(f"ERROR: FONT '{FONT_PATH_TEXT}' no encontrada!")
    time_sig_font = ImageFont.load_default(TIME_SIG_FONT_SIZE)


# --- Cargar imagen de puntos de repetición ---
PUNTOS_IMG_PATH = os.path.join(os.path.dirname(__file__), "puntos.png")
try:
    PUNTOS_IMG = Image.open(PUNTOS_IMG_PATH).convert("RGBA")
except Exception as e:
    print(f"Error cargando puntos.png: {e}")
    PUNTOS_IMG = None


def get_text_bbox_width(draw_context, text, font, anchor_pos=(0,0), anchor_str="lt"):
    bbox = draw_context.textbbox(anchor_pos, text, font=font, anchor=anchor_str)
    return bbox[2] - bbox[0]

FIGURE_IMAGES = {}
for key, val in FIGURE_DEFINITIONS.items():
    img_path = os.path.join(os.path.dirname(__file__), val)
    try:
        FIGURE_IMAGES[key] = Image.open(img_path).convert("RGBA")
    except Exception as e:
        print(f"Error cargando imagen {img_path}: {e}")
        FIGURE_IMAGES[key] = None

def get_figure_width(fig_key):
    img = FIGURE_IMAGES.get(fig_key)
    if img:
        # Calcula el ancho proporcional al escalar la altura a FIGURE_TARGET_HEIGHT
        new_width = int(img.width * (FIGURE_TARGET_HEIGHT / img.height))
        return new_width
    return 0

def draw_note_glyph(draw_img, x_pos, fig_key, y_center):
    """
    Pega la imagen de la figura musical centrada verticalmente en y_center,
    ajustada por FIGURE_VERTICAL_OFFSET y escalada a FIGURE_TARGET_HEIGHT,
    manteniendo la proporción original.
    """
    img = FIGURE_IMAGES.get(fig_key)
    if img is None:
        return 0
    # Escalar manteniendo proporción
    if img.height != FIGURE_TARGET_HEIGHT:
        new_width = int(img.width * (FIGURE_TARGET_HEIGHT / img.height))
        img_resized = img.resize((new_width, FIGURE_TARGET_HEIGHT), Image.LANCZOS)
    else:
        img_resized = img
    y_top = int(y_center - img_resized.height // 2 + FIGURE_VERTICAL_OFFSET)
    draw_img.paste(img_resized, (int(x_pos), y_top), img_resized)
    return img_resized.width

def generate_music_snippet(numerador_compas, figuras_input, output_filename="musical_snippet.png"):
    # Cálculo del ancho total usando imágenes en vez de fuentes
    current_x_calc = MARGIN_X
    num_str = str(numerador_compas)
    den_str = "8"

    # Cálculo del ancho de la indicación de compás (sigue usando fuente)
    dummy_img = Image.new('RGB', (1, 1), 'white')
    dummy_draw = ImageDraw.Draw(dummy_img)
    num_w_calc = get_text_bbox_width(dummy_draw, num_str, time_sig_font)
    den_w_calc = get_text_bbox_width(dummy_draw, den_str, time_sig_font)
    time_sig_width_calc = max(num_w_calc, den_w_calc)
    current_x_calc += time_sig_width_calc + SPACE_AFTER_TIME_SIG
    current_x_calc += BAR_THICK_WIDTH + BAR_SPACING[0] + BAR_THIN_WIDTH
    current_x_calc += SPACE_BEFORE_START_BAR_DOTS + REPEAT_DOT_DIAMETER + SPACE_AFTER_START_BAR_DOTS
    current_x_calc += SPACE_AFTER_START_BAR

    num_figures = len(figuras_input)
    for i, fig_key in enumerate(figuras_input):
        if fig_key not in FIGURE_DEFINITIONS:
            # print(f"Advertencia: La figura '{fig_key}' no se reconoció durante el cálculo del ancho. Se omitirá.")
            continue
        fig_width_calc = get_figure_width(fig_key)
        current_x_calc += fig_width_calc
        # if FIGURE_DEFINITIONS[fig_key]['has_dot']:
        #     current_x_calc += SPACE_NOTE_TO_AUG_DOT
        if i < num_figures - 1:
            current_x_calc += SPACE_BETWEEN_NOTES
    del dummy_draw, dummy_img

    current_x_calc += SPACE_BEFORE_END_BAR
    current_x_calc += REPEAT_DOT_DIAMETER + SPACE_END_BAR_DOTS_TO_BAR
    current_x_calc += BAR_THIN_WIDTH + BAR_SPACING[1] + BAR_THICK_WIDTH
    current_x_calc += MARGIN_X
    current_x_calc += SPACE_AFTER_CLOSING_BAR  # Añadir margen derecho
    total_width = int(current_x_calc)

    img = Image.new('RGBA', (total_width, IMG_HEIGHT), 'white')
    draw = ImageDraw.Draw(img)

    # Línea principal horizontal
    if SHOW_MAIN_LINE:
        draw.line([(MAIN_LINE_PRE, Y_CENTER), (total_width-MAIN_LINE_POST, Y_CENTER)], fill='black', width=MAIN_LINE_THICKNESS)

    current_x_draw = MARGIN_X

    # --- Draw Time Signature ---
    num_actual_w = get_text_bbox_width(draw, num_str, time_sig_font)
    den_actual_w = get_text_bbox_width(draw, den_str, time_sig_font)
    num_x_offset = (time_sig_width_calc - num_actual_w) / 2
    den_x_offset = (time_sig_width_calc - den_actual_w) / 2

    # Numerador
    y_num_baseline = Y_CENTER - (MAIN_LINE_THICKNESS / 2) + 1 - TIME_SIG_VERTICAL_PADDING_FROM_LINE
    draw.text((current_x_draw + num_x_offset, y_num_baseline), num_str, font=time_sig_font, fill='black', anchor="ls")

    # Denominador
    y_den_top = Y_CENTER + (MAIN_LINE_THICKNESS / 2) + TIME_SIG_VERTICAL_PADDING_FROM_LINE
    draw.text((current_x_draw + den_x_offset, y_den_top), den_str, font=time_sig_font, fill='black', anchor="lt")
    current_x_draw += time_sig_width_calc + SPACE_AFTER_TIME_SIG

    # --- Draw Start Bar & Repeat Dots ---
    bar_y_start = Y_CENTER - BAR_HEIGHT // 2
    bar_y_end = Y_CENTER + BAR_HEIGHT // 2
    draw.line([(current_x_draw, bar_y_start), (current_x_draw, bar_y_end)], fill='black', width=BAR_THICK_WIDTH)
    current_x_draw += BAR_THICK_WIDTH + BAR_SPACING[2]
    draw.line([(current_x_draw, bar_y_start), (current_x_draw, bar_y_end)], fill='black', width=BAR_THIN_WIDTH)
    current_x_draw += BAR_THIN_WIDTH
    current_x_draw += SPACE_BEFORE_START_BAR_DOTS

    # Sustituir los puntos dibujados por la imagen
    pegar_puntos(img, current_x_draw, Y_CENTER)
    # Ajustar el avance en X según el ancho de la imagen de puntos
    if PUNTOS_IMG is not None:
        puntos_width = int(PUNTOS_IMG.width * ( (REPEAT_DOT_VERTICAL_OFFSET * 2 + REPEAT_DOT_DIAMETER * 2) / PUNTOS_IMG.height ))
        current_x_draw += puntos_width
    else:
        current_x_draw += REPEAT_DOT_DIAMETER
    current_x_draw += SPACE_AFTER_START_BAR_DOTS
    current_x_draw += SPACE_AFTER_START_BAR

    # --- Draw Musical Figures (usando imágenes PNG) ---
    for i, fig_key in enumerate(figuras_input):
        if fig_key not in FIGURE_DEFINITIONS:
            print(f"Advertencia: La figura '{fig_key}' no se reconoció durante el dibujo. Se omitirá.")
            continue
        actual_fig_width = draw_note_glyph(img, current_x_draw, fig_key, Y_CENTER)
        current_x_draw += actual_fig_width

        # if FIGURE_DEFINITIONS[fig_key]['has_dot']:
        #     current_x_draw += SPACE_NOTE_TO_AUG_DOT
        #     aug_dot_center_x = current_x_draw + DOT_DIAMETER / 2
        #     draw.ellipse([(aug_dot_center_x - DOT_DIAMETER/2, Y_CENTER - DOT_DIAMETER/2),
        #                   (aug_dot_center_x + DOT_DIAMETER/2, Y_CENTER + DOT_DIAMETER/2)], fill='black')
        #     current_x_draw += DOT_DIAMETER

        if i < num_figures - 1:
            current_x_draw += SPACE_BETWEEN_NOTES

    current_x_draw += SPACE_BEFORE_END_BAR

    # --- End Repeat Dots & Bar ---
    pegar_puntos(img, current_x_draw, Y_CENTER)
    if PUNTOS_IMG is not None:
        puntos_width = int(PUNTOS_IMG.width * ( (REPEAT_DOT_VERTICAL_OFFSET * 2 + REPEAT_DOT_DIAMETER * 2) / PUNTOS_IMG.height ))
        current_x_draw += puntos_width
    else:
        current_x_draw += REPEAT_DOT_DIAMETER
    current_x_draw += SPACE_END_BAR_DOTS_TO_BAR
    draw.line([(current_x_draw, bar_y_start), (current_x_draw, bar_y_end)], fill='black', width=BAR_THIN_WIDTH)
    current_x_draw += BAR_THIN_WIDTH + BAR_SPACING[3]
    draw.line([(current_x_draw, bar_y_start), (current_x_draw, bar_y_end)], fill='black', width=BAR_THICK_WIDTH)

    current_x_draw += SPACE_AFTER_CLOSING_BAR  # Añadir margen derecho

    try:
        img.save(output_filename)
        print(f"Imagen guardada como {output_filename}")
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")

def pegar_puntos(img, x, y_center):
    """
    Pega la imagen de puntos de repetición centrada verticalmente respecto a y_center.
    """
    if PUNTOS_IMG is None:
        return
    puntos_img = PUNTOS_IMG
    
    escala = 2
    # Escalar si es necesario para que coincida con el tamaño anterior
    target_height = int(REPEAT_DOT_VERTICAL_OFFSET * escala + REPEAT_DOT_DIAMETER * escala)
    if puntos_img.height != target_height:
        scale = target_height / puntos_img.height
        new_width = int(puntos_img.width * scale)
        puntos_img = puntos_img.resize((new_width, target_height), Image.LANCZOS)
    y_top = int(y_center - puntos_img.height // 2)
    img.paste(puntos_img, (int(x), y_top), puntos_img)

def explotarClave(clave):
    c = clave.strip()
    if len(c) < 1:
        return None, None
    else:
        l = 0
        for i in range(len(c)):
            l+=int(c[i])
        if l == 0:
            return None, None
        return l, c

def extraer_nombre_fuente(ruta):
    """
    Extrae el nombre de la fuente (sin extensión) de una ruta usando regex.
    Ejemplo: "./fonts/Ribeye-Regular.ttf" -> "Ribeye-Regular"
    """
    match = re.search(r'/([^/\\]+)\.[a-z]+$', ruta)
    if match:
        return match.group(1)
    return None

if __name__ == '__main__':
    print("Creando imágenes de claves musicales...")
    print("Font:",FONT_PATH_TEXT)
    
    try:
        with open("generador_claves.json", "r", encoding="utf-8") as f:
            test_claves = json.load(f)
    except Exception as e:
        print(f"Error cargando generador_claves.json: {e}")
        test_claves = ["221","3212"]
    
    total = 0
    for clave in test_claves:
        clave = explotarClave(clave)
        if clave[0] is None:
            print(f"Clave inválida: {clave} (saltando)")
            continue
        total+=1
        generate_music_snippet(
            numerador_compas=clave[0],
            figuras_input=clave[1],
            # output_filename="./claves_png/"+"clave_"+str(clave[0])+"."+''.join(clave[1])+"-"+str(LETRA_NUMERO)+"-"+extraer_nombre_fuente(FONT_PATH_TEXT)+".png"
            output_filename="./claves_png/"+"clave_"+str(clave[0])+"."+''.join(clave[1])+".png"
        )

    print("FIN. Se crearon",total,"claves")
    