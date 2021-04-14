# TCC - DIMAS CURTI E LUIZ GUILHERME ALMADA

## *FERRAMENTA DE ANÁLISE DE ASSINATURA DE ARQUIVOS (FILE SIGNATURE ANALYSIS TOOL)*

O objetivo do algoritmo é determinar, com uma precisão considerável, qual a extensão do arquivo passado como entrada. 
Para isso utilizamos um banco de dados de 20 extensões com 10 arquivos para cada extensão para gerar as assinaturas iniciais para armazenar no banco de dados para comparação.

Link do banco: https://drive.google.com/drive/folders/1QIrI7peGz9bjo3xOmZMzEo5JM0x5ex9F

Utilizamos o algoritmo File Header/Trailer analysis (FHT) que analisa Header e o Trailer dos arquivos de entrada para compararmos e determinarmos a probabilidade do arquivo de entrada ser da extensão verificada correspondente.
Usamos como base o artigo:
Content based file type detection algorithms de 2003 (https://ieeexplore.ieee.org/abstract/document/1174905)

Trabalho de conclusão de curso realizado no semestre 2021/1 na FAESA para o curso de Ciência da Computação.

