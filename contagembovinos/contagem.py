from ultralytics import YOLO 
import cv2
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from glob import glob
import time

# Carregar modelo
model = YOLO('yolov8x-seg.pt')

# Parâmetros dos tiles
tile_size = 960
pasta_tiles = 'tiles'

def carregar_tiles_existentes():
    arquivos = sorted(glob(os.path.join(pasta_tiles, 'tile_*.jpg')))
    tiles = []
    largura_max = 0
    altura_max = 0

    for tile_path in arquivos:
        nome = os.path.basename(tile_path).replace('.jpg', '')
        try:
            _, x, y = nome.split('_')
            x, y = int(x), int(y)
            tiles.append((tile_path, x, y))

            largura_max = max(largura_max, x + tile_size)
            altura_max = max(altura_max, y + tile_size)
        except:
            print(f"❌ Nome de tile inválido: {nome}")

    print(f"🔹 Total de tiles encontrados: {len(tiles)}")
    return tiles, (largura_max, altura_max)

def processar_tile(tile_info):
    tile_path, x, y = tile_info
    img = cv2.imread(tile_path)

    results = model(img, imgsz=tile_size, conf=0.2)
    deteccoes = results[0]
    count_bovinos = 0
    tile_result = img.copy()

    for box in deteccoes.boxes:
        classe = int(box.cls.item())
        conf = box.conf.item()
        if classe == 19:  # 'cow'
            count_bovinos += 1
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cv2.rectangle(tile_result, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f'Cow {conf:.2f}'
            cv2.putText(tile_result, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    return (tile_path, count_bovinos, tile_result)

def executar_teste(n_threads, tiles, dimensoes, salvar_imagem=False):
    largura_total, altura_total = dimensoes
    resultado_final = np.zeros((altura_total, largura_total, 3), dtype=np.uint8)
    total_bovinos = 0
    relatorio = []

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(processar_tile, tile) for tile in tiles]
        for future in futures:
            tile_path, bovinos, tile_result = future.result()
            nome = os.path.basename(tile_path).replace('.jpg', '')
            _, x, y = nome.split('_')
            x, y = int(x), int(y)
            h, w, _ = tile_result.shape
            resultado_final[y:y + h, x:x + w] = tile_result
            total_bovinos += bovinos
            relatorio.append((nome, bovinos))

    tempo_total = time.time() - start_time

    if salvar_imagem:
        cv2.imwrite('resultado_final.jpg', resultado_final)
        with open('relatorio_bovinos.txt', 'w') as f:
            f.write("Relatório de Detecção de Bovinos por Tile\n")
            f.write("=" * 40 + "\n")
            for nome, qtd in sorted(relatorio):
                f.write(f"{nome}: {qtd} bovinos\n")
            f.write("=" * 40 + "\n")
            f.write(f"Total geral de bovinos: {total_bovinos}\n")

    return tempo_total

if __name__ == "__main__":
    tiles, dimensoes = carregar_tiles_existentes()
    configuracoes_threads = [1, 2, 4, 8, 16, 32]
    tempos = {}

    for i, n in enumerate(configuracoes_threads):
        print(f"\n🔧 Executando com {n} thread(s)...")
        salvar = n == 1  # Salvar resultados apenas na primeira execução
        tempo = executar_teste(n, tiles, dimensoes, salvar_imagem=salvar)
        tempos[n] = tempo
        print(f"⏱️ Tempo total com {n} thread(s): {tempo:.2f} segundos")

    print("\n📊 Comparativo de Performance")
    tempo_base = tempos[1]
    for n in configuracoes_threads:
        tempo = tempos[n]
        speedup = tempo_base / tempo
        eficiencia = speedup / n
        print(f"\n🧵 {n} thread(s):")
        print(f"   Tempo total: {tempo:.2f} s")
        print(f"   Speedup: {speedup:.2f}")
        print(f"   Eficiência: {eficiencia:.2f}")
