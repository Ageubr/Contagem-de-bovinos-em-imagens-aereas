INTRODUÇÃO

O projeto “Contador de Bovinos em Pasto com Segmentação e Processamento Paralelo” tem como objetivo desenvolver um sistema automático para detectar e contar bovinos em imagens de pastagens. Utilizamos técnicas de segmentação de imagem e o modelo de detecção YOLOv5 para identificar os animais. Para acelerar o processo, aplicamos processamento paralelo em Python, que permite analisar várias imagens ao mesmo tempo.
O programa carrega um modelo pré-treinado de YOLOv5 para detectar bovinos em imagens previamente segmentadas para destacar os animais e remover o fundo. Com isso, é possível contar os bovinos de forma rápida e precisa, ajudando no manejo das fazendas.
As tecnologias usadas incluem Python 3, PyTorch, OpenCV e bibliotecas para processamento paralelo, garantindo eficiência na análise das imagens.

•	Usamos uma imagem de 4 Gb
•	Dividimos a imagem em TILES (total de tiles encontrados: 1536). Mais o que são tiles, tiles são pedaços menores de uma imagem grande. Mais por que usamos tiles? Usamos tiles para dividir uma imagem grande em pedaços menores, facilitando o processamento. Isso ajuda a: evitar problemas de memória e lentidão ao trabalhar com imagens muito grandes; permitir que várias partes da imagem sejam analisadas ao mesmo tempo, acelerando o processo; melhorar a precisão da detecção, pois o modelo consegue focar melhor em detalhes menores.

A imagem original foi segmentada em 1536 tiles para possibilitar o processamento eficiente. Essa divisão em blocos menores permite que o modelo realize a análise de cada tile individualmente, otimizando o uso de recursos computacionais e possibilitando o processamento paralelo. Embora a imagem seja dividida em múltiplos tiles, todos correspondem a fragmentos da mesma imagem original, não sendo imagens distintas. Além disso, o particionamento melhora a precisão da detecção, pois cada tile contém uma área limitada da imagem, facilitando a identificação de objetos em alta resolução.
 
Figura 1 - Rebanho de bois. Imagem gerada por inteligência artificial ChatGPT, 2025.
![image](https://github.com/user-attachments/assets/34ac44f0-6729-473a-aed0-1775d8821c70)

Figura 2 – Composição visual com 442 repetições da imagem original. Gerada com auxílio da ferramenta ChatGPT.
![image](https://github.com/user-attachments/assets/698602a2-5e1e-4d36-b932-4da027c810f4)


TECNOLOGIAS UTILIZADAS 
BIBLIOTECAS
Bibliotecas externas (precisam ser instaladas via pip)
1.	ultralytics
•	Usada para carregar o modelo YOLOv8 
•	Instalação: pip install ultralytics

2.	opencv-python
•	Para leitura, desenho e escrita de imagens.
•	Instalação: pip install opencv-python

3.	Numpy
•	Para manipulação de arrays e imagens como matrizes.
•	Instalação:
pip install numpy
Você pode instalar tudo com este comando: pip install ultralytics opencv-python numpy


AMBIENTE DE TESTES
Os experimentos foram realizados em duas máquinas com as seguintes configurações:
•	Máquina 1:
Memória RAM: 16 GB
Processador: Intel Core i7-12700
Placa de vídeo: Intel UHD Graphics 770
Armazenamento: SSD de 512 GB


4 RESULTADOS	
Tabela 1 – Comparação do desempenho em diferentes quantidades de processos, com tempo de execução, speedup e eficiência.
Processos	 Tempo/s	Speedup 	Eficiência 
   1			
   2			
   4			
   8			
  16			
  32			
