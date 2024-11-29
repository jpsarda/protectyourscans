import argparse
import os
import math  
from PIL import Image, ImageDraw, ImageFont
from unidecode import unidecode
from datetime import datetime


# pip3 install unidecode
# exple
# python3 watermark.py fake_document.jpg -p 'BANQUE VEUMAISSOUX'
# python3 watermark.py fake_document.jpg -p 'BANQUE VEUMAISSOUX' -lo 30 -fs 15

# Obtenir le chemin absolu du script
script_path = os.path.dirname(os.path.abspath(__file__))

def intersection_lignes(x1, y1, x2, y2, x3, y3, x4, y4):
    # Calcul des coefficients pour la ligne 1 et la ligne 2
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    # Vérifier si les lignes sont parallèles (si le déterminant est nul)
    if denom == 0:
        return None  # Les lignes sont parallèles et n'ont pas d'intersection

    # Calcul des coordonnées du point d'intersection
    x_inter = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    y_inter = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom

    return (x_inter, y_inter)


# Renvoie le un extraction du texte à partir de offset, de longueur length, et en bouclant (c'est à dire qu'on revient au caractère du début quand on arrive à la fin du texte)
def get_looped_text(text,offset,length):
    ret = ""
    # On ajoute un à un les caractères, on doit pouvoir optimiser ce algorithme en ajoutant des blocs entiers, mais la rapidité d'execution n'est pas un problème ici
    for i in range(length):
        ret = ret + text[offset:offset+1]
        offset += 1
        if offset >= len(text):
            offset = 0
    return ret, offset

def max_text_that_fits(text, offset, max_width, font):
    # Créer une image vide pour mesurer le texte
    image = Image.new('RGB', (int(max_width), 100), color='white')
    draw = ImageDraw.Draw(image)


    # On augmente petit à petit la taille du texte jusqu'à ce que la taille d'affichage du texte dépasse la max_width
    # On renvoie le texte précédant le dépassement de max_width, qui ne dépasse donc pas.
    # On renvoie au minimum un texte de 1 caractère, même si le texte dépasse la max_width.
    length = 1

    # On doit pouvoir améliorer les performances de cette algorithme en utilisant la dichotomie, mais la rapidité d'execution n'est pas un pb ici.
    while True:
        # Mesurer la largeur du texte
        text_loop , offset_loop = get_looped_text(text,offset,length)

        bbox = draw.textbbox((0, 0), text_loop, font=font)
        # La largeur et la hauteur du texte sont données par les dimensions du rectangle
        text_loop_width = bbox[2] - bbox[0]

        if text_loop_width > max_width and length>1:
            break;

        ret_text = text_loop 
        ret_offset = offset_loop

        length += 1
        

    return ret_text, ret_offset



def add_watermark(input_image_path, output_image_path, watermark_text, font_size, line_offset, angle, text_color, line_width, line_color, background_color):
    watermark_text = watermark_text.replace("\n", " ")
    watermark_text = watermark_text + " " #pour pouvoir boucler le texte
    watermark_text = unidecode(watermark_text)

    # Ouvrir l'image originale
    original_image = Image.open(input_image_path)
    # Obtenir les dimensions de l'image
    width, height = original_image.size

    print("Image size ",width,",",height)
    
    # Créer un objet ImageDraw
    draw = ImageDraw.Draw(original_image)

    if font_size < 0:
        font_size = int((width+height)/30)

    #font_size = 50
    line_gap = font_size + font_size * line_offset/100
    #angle = 70 #degres

    # Définir la couleur du texte (en utilisant RGBA pour transparence)
    #text_color = (255, 255, 255, 255)  # Blanc 
    #text_color = (200, 200, 200, 255)  
    #text_color = "#faaa"
    
    # Choisir une police et une taille pour le texte
    font = ImageFont.truetype(script_path+"/THEBOLDFONT-FREEVERSION-2023.ttf", font_size)  # Vous pouvez remplacer par une police spécifique

    #print(font)
    #print (watermark_text)

    x=0
    y=0

    cos = math.cos(angle*math.pi/180)
    sin = math.sin(angle*math.pi/180)

    xadd = cos * line_gap
    yadd = sin * line_gap

    # points définissant la ligne bordure gauche
    left_line_x1 = 0
    left_line_y1 = 0
    left_line_x2 = 0
    left_line_y2 = 1

    # points définissant la ligne bordure bas
    bottom_line_x1 = 0
    bottom_line_y1 = height
    bottom_line_x2 = 1
    bottom_line_y2 = height

    # points définissant la ligne bordure haute
    top_line_x1 = 0
    top_line_y1 = 0
    top_line_x2 = 1
    top_line_y2 = 0

    # points définissant la ligne bordure droite
    right_line_x1 = width
    right_line_y1 = 0
    right_line_x2 = width
    right_line_y2 = 1

    #offset courant dans le texte
    #on incrémente l'offset au fur et à mesure des lignes, pour que chaque ligne est la continuation du texte de la ligne précédente
    text_offset = 0

    # Boucle de création des lignes de watermarks
    while True:
        x = x + xadd
        y = y + yadd
        intersection_left = intersection_lignes(left_line_x1, left_line_y1, left_line_x2, left_line_y2, x, y, x+sin, y-cos)
        if intersection_left == None: #angle 90
            y = height
        else:
            x = intersection_left[0]
            y = intersection_left[1]
            if y > height:
                intersection_bottom = intersection_lignes(bottom_line_x1, bottom_line_y1, bottom_line_x2, bottom_line_y2, x, y, x+sin, y-cos)
                if intersection_bottom == None: #angle 0
                    x = 0;
                else:
                    x = intersection_bottom[0]
                    y = intersection_bottom[1]

        
        

        #print("draw point ",x,",",y)
        if y>height+1:
            break;
        if x>width+1:
            break;

        #debug dot
        #draw.ellipse( [(x - 3, y - 3) , (x + 3, y + 3) ] ,fill="red")


        # determine width of text
        # on va prendre l'intersection à l'autre bout du rectangle
        end_ok = True
        intersection_right = intersection_lignes(right_line_x1, right_line_y1, right_line_x2, right_line_y2, x, y, x+sin, y-cos)
        if intersection_right == None or intersection_right[1]<0  or intersection_right[1]>height: 
            intersection_top = intersection_lignes(top_line_x1, top_line_y1, top_line_x2, top_line_y2, x, y, x+sin, y-cos)
            if intersection_top == None or intersection_top[0]<0  or intersection_top[0]>width: 
                end_ok = False
            else:
                end_x=intersection_top[0]
                end_y=intersection_top[1]
        else:
            end_x=intersection_right[0]
            end_y=intersection_right[1]

        if end_ok == False:
            break;

        #debug line
        #Bin non finalement on va la garder cette ligne rouge, elle est sympa
        draw.line( [(x, y) , (end_x, end_y) ] ,fill=line_color, width=line_width)

        print("Line ",(x,y)," - ",(end_x, end_y))

        text_width = int(math.sqrt((end_x-x)*(end_x-x)+(end_y-y)*(end_y-y)))
        #print ("text_width: ",text_width)
        max_text, new_offset = max_text_that_fits(watermark_text, text_offset, text_width, font)
        #print (max_text)
        text_offset = new_offset

        # Créer une image pour le texte incliné
        bbox = draw.textbbox((0, 0), max_text, font=font)
        # La largeur et la hauteur du texte sont données par les dimensions du rectangle
        actual_text_width = bbox[2] - bbox[0]
        actual_text_height = bbox[3] - bbox[1]

        #print("Text width ",text_width," - actual ",actual_text_width," - height ",actual_text_height)

        #watermark_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        watermark_image = Image.new('RGBA', (text_width, actual_text_height), background_color)
        watermark_draw = ImageDraw.Draw(watermark_image)
        # Ajouter le texte au filigrane (en oblique à 45°)
        watermark_draw.text( ( ((text_width-actual_text_width)*0.5) , 0), max_text, font=font, fill=text_color)

        # Faire pivoter l'image du texte de 45 degrés
        watermark_image = watermark_image.rotate(90-angle, expand=True)

        # Obtenir les dimensions de l'image du filigrane après la rotation
        watermark_width, watermark_height = watermark_image.size

        # Coller l'image du filigrane oblique sur l'image originale
        # On décale en fonction de actual_text_height et de l'angle pour centrer le texte sur la ligne
        original_image.paste(watermark_image, (int(x-actual_text_height*0.5*cos), int(y-watermark_height+actual_text_height*0.5*sin)), watermark_image)

    
    # Sauvegarder l'image modifiée
    original_image.save(output_image_path)

def ajouter_prefixe(chemin_fichier, prefixe):
    # Séparer le nom du fichier et l'extension
    nom_fichier, extension = os.path.splitext(chemin_fichier)
    
    # Ajouter le préfixe au nom du fichier
    nouveau_nom = f"{nom_fichier}{prefixe}{extension}"
    
    return nouveau_nom


def main():
    # Créer le parseur d'arguments
    parser = argparse.ArgumentParser(description="Ajouter un filigrane oblique à une image.")

    default_lineoffset = 75;
    default_angle = 70;
    default_textcolor = "#aaaf"
    default_backgroundcolor = "#0008"
    default_linecolor = "red"
    default_linewidth = 5
    
    # Ajouter les arguments
    parser.add_argument("input", help="Chemin de l'image d'entrée")
    parser.add_argument("-o","--output", type=str, help="Chemin de l'image de sortie, optionnel, le nom de fichier sortie est par défaut [nom fichier entrée]_watermarked.[extension fichiée entrée]")
    parser.add_argument("-w","--watermark", type=str, help="Texte du filigrane, la valeur defaut est prise dans le fichier watermark.txt")
    parser.add_argument("-p","--prefix", type=str, help="Prefixe du filigrane")
    parser.add_argument("-fs","--fontsize", type=int, help="Taille de la police en pixels, par defaut la taille de la font est calculée pour qu'on puisse caser une 20aine de lignes les unes sous les autres dans l'image")
    parser.add_argument("-lo","--lineoffset", type=int, default=default_lineoffset, help="Distance entre chaque ligne, en pourcentage de la taille de police, defaut "+str(default_lineoffset)+" pour "+str(default_lineoffset)+"%%")
    parser.add_argument("-a","--angle", type=int, default=default_angle, help="Angle orientation du texte entre 0 et 90, defaut "+str(default_angle)+", pour "+str(default_angle)+"°")
    parser.add_argument("-c","--textcolor", type=str, default=default_textcolor, help="Couleur du texte, defaut "+str(default_textcolor))
    parser.add_argument("-bc","--backgroundcolor", type=str, default=default_backgroundcolor, help="Couleur du background du texte, defaut "+str(default_backgroundcolor))
    parser.add_argument("-lw","--linewidth", type=int, default=default_linewidth, help="Epaisseur de la ligne de fond, defaut "+str(default_linewidth))
    parser.add_argument("-lc","--linecolor", type=str, default=default_linecolor, help="Couleur de la ligne de fond, defaut "+str(default_linecolor))
    
    
    # Analyser les arguments de la ligne de commande
    args = parser.parse_args()

    if not args.output:
        args.output = ajouter_prefixe(args.input,"_watermarked")

    if not args.fontsize:
        args.fontsize = -1

    #if not args.lineoffset:
    #    args.lineoffset = default_lineoffset

    #if not args.angle:
    #    args.angle = default_angle
    if int(args.angle) < 0:
        args.angle = default_angle
    if int(args.angle) > 90:
        args.angle = default_angle

    if not args.watermark:
        with open(script_path+'/watermark.txt', 'r') as fichier:
            args.watermark = fichier.read()

    # Obtenir la date actuelle
    current_date = datetime.now()

    # Formater la date
    # On ajoute la date courante en début du watermark
    formatted_date = current_date.strftime("%d.%m.%Y %H:%M") 

    prefix = formatted_date;

    if args.prefix:
        prefix = prefix + " " + args.prefix

    args.watermark = prefix + " " + formatted_date + " " +args.watermark

    #if not args.textcolor:
    #    args.textcolor=default_textcolor
    
    # Appeler la fonction pour ajouter le filigrane
    add_watermark(args.input, args.output, args.watermark, int(args.fontsize), int(args.lineoffset), int(args.angle), args.textcolor, args.linewidth, args.linecolor, args.backgroundcolor)

if __name__ == "__main__":
    main()
