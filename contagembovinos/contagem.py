from ultralytics import YOLO
import cv2
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

tiles_folder = 'tiles'
tile_size = 960
max_threads = 4  # Ajuste o número de threads aqui

def processar_tile(tile_info):
    tile_name, x_offset, y_offset = tile_info

    tile_path = os.path.join(tiles_folder, tile_name)
    tile_img = cv2.imread(tile_path)

    # DESATIVADO para debug - sem filtro de verde
    # if not is_green_dominant(tile_img):
    #     return (tile_name, [], np.zeros_like(tile_img))

    model = YOLO('yolov8x.pt')

    # Confiança menor pra pegar mais detecções
    results = model(tile_img, imgsz=tile_size, conf=0.1)

    names = model.names

    # Debug: imprime as classes detectadas neste tile
    print(f"Tile {tile_name} detectou as seguintes classes:")
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        print(f" - {names[cls_id]}")

    bovinos = [
        box for box in results[0].boxes
        if names[int(box.cls[0])] == 'bovinos'  # ajuste pro seu nome exato
    ]

    tile_result = np.zeros_like(tile_img)

    for box in bovinos:
        xyxy = box.xyxy[0].cpu().numpy().astype(int)
        cv2.rectangle(tile_result, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
        cv2.putText(tile_result, 'bovinos', (xyxy[0], xyxy[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return (tile_name, bovinos, tile_result)


tile_files = sorted(os.listdir(tiles_folder))
num_tiles_horizontal = (1920 // tile_size)  # ajuste se necessário

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

cv2.imwrite('deteccoes_resultado.jpg', final_image)
print("Imagem com detecções salva como 'deteccoes_resultado.jpg'")
cv2.imshow('Detecções Completas', final_image)
cv2.waitKey(0)