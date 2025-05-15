Projeto: Contador de Bovinos em Pasto com Segmentação e Processamento Paralelo

Este projeto tem como objetivo realizar a detecção e contagem automática de bovinos (vacas) a partir de imagens capturadas em pastos, utilizando segmentação de imagem, detecção com YOLOv5 e execução paralela com Python para maior desempenho.


O que o programa faz:
	•	Carrega um modelo pré-treinado YOLOv5 para detecção de objetos.
	•	Lê todas as imagens da pasta imagens/.
	•	Para cada imagem:
	1.	Aplica segmentação de imagem para destacar apenas os bovinos e remover o fundo (grama, céu, etc.).
	2.	Usa o modelo YOLOv5 para detectar os bovinos.
	3.	Conta quantos bovinos foram detectados.
	•	Executa a análise de várias imagens em paralelo, aproveitando múltiplos núcleos do processador.
	•	Exibe a contagem de bovinos por imagem no terminal.


Tecnologias utilizadas:
	•	Python 3
	•	YOLOv5 (via torch.hub)
	•	PyTorch
	•	OpenCV (para segmentação)
	•	Pandas
	•	concurrent.futures (para paralelismo)
