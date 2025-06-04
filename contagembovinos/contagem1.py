from roboflow import Roboflow
from ultralytics import YOLO
import cv2
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Configurações ---
tiles_folder = 'tiles'
tile_size = 960
max_threads = 4
green_threshold = 0.3

# --- Inicializa Roboflow e baixa modelo ---
print("Conectando ao Roboflow...")
rf = Roboflow(api_key="KAGFpgKZ5YxnFezutf8K")
project = rf.workspace("ageubr").project("bovinosdetection")
version = project.version(1)

print("Baixando modelo yolov8...")
model_obj = version.model
model_path = model_obj.download("yolov8")
print(f"Modelo baixado em: {model_path}")

# Carrega modelo YOLO
model = YOLO(model_path)

def is_green_dominant(tile_img, threshold=green_threshold):
    hsv = cv2.cvtColor(tile_img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = np.sum(mask > 0) / (tile_img.shape[0] * tile_img.shape[1])
    return green_ratio >= threshold

def processar_tile(tile_info):
    tile_name, x_offset, y_offset = tile_info
    tile_path = os.path.join(tiles_folder, tile_name)
    tile_img = cv2.imread(tile_path)

    if tile_img is None:
        print(f"Erro ao ler imagem {tile_path}")
        return (tile_name, [], np.zeros((tile_size, tile_size, 3), dtype=np.uint8))

    if not is_green_dominant(tile_img):
        return (tile_name, [], np.zeros_like(tile_img))

    results = model(tile_img, imgsz=tile_size, conf=0.20)
    names = model.names

    bovinos = [
        box for box in results[0].boxes
        if names[int(box.cls[0])] == 'cow'
    ]

    tile_result = np.zeros_like(tile_img)
    for box in bovinos:
        xyxy = box.xyxy[0].cpu().numpy().astype(int)
        cv2.rectangle(tile_result, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
        cv2.putText(tile_result, 'cow', (xyxy[0], xyxy[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return (tile_name, bovinos, tile_result)

# --- Preparar tiles ---
tile_files = sorted(os.listdir(tiles_folder))
num_tiles_horizontal = (1920 // tile_size)  # ajuste conforme imagem base

tile_infos = []
for tile_name in tile_files:
    idx = int(tile_name.split('_')[1].split('.')[0])
    x_offset = (idx % num_tiles_horizontal) * tile_size
    y_offset = (idx // num_tiles_horizontal) * tile_size
    tile_infos.append((tile_name, x_offset, y_offset))

max_x = max(x for _, x, _ in tile_infos)
max_y = max(y for _, _, y in tile_infos)
height = max_y + tile_size
width = max_x + tile_size
final_image = np.zeros((height, width, 3), dtype=np.uint8)

total_bovinos = 0

# --- Processamento paralelo ---
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = [executor.submit(processar_tile, info) for info in tile_infos]
    for future in as_completed(futures):
        tile_name, bovinos, tile_result = future.result()
        idx = int(tile_name.split('_')[1].split('.')[0])
        x_offset = (idx % num_tiles_horizontal) * tile_size
        y_offset = (idx // num_tiles_horizontal) * tile_size

        total_bovinos += len(bovinos)

        for c in range(3):
            final_image[y_offset:y_offset+tile_size, x_offset:x_offset+tile_size, c] = \
                np.maximum(final_image[y_offset:y_offset+tile_size, x_offset:x_offset+tile_size, c], tile_result[:, :, c])

print(f'Total de bovinos detectados na imagem inteira: {total_bovinos}')

cv2.imshow('Detecções Completas', final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
