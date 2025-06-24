import tifffile
import numpy as np
from PIL import Image
import os

def dividir_imagem_em_tiles_tiff(caminho_imagem, tamanho_tile=960, pasta_saida='tiles'):
    os.makedirs(pasta_saida, exist_ok=True)
    with tifffile.TiffFile(caminho_imagem) as tif:
        img = tif.asarray()
        altura, largura = img.shape[:2]
        contador = 0
        for y in range(0, altura, tamanho_tile):
            for x in range(0, largura, tamanho_tile):
                tile = img[y:y+tamanho_tile, x:x+tamanho_tile]
                # Converte para PIL e salva
                tile_pil = Image.fromarray(tile)
                nome_arquivo = os.path.join(pasta_saida, f'tile_{x}_{y}.jpg')
                tile_pil.save(nome_arquivo)
                print(f'Salvo {nome_arquivo}')
                contador += 1
    print(f'Total de tiles gerados: {contador}')
    return contador

# Usar:
num_tiles = dividir_imagem_em_tiles_tiff('imagem_grande.tif', tamanho_tile=960, pasta_saida='tiles')
