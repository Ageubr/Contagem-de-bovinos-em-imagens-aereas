from PIL import Image
import math

# Carrega a imagem original
imagem_original_path = "imagembovinos4.jpg"
imagem = Image.open(imagem_original_path)

# Define o tamanho alvo em bytes (4GB)
tamanho_alvo_bytes = 1 * 1024**3  # 4GB

# Tamanho da imagem original em pixels
width, height = imagem.size
print(f"Tamanho original da imagem: {width}x{height} pixels")

# Estimativa do tamanho da imagem original em bytes (não compactada)
bytes_por_pixel = len(imagem.getbands())  # ex: 3 para RGB, 4 para RGBA
tamanho_imagem_est = width * height * bytes_por_pixel
print(f"Tamanho estimado da imagem original (não compactada): {tamanho_imagem_est / (1024**2):.2f} MB")

# Calcula o fator de repetição por eixo para atingir ~4GB
fator_repeticao = math.ceil(math.sqrt(tamanho_alvo_bytes / tamanho_imagem_est))
print(f"Repetição por eixo: {fator_repeticao} vezes")

# Cria nova imagem grande para colar a original repetida
nova_largura = width * fator_repeticao
nova_altura = height * fator_repeticao
print(f"Nova imagem terá tamanho: {nova_largura}x{nova_altura} pixels")

imagem_grande = Image.new(imagem.mode, (nova_largura, nova_altura))

# Preenche com mosaico da imagem original
for i in range(fator_repeticao):
    for j in range(fator_repeticao):
        pos = (i * width, j * height)
        imagem_grande.paste(imagem, pos)

# Salva imagem TIFF sem compressão (compression='raw' no PIL)
output_path = "imagem_grande.tif"
imagem_grande.save(output_path, compression='raw')

print(f"Imagem TIFF gigante salva em {output_path}")
