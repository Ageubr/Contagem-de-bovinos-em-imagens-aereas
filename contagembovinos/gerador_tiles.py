import tifffile
import numpy as np
from PIL import Image
import os

def dividir_imagem_em_tiles_tiff_memmap(caminho_imagem, tamanho_tile=960, pasta_saida='tiles'):
    os.makedirs(pasta_saida, exist_ok=True)

    print(f"🔍 Abrindo imagem como memmap: {caminho_imagem}")
    with tifffile.TiffFile(caminho_imagem) as tif:
        img_memmap = tif.asarray(out='memmap')  # NÃO carrega na RAM

        altura, largura = img_memmap.shape[:2]
        canais = img_memmap.shape[2] if img_memmap.ndim == 3 else 1
        print(f"📐 Dimensões: {largura}x{altura}, canais: {canais}")

        contador = 0

        for y in range(0, altura, tamanho_tile):
            for x in range(0, largura, tamanho_tile):
                tile = img_memmap[y:y+tamanho_tile, x:x+tamanho_tile]

                # Se tile for menor que 960x960 (borda inferior ou direita), pula
                if tile.shape[0] < tamanho_tile or tile.shape[1] < tamanho_tile:
                    continue

                tile_pil = Image.fromarray(tile)
                nome_arquivo = os.path.join(pasta_saida, f'tile_{x}_{y}.jpg')
                tile_pil.save(nome_arquivo)
                print(f"💾 Salvo: {nome_arquivo}")
                contador += 1

    print(f"\n✅ Total de tiles gerados: {contador}")
    return contador

# Executar
num_tiles = dividir_imagem_em_tiles_tiff_memmap('imagem_grande_20GB.tif', tamanho_tile=960, pasta_saida='tiles')
