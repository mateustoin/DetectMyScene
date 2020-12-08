<figure class="image" align='center'>
    <img src="img/DetectMySceneHeader.png?raw=true">
    <figcaption></figcaption>
</figure>

## Índice
+ [Sobre](#sobre)
+ [Primeiros Passos](#primeiros_passos)
+ [Uso](#uso)
+ [Contribuiçōes](../CONTRIBUTING.md)

<h2 id="sobre">Sobre</h2>

O *Detect My Scene* foi um projeto realizado durante a live coding do <a href="">meu canal na Twitch</a>. O objetivo principal era realizar algum projeto assistivo, para suprir alguma necessidade. Através de discussões foi resolvido que poderíamos ajudar deficientes visuais, criando um programa que fosse capaz de descrever uma foto (que poderia ser extendido para vídeos também) através de texto ou áudio. Com isso o deficiente visual poderia tirar fotos em um ambiente ou até tirar fotos de alguma notícia ou artigo para rodar no software e ter uma breve descrição do que existe ali.

Para a criação dessa aplicação foram utilizados alguns conceitos de Inteligência Artificial e Processamento Digital de Imagens, com a biblioteca <a href="https://github.com/OlafenwaMoses/ImageAI">ImageAI</a> e alguns cálculos e aplicações implementadas do zero. O projeto é realizado em alguns passos.

Para a maioria dos testes durante o desenvolvimento do projeto, a imagem a seguir foi utilizada, além de algumas outras para validações. Os objetos identificados nas imagens testadas no desenvolvimento mostram apenas objetos que o algoritmo tem 45% ou mais de certeza de ser de fato aquilo que foi identificado.

<figure class="image" align='center'>
    <img src="img/example.jpg?raw=true">
    <figcaption>Figura 1. Imagem de teste</figcaption>
</figure>

<h3><b>Passo 1: Identificação dos objetos</b></h3>

Esse passo é realizado pela própria biblioteca utilizada (ImageAI), onde são identificados todos os objetos reconhecidos na imagem, informando o nome, probabilidade de ser aquele objeto específico e suas delimitações na imagem. Essas informações base são essenciais para os próximos passos, pois são com elas que todas as informações são cruzadas e geram novos resultados.

<figure class="image" align='center'>
    <img src="img/example_square.jpg?raw=true">
    <figcaption>Figura 2. Identificação da biblioteca</figcaption>
</figure>

<h3><b>Passo 2: </b></h3>

Após o passo 1 o objetivo foi calcular o "ponto central" dos objetos, a partir da delimitação, conhecida como *box_points*. Determinar esse ponto foi necessário para que cada objeto tivesse sua posição em um ponto (x, y) na imagem, para que o próximo passo pudesse ser feito.

<figure class="image" align='center'>
    <img src="img/example_point.jpg?raw=true">
    <figcaption>Figura 3. Determinação do ponto (x, y) de cada objeto</figcaption>
</figure>

<h3><b>Passo 3: </b></h3>

Com os objetos tendo suas posições devidamente identificadas, foi possível implementar e calcular a *distância euclidiana* entre cada um dos objetos identificados. Além de saber exatamente em que área da imagem cada objeto está, agora sabemos a distância entre cada um. Isso possibilita a implementação de outros algoritmos como KNN (Vizinho mais próximo), entre outros, a fim de criar uma relação entre os objetos e criar descrições para o/a deficiente visual cada vez mais detalhadas.

<figure class="image" align='center'>
    <img src="img/example_line.jpg?raw=true">
    <figcaption>Figura 3. Cálculo de distância entre objetos</figcaption>
</figure>

Além disso foi criada uma Matriz de Distância, com identificador entre cada objeto (como pode ser visto na imagem acima) e linhas indicando onde inicia e para. A tabela com os valores para a imagem de exemplo podem ser vistos abaixo (distância em pixels).

<table align='center'>
<thead>
<tr>
<th style="text-align:center">*</th>
<th style="text-align:center"><strong>0</strong></th>
<th style="text-align:center"><strong>1</strong></th>
<th style="text-align:center"><strong>2</strong></th>
<th style="text-align:center"><strong>3</strong></th>
<th style="text-align:center"><strong>4</strong></th>
<th style="text-align:center"><strong>5</strong></th>
<th style="text-align:center"><strong>6</strong></th>
<th style="text-align:center"><strong>7</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center"><strong>0</strong></td>
<td style="text-align:center">0</td>
<td style="text-align:center">132</td>
<td style="text-align:center">71</td>
<td style="text-align:center">452</td>
<td style="text-align:center">188</td>
<td style="text-align:center">203</td>
<td style="text-align:center">190</td>
<td style="text-align:center">296</td>
</tr>
<tr>
<td style="text-align:center"><strong>1</strong></td>
<td style="text-align:center">132</td>
<td style="text-align:center">0</td>
<td style="text-align:center">63</td>
<td style="text-align:center">584</td>
<td style="text-align:center">318</td>
<td style="text-align:center">282</td>
<td style="text-align:center">321</td>
<td style="text-align:center">426</td>
</tr>
<tr>
<td style="text-align:center"><strong>2</strong></td>
<td style="text-align:center">71</td>
<td style="text-align:center">63</td>
<td style="text-align:center">0</td>
<td style="text-align:center">521</td>
<td style="text-align:center">259</td>
<td style="text-align:center">249</td>
<td style="text-align:center">261</td>
<td style="text-align:center">367</td>
</tr>
<tr>
<td style="text-align:center"><strong>3</strong></td>
<td style="text-align:center">452</td>
<td style="text-align:center">584</td>
<td style="text-align:center">521</td>
<td style="text-align:center">0</td>
<td style="text-align:center">282</td>
<td style="text-align:center">433</td>
<td style="text-align:center">269</td>
<td style="text-align:center">193</td>
</tr>
<tr>
<td style="text-align:center"><strong>4</strong></td>
<td style="text-align:center">188</td>
<td style="text-align:center">318</td>
<td style="text-align:center">259</td>
<td style="text-align:center">282</td>
<td style="text-align:center">0</td>
<td style="text-align:center">171</td>
<td style="text-align:center">25</td>
<td style="text-align:center">108</td>
</tr>
<tr>
<td style="text-align:center"><strong>5</strong></td>
<td style="text-align:center">203</td>
<td style="text-align:center">282</td>
<td style="text-align:center">249</td>
<td style="text-align:center">433</td>
<td style="text-align:center">171</td>
<td style="text-align:center">0</td>
<td style="text-align:center">195</td>
<td style="text-align:center">240</td>
</tr>
<tr>
<td style="text-align:center"><strong>6</strong></td>
<td style="text-align:center">190</td>
<td style="text-align:center">321</td>
<td style="text-align:center">261</td>
<td style="text-align:center">269</td>
<td style="text-align:center">25</td>
<td style="text-align:center">195</td>
<td style="text-align:center">0</td>
<td style="text-align:center">109</td>
</tr>
<tr>
<td style="text-align:center"><strong>7</strong></td>
<td style="text-align:center">296</td>
<td style="text-align:center">426</td>
<td style="text-align:center">367</td>
<td style="text-align:center">193</td>
<td style="text-align:center">108</td>
<td style="text-align:center">240</td>
<td style="text-align:center">109</td>
<td style="text-align:center">0</td>
</tr>
</tbody>
</table>

<p align='center'>Tabela 1. Matriz de distância entre os objetos da imagem</p>

<h3><b>Passo 4: </b></h3>

De acordo com o que foi feito no *passo 1* já é possível criar uma descrição textual do que pode ser encontrado na imagem e uma sonora também. Todos os tipos de objetos identificáveis pelo modelo foram traduzidos para que um dos principais diferenciais do projeto pudesse ser feito: descrição textual e sonora em português. A seguir é possível escutar o áudio gerado automaticamente depois da identificação dos objetos:

<div class="iframe_container">
<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/942458215&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true" allowfullscreen></iframe><div style="font-size: 10px; color: #cccccc;line-break: anywhere;word-break: normal;overflow: hidden;white-space: nowrap;text-overflow: ellipsis; font-family: Interstate,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Garuda,Verdana,Tahoma,sans-serif;font-weight: 100;"><a href="https://soundcloud.com/mateus-antonio-11" title="Mateus Antonio" target="_blank" style="color: #cccccc; text-decoration: none;">Mateus Antonio</a> · <a href="https://soundcloud.com/mateus-antonio-11/localizada-descricao" title="Localizada Descricao" target="_blank" style="color: #cccccc; text-decoration: none;">Localizada Descricao</a></div>
</div>

<div class="iframe_container">
<iframe width="100%" height="166" frameborder="0" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/942458215&color=%23ff5500&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true" allowfullscreen></iframe>
</div>

<div style="font-size: 10px; color: #cccccc;line-break: anywhere;word-break: normal;overflow: hidden;white-space: nowrap;text-overflow: ellipsis; font-family: Interstate,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Garuda,Verdana,Tahoma,sans-serif;font-weight: 100;"><a href="https://soundcloud.com/mateus-antonio-11" title="Mateus Antonio" target="_blank" style="color: #cccccc; text-decoration: none;">Mateus Antonio</a> · <a href="https://soundcloud.com/mateus-antonio-11/localizada-descricao" title="Localizada Descricao" target="_blank" style="color: #cccccc; text-decoration: none;">Localizada Descricao</a></div>

<h3><b>Passo 5: </b></h3>

link para os áudios:
https://soundcloud.com/mateus-antonio-11/sets/audios-projeto-detectmyscene

## Começando <a name = "comecando"></a>
Estas intruçōes te darão uma cópia funcional do projeto na sua máquina local para desenvolvimento e testes. Veja [deployment](#deployment) para uma descrição de como realizar o deployment deste projeto online.

### Pré-requisitos

Descreva o que é necessário para instalar este software e como instalá-lo.

```
Dê exemplos
```

### Instalação

Passo-a-passo com exemplos que reproduzam um estágio de desenvolvimento funcional.

Descreva o passo a ser tomado

```
Dê um exemplo
```

Repita

```
Até terminar
```

## Uso <a name="uso"></a>
Descreva como utilizar seu app ou sistema.

