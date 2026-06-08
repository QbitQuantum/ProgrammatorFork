from PIL import Image
import os

def make_transparent_png(input_path, output_path, target_color=(53, 53, 52)):
    """Делает фон прозрачным и сохраняет новый PNG"""
    img = Image.open(input_path)
    img = img.convert("RGBA")
    pixels = img.load()
    
    for x in range(img.width):
        for y in range(img.height):
            r, g, b, a = pixels[x, y]
            # Если цвет совпадает с целевым (с допуском)
            if abs(r - target_color[0]) < 5 and abs(g - target_color[1]) < 5 and abs(b - target_color[2]) < 5:
                pixels[x, y] = (r, g, b, 0)  # делаем прозрачным
    
    img.save(output_path, "PNG")

def preprocess_icons(input_folder, output_folder):
    """Обрабатывает все иконки в папке и сохраняет с прозрачностью"""
    os.makedirs(output_folder, exist_ok=True)
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            print(f"Обработка: {filename}")
            make_transparent_png(input_path, output_path)
            print(f"Сохранено: {output_path}")
    
    print(f"\nГотово! Обработано файлов в папку: {output_folder}")

# Использование
if __name__ == "__main__":
    preprocess_icons("items_cropped", "items_transparent")