from PIL import Image
import os

Image.MAX_IMAGE_PIXELS = None  # Desabilita o limite de segurança

def dividir_imagem_em_tiles(caminho_imagem, tamanho_tile=960, pasta_saida='tiles'):
    img = Image.open(caminho_imagem).convert('RGB')
    largura, altura = img.size

    os.makedirs(pasta_saida, exist_ok=True)

    contador = 0
    for y in range(0, altura, tamanho_tile):
        for x in range(0, largura, tamanho_tile):
            box = (x, y, min(x + tamanho_tile, largura), min(y + tamanho_tile, altura))
            tile = img.crop(box)

            # Salva com nome tile_{x}_{y}.jpg
            nome_arquivo = os.path.join(pasta_saida, f'tile_{x}_{y}.jpg')
            tile.save(nome_arquivo)
            print(f'Salvo {nome_arquivo}')
            contador += 1

    print(f'Total de tiles gerados: {contador}')
    return contador

# Usar:
num_tiles = dividir_imagem_em_tiles('imagem_grande.tif', tamanho_tile=960, pasta_saida='tiles')
