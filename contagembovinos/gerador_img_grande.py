import numpy as np
import tifffile
from PIL import Image
import math
import os

def gerar_tiff_grande_com_imagem_base(
    caminho_imagem_base='contagembovinos/imagembov.jpg',
    output_path='imagem_grande_20GB.tif',
    tamanho_alvo_gb=20,
    bloco_altura=100
):
    # Abre imagem base
    imagem = Image.open(caminho_imagem_base)
    img_np = np.array(imagem)
    altura_base, largura_base = img_np.shape[:2]
    canais = img_np.shape[2] if img_np.ndim == 3 else 1
    print(f"📏 Imagem base: {largura_base}x{altura_base}, canais: {canais}")

    # Bytes por pixel
    bpp = canais  # uint8, 1 byte por canal

    # Calcular tamanho alvo em bytes
    tamanho_alvo_bytes = tamanho_alvo_gb * 1024**3

    # Estimar tamanho da imagem base (bytes)
    tamanho_base = largura_base * altura_base * bpp
    print(f"📦 Tamanho imagem base: {tamanho_base / (1024**2):.2f} MB")

    # Calcular fator de repetição necessário para atingir o tamanho alvo
    fator = math.sqrt(tamanho_alvo_bytes / tamanho_base)
    fator_x = math.ceil(fator)
    fator_y = math.ceil(fator)

    nova_largura = largura_base * fator_x
    nova_altura = altura_base * fator_y
    tamanho_est = nova_largura * nova_altura * bpp
    print(f"🔁 Repetição por eixo: x={fator_x}, y={fator_y}")
    print(f"🖼️ Nova imagem: {nova_largura}x{nova_altura} pixels (~{tamanho_est/(1024**3):.2f} GB)")

    # Cria memmap para a nova imagem gigante
    shape = (nova_altura, nova_largura, canais) if canais > 1 else (nova_altura, nova_largura)
    dtype = np.uint8

    buffer_path = 'buffer_grande.raw'
    data = np.memmap(buffer_path, dtype=dtype, mode='w+', shape=shape)

    # Escreve a imagem grande em blocos para economizar RAM
    for y_start in range(0, nova_altura, bloco_altura):
        y_end = min(y_start + bloco_altura, nova_altura)
        altura_bloco = y_end - y_start

        # Criar bloco vazio
        bloco = np.zeros((altura_bloco, nova_largura, canais), dtype=dtype) if canais > 1 else np.zeros((altura_bloco, nova_largura), dtype=dtype)

        # Para cada linha do bloco, copiar repetição da imagem base
        for i in range(altura_bloco):
            linha_global = y_start + i
            linha_img_base = linha_global % altura_base

            # Repetir a linha da imagem base no eixo X
            if canais > 1:
                linha = np.tile(img_np[linha_img_base, :, :], (fator_x, 1))
                linha = linha.reshape(nova_largura, canais)
            else:
                linha = np.tile(img_np[linha_img_base, :], fator_x)

            bloco[i] = linha

        data[y_start:y_end] = bloco

        if y_start % (bloco_altura * 10) == 0:
            print(f"🧱 Preenchido linhas {y_start} a {y_end} de {nova_altura}")

    # Salva TIFF
    print("💾 Salvando TIFF grande...")
    tifffile.imwrite(output_path, data, bigtiff=True, compression=None)
    print(f"✅ Arquivo salvo: {output_path}")

    # Remove buffer temporário
    data._mmap.close()
    os.remove(buffer_path)
    print("🧹 Buffer temporário removido.")

# Executa
gerar_tiff_grande_com_imagem_base()
