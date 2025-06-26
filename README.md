Relatório: Contagem de Bovinos em Imagens Aéreas

1. Introdução
Este projeto tem como objetivo principal desenvolver e avaliar uma solução computacional capaz de realizar a contagem automatizada de bovinos em imagens aéreas de grandes pastagens, utilizando técnicas modernas de visão computacional e aprendizado profundo. A proposta parte da necessidade de monitoramento de rebanhos de forma escalável, eficiente e com mínima intervenção humana.
Com o crescimento do uso de tecnologias na agropecuária, especialmente com o advento de drones e sensores de alta resolução, tornou-se possível capturar imagens detalhadas de grandes áreas rurais. No entanto, o processamento dessas imagens para fins de análise, como a contagem de animais, ainda representa um desafio computacional significativo devido ao tamanho dos arquivos e à necessidade de precisão na detecção de objetos.
Neste contexto, este trabalho propõe uma abordagem que une três frentes principais: a geração de imagens simuladas de alta capacidade (cerca de 20 GB), a segmentação dessas imagens em tiles menores para facilitar o processamento, e o uso de um modelo de detecção de objetos (YOLOv5) para identificar bovinos em cada tile. Para garantir eficiência e escalabilidade, também é aplicada técnica de paralelismo com execução em múltiplos núcleos.
A proposta visa tanto validar a viabilidade técnica da solução quanto analisar o ganho de desempenho proporcionado pelo processamento paralelo, oferecendo uma alternativa viável para monitoramento automatizado de rebanhos em larga escala.

2. Descrição do Problema / Justificativa
Contar manualmente bovinos em grandes áreas rurais é uma tarefa demorada, sujeita a erros humanos e pouco escalável. A aquisição de imagens por drones fornece uma visão ampla e precisa das pastagens, mas essas imagens podem ser de alta resolução e de grande tamanho, o que torna o processamento computacional um desafio. A proposta visa otimizar esse processo dividindo a imagem em pequenas partes (tiles), processando-as paralelamente e aplicando um modelo treinado para detecção de bovinos.

3. Descrição da Solução
   
A solução é composta por três etapas principais:

 Geração de imagem grande: uma imagem original é repetida para gerar um arquivo de aproximadamente 20gb, 7.162.742.240 pixels (aproximadamente 7,16 bilhões de pixels)
 Segmentação em tiles: a imagem é dividida em blocos de menores pixels para facilitar o processamento.
 Contagem de bovinos por tile: cada tile é processado por um modelo YOLOv5 em execução paralela, detectando e contando bovinos. Os resultados são reunidos em uma imagem final e um relatório.

4. Detalhamento do que foi feito
 
•	Geração da imagem grande: usando a biblioteca PIL, a imagem original foi repetida em ambos os eixos (x e y) até que o tamanho estimado da imagem não compactada alcançasse aproximadamente 20 GB. A imagem foi salva no formato TIFF sem compressão.
•	Divisão em tiles: a imagem TIFF foi carregada com tifffile e dividida em blocos de menores pixels, que foram salvos como arquivos JPEG em uma pasta específica.
•	Processamento paralelo e contagem:
o	Cada tile foi processado com o modelo YOLOv5, configurado para detectar objetos com confiança acima de 0.2 e foco na classe "cow".
o	Foi utilizada a biblioteca concurrent.futures com ProcessPoolExecutor para paralelizar o processamento com 1, 2, 4, 8 e 16 processos.
o	Os tiles com detecções foram reunidos em uma imagem final.
o	Um relatório em texto foi gerado contendo a contagem individual por tile e o total geral.

4.1 Ambiente de Testes
Os experimentos foram conduzidos em uma única plataforma computacional para avaliação do desempenho do sistema. A configuração da máquina utilizada está detalhada a seguir:

•	Memória RAM: 16 GB DDR4
•	Processador: Intel Core i7-12700 (12 núcleos, 20 threads)
•	Placa de vídeo: Intel UHD Graphics 770 (GPU integrada)
•	Armazenamento: SSD de 512 GB
•	Sistema Operacional: Windows 10 (64 bits)

4.2 Imagens Utilizadas no Experimento
 
 ![image](https://github.com/user-attachments/assets/8ad91e5e-e98f-41a9-ae2d-f04b71052744)

Figura 1.1 - Imagem base de bovinos criada pelo ChatGPT:
Esta imagem foi gerada artificialmente pelo ChatGPT e representa um pequeno grupo de bovinos em um pasto verde. Ela contém animais nas cores branca e marrom, dispostos de forma a simular uma cena realista. Essa imagem base serve como unidade para a criação de cenários maiores, funcionando como um padrão repetível para compor áreas extensas.

 ![image](https://github.com/user-attachments/assets/a17cffac-d107-47ed-bcbf-8da25dbb1764)

Figura 1.2 - Imagem simulada de 4GB criada pelo ChatGPT:
Esta imagem de alta resolução foi criada pelo ChatGPT através da repetição em mosaico da imagem base, resultando em um arquivo volumoso (aproximadamente 4 GB sem compressão). Essa composição simula um cenário amplo e realista para o monitoramento de bovinos, possibilitando a avaliação do desempenho da segmentação e do processamento paralelo em grandes volumes de dados.

![3d852a14-37d2-4651-adf1-a34f2738c581](https://github.com/user-attachments/assets/9cc7fc9b-bd72-43ee-816b-72d95e9a5bb2)

Figura 1.3 - A imagem final mostra o resultado do teste de detecção de bovinos em uma imagem menor de 100 MB. Para facilitar o processamento, a imagem original foi dividida em 48 partes (tiles), que foram processadas individualmente. Após a detecção, as partes foram reunidas novamente, formando a imagem completa. Os bovinos detectados aparecem com retângulos verdes, evidenciando a eficácia do modelo utilizado.

5. Resultados
A contagem foi realizada com sucesso para todos os 7672 tiles gerados e foram detectados cerca de 90342 bovinos. A execução foi feita com diferentes quantidades de processos para medir o ganho de desempenho. Os resultados de tempo e eficiência foram:

![image](https://github.com/user-attachments/assets/9cd1f46c-2e03-4700-b4b0-12531dafe7a1)

Figura 1.4 - Descrição da tabela: A tabela apresenta os resultados do processamento de 20 GB de dados utilizando diferentes quantidades de processos (1, 2, 4, 8 e 16). Para cada configuração, são mostrados o tempo total de execução, o speedup (aceleração em relação à execução sequencial) e a eficiência. Observa-se que o menor tempo foi alcançado com 4 processos, que também teve o maior speedup (1.36). A eficiência diminui conforme o número de processos aumenta, indicando que o uso excessivo de paralelismo reduz o aproveitamento dos recursos. Essa diminuição da eficiência ocorre principalmente por causa do overhead e da escala limitada do paralelismo.

![graficos_linha_comparativo](https://github.com/user-attachments/assets/069a5c10-b809-4ebf-a328-7b3154849e7a)

Figura 1.5 - Descrição dos gráficos: Os gráficos mostram o desempenho no processamento de 20 GB de dados com diferentes quantidades de processos 1, 2, 4, 8 e 16. Observa-se que o melhor resultado foi com 4 processos, apresentando o menor tempo total, maior speedup e uma eficiência razoável. Com 8 e 16 processos, o desempenho piorou, indicando que o excesso de paralelismo causou sobrecarga no sistema. Isso mostra que mais processos nem sempre significam melhor desempenho.

![graficos_barras_comparativo](https://github.com/user-attachments/assets/1c57bd6a-f5f9-4f24-b997-f328aaac65ff)

Figura 1.6 - Descrição dos gráficos: Os gráficos mostram três gráficos que comparam o desempenho no processamento de 20 GB com diferentes quantidades de processos. O menor tempo de execução e o melhor desempenho ocorreram com 4 processos. A partir desse ponto, o uso de mais processos não trouxe ganhos e ainda reduziu a eficiência, indicando que o excesso de paralelismo prejudicou o resultado.


6. Conclusão

A metodologia implementada demonstrou eficácia na contagem automatizada de bovinos em imagens aéreas de alta resolução. A estratégia de segmentação da imagem em tiles combinada com o processamento paralelo proporcionou escalabilidade significativa ao sistema, resultando em ganhos expressivos de speedup no tempo de execução. O modelo YOLOv apresentou desempenho satisfatório para a tarefa de detecção, contudo, há potencial para aprimoramentos futuros por meio da utilização de modelos com maior capacidade preditiva e da implementação de técnicas de pós-processamento, como a recontagem e a filtragem de detecções duplicadas em regiões sobrepostas entre tiles adjacentes, visando aumentar a precisão dos resultados. 



