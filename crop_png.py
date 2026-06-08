from PIL import Image
import os

def crop_images_from_right_bottom(input_dir, output_dir, crop_right=10, crop_bottom=10):
    """
    Обрезает все PNG изображения в папке справа и снизу
    
    Args:
        input_dir: папка с исходными изображениями
        output_dir: папка для сохранения обрезанных изображений
        crop_right: сколько пикселей обрезать справа
        crop_bottom: сколько пикселей обрезать снизу
    """
    # Создаем папку для результатов
    os.makedirs(output_dir, exist_ok=True)
    
    # Получаем список всех PNG файлов
    image_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.png')]
    
    print(f"Найдено PNG файлов: {len(image_files)}")
    
    for filename in image_files:
        # Открываем изображение
        input_path = os.path.join(input_dir, filename)
        img = Image.open(input_path)
        
        # Получаем размеры
        width, height = img.size
        
        # Вычисляем новые размеры (обрезаем справа и снизу)
        new_width = width - crop_right
        new_height = height - crop_bottom
        
        # Обрезаем изображение (left, top, right, bottom)
        cropped_img = img.crop((0, 0, new_width, new_height))
        
        # Сохраняем
        output_path = os.path.join(output_dir, filename)
        cropped_img.save(output_path)
        
        print(f"Обрезано: {filename} ({width}x{height} -> {new_width}x{new_height})")
    
    print(f"\nГотово! Обработано {len(image_files)} файлов")

# Использование
crop_images_from_right_bottom(
    input_dir="items",      # исходная папка
    output_dir="items_cropped",  # папка для обрезанных
    crop_right=20,          # обрезать 10px справа
    crop_bottom=60          # обрезать 10px снизу
)
