from PIL import Image
import math
import sys
import os

# Nome esperado do arquivo de imagem
imagem_original_path = "imagembov.jpg"

# ✅ Verifica se o arquivo realmente existe
if not os.path.exists(imagem_original_path):
    print(f"❌ Arquivo '{imagem_original_path}' não encontrado no diretório atual:")
    print(f"📁 Diretório atual: {os.getcwd()}")
    print("🗂️ Arquivos encontrados:", os.listdir())
    sys.exit(1)

try:
    imagem = Image.open(imagem_original_path)

    tamanho_alvo_bytes = 0.5 * 1024**3  # 4GB

    width, height = imagem.size
    print(f"📏 Tamanho original da imagem: {width}x{height} pixels")

    bytes_por_pixel = len(imagem.getbands())
    tamanho_imagem_est = width * height * bytes_por_pixel
    print(f"📦 Tamanho estimado (não compactado): {tamanho_imagem_est / (1024**2):.2f} MB")

    fator_repeticao = math.ceil(math.sqrt(tamanho_alvo_bytes / tamanho_imagem_est))
    print(f"🔁 Repetição por eixo: {fator_repeticao} vezes")

    nova_largura = width * fator_repeticao
    nova_altura = height * fator_repeticao
    print(f"🖼️ Nova imagem: {nova_largura}x{nova_altura} pixels")

    imagem_grande = Image.new(imagem.mode, (nova_largura, nova_altura))

    for i in range(fator_repeticao):
        for j in range(fator_repeticao):
            imagem_grande.paste(imagem, (i * width, j * height))

    output_path = "imagem_grande.tif"
    imagem_grande.save(output_path, compression='raw')

    print(f"✅ Imagem TIFF gigante salva em: {output_path}")

except FileNotFoundError:
    print("❌ Arquivo de imagem não encontrado mesmo após a verificação.")
except MemoryError:
    print("❌ Erro de memória! Tente reduzir o fator de repetição ou use uma máquina com mais RAM.")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    sys.exit(1)
