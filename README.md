```
usage: watermark.py [-h] [-o OUTPUT] [-w WATERMARK] [-p PREFIX] [-fs FONTSIZE] [-lo LINEOFFSET] [-a ANGLE] [-c TEXTCOLOR] [-bc BACKGROUNDCOLOR] [-lw LINEWIDTH] [-lc LINECOLOR]
                    input

Ajouter un filigrane oblique à une image.

positional arguments:
  input                 Chemin de l'image d'entrée

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Chemin de l'image de sortie, optionnel, le nom de fichier sortie est par défaut [nom fichier entrée]_watermarked.[extension fichiée entrée]
  -w WATERMARK, --watermark WATERMARK
                        Texte du filigrane, la valeur defaut est prise dans le fichier watermark.txt
  -p PREFIX, --prefix PREFIX
                        Prefixe du filigrane
  -fs FONTSIZE, --fontsize FONTSIZE
                        Taille de la police en pixels, par defaut la taille de la font est calculée pour qu'on puisse caser une 20aine de lignes les unes sous les autres dans
                        l'image
  -lo LINEOFFSET, --lineoffset LINEOFFSET
                        Distance entre chaque ligne, en pourcentage de la taille de police, defaut 75 pour 75%
  -a ANGLE, --angle ANGLE
                        Angle orientation du texte entre 0 et 90, defaut 70, pour 70°
  -c TEXTCOLOR, --textcolor TEXTCOLOR
                        Couleur du texte, defaut #aaaf
  -bc BACKGROUNDCOLOR, --backgroundcolor BACKGROUNDCOLOR
                        Couleur du background du texte, defaut #0008
  -lw LINEWIDTH, --linewidth LINEWIDTH
                        Epaisseur de la ligne de fond, defaut 5
  -lc LINECOLOR, --linecolor LINECOLOR
                        Couleur de la ligne de fond, defaut red
```

![Document non watermarké](fake_document.jpg)
![Document watermarké](fake_document_watermarked.jpg)
