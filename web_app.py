from PIL import Image

# Carga la imagen desde la misma carpeta donde está tu código
# Asegúrate de poner el nombre correcto y la extensión (.jpg, .png)
try:
    img = Image.open("PanamLogo.jpg")
    img.show()
except FileNotFoundError:
    print("No se encontró el archivo de imagen.")
