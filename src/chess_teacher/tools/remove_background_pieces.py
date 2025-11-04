import os
from PIL import Image

# Ruta absoluta a assets/pieces (independiente de desde dónde ejecutes)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, "..", "assets", "pieces")
path = os.path.abspath(path)

for file in os.listdir(path):
    if file.endswith(".png"):
        img_path = os.path.join(path, file)
        img = Image.open(img_path).convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            # Si el color es blanco (o casi blanco), lo hacemos transparente
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)

        img.putdata(new_data)
        img.save(img_path)
        print(f"✅ Fondo eliminado de {file}")