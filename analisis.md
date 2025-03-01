Grafo creado con 260 nodos y 337 aristas

1. ANÁLISIS DE CENTRALIDAD DE GRADO
--------------------------------------------------
Top 10 artistas con mayor centralidad de grado:
               artista  grado_entrada  grado_salida  grado_total
96         Mau y Ricky              1            30           31
1        Maria Becerra              8            15           23
133           Anuel AA              1            20           21
0          Lola Indigo              5            15           20
143           Soolking             10             9           19
22             Big One              1            17           18
45            J Balvin              2            14           16
178              SAIKO              5            11           16
120            Quevedo              5             9           14
2    Villano Antillano              2            11           13

Estadísticas de grado en la red:
Grado medio: 2.59
Grado máximo: 31
Grado mínimo: 0
Desviación estándar: 4.30

Interpretación:
El artista Mau y Ricky tiene la mayor centralidad de grado con 31 conexiones totales.
Los artistas con alta centralidad de grado son influyentes en la red ya que:
- Tienen más contacto directo con otros artistas
- Pueden difundir información más rápidamente
- Son posibles puentes entre diferentes grupos o comunidades

2. ANÁLISIS DE CENTRALIDAD DE INTERMEDIACIÓN Y CERCANÍA
--------------------------------------------------
Nota: El grafo no es fuertemente conexo. Usando el componente más grande con 32 nodos.
Top 10 artistas con mayor centralidad de intermediación:
             artista  intermediacion
0        Lola Indigo        0.064412
1      Maria Becerra        0.052844
79     Manuel Turizo        0.039568
96       Mau y Ricky        0.035078
143         Soolking        0.031882
120          Quevedo        0.029953
178            SAIKO        0.027760
89   Sebastian Yatra        0.023593
121           Aitana        0.020876
213            Emkal        0.010469

Top 10 artistas con mayor centralidad de cercanía:
           artista  cercania
0      Lola Indigo  0.596154
143       Soolking  0.469697
1    Maria Becerra  0.449275
120        Quevedo  0.442857
178          SAIKO  0.442857
213          Emkal  0.436620
144           GIMS  0.430556
161           Rvfv  0.413333
79   Manuel Turizo  0.413333
12            TINI  0.413333

Correlación entre intermediación y cercanía: 0.68

Interpretación:
Centralidad de intermediación:
- Lola Indigo tiene la mayor intermediación, lo que significa que actúa como puente entre diferentes
  grupos de la red. Estos nodos son cruciales para la transmisión de información o influencia.

Centralidad de cercanía:
- Lola Indigo tiene la mayor cercanía, lo que indica que puede alcanzar cualquier otro nodo
  de la red con menos pasos intermedios. Estos artistas pueden distribuir información
  de manera más eficiente y tener acceso más rápido a los recursos de la red.

3. ANÁLISIS DE PAGERANK
--------------------------------------------------
Top 10 artistas con mayor PageRank:
           artista  pagerank  followers
143       Soolking  0.009234  5863174.0
238            NaN  0.006216        NaN
144           GIMS  0.005995  5747998.0
0      Lola Indigo  0.005768  1465255.0
145       DYSTINCT  0.005763   684861.0
1    Maria Becerra  0.005589  7541436.0
147          Morad  0.005378  3937312.0
178          SAIKO  0.005311  1597683.0
157           Naza  0.005210  1714166.0
120        Quevedo  0.005169  5610673.0

Correlación entre PageRank y número de seguidores: 0.05

Interpretación:
- Soolking tiene el mayor PageRank, lo que indica que es el artista más influyente según este algoritmo.
- El PageRank considera no solo la cantidad de conexiones, sino también la calidad de estas.
- Los artistas con alto PageRank reciben conexiones de otros artistas que también son influyentes.
- Estos artistas son considerados autoridades o referencias en la red.

La baja correlación entre PageRank y seguidores sugiere que la influencia en esta red
no está directamente relacionada con la popularidad general del artista en términos de seguidores.

4. ANÁLISIS HITS (HUBS Y AUTORIDADES)
--------------------------------------------------
Top 10 artistas que funcionan como HUBS (conectores):
                artista  hub_score
96          Mau y Ricky   0.239157
133            Anuel AA   0.083030
0           Lola Indigo   0.078887
22              Big One   0.076148
45             J Balvin   0.053676
60     Enrique Iglesias   0.050365
1         Maria Becerra   0.049752
89      Sebastian Yatra   0.039257
37   Los Ángeles Azules   0.030585
79        Manuel Turizo   0.029815

Top 10 artistas que funcionan como AUTORIDADES:
             artista  authority_score
1      Maria Becerra         0.033803
47           KAROL G         0.024574
79     Manuel Turizo         0.022572
55         Nicky Jam         0.020798
106          Farruko         0.019525
90             Beéle         0.018679
62     Gente De Zona         0.017545
89   Sebastian Yatra         0.017447
239              NaN         0.016872
92      Carlos Vives         0.016872

Interpretación:
- Mau y Ricky es el principal hub en la red, lo que significa que conecta a muchas autoridades.
  Los hubs son nodos que enlazan a muchas autoridades de calidad, actuando como agregadores o distribuidores.

- Maria Becerra es la principal autoridad en la red, lo que significa que recibe enlaces de muchos hubs.
  Las autoridades son nodos reconocidos como fuentes confiables o importantes, recibiendo muchas conexiones de hubs.

Contribución a la estructura de la red:
- Los hubs facilitan la navegación y el flujo de información al conectar diferentes autoridades.
- Las autoridades proporcionan contenido valioso o posiciones de referencia en la red.
- La estructura hub-autoridad crea una jerarquía natural que organiza el flujo de información.
- Esta estructura mejora la cohesión y la eficiencia en la transmisión de información dentro de la red.

5. ANÁLISIS DE EXCENTRICIDAD Y DIÁMETRO
--------------------------------------------------
Nota: El grafo no es fuertemente conexo. Usando el componente más grande con 32 nodos.
Diámetro de la red: 10
Radio de la red: 2

Artistas con menor excentricidad (más centrales):
              artista  excentricidad
9         Lola Indigo              2
1                Rvfv              3
15  Villano Antillano              3
2               Emkal              3
31           Soolking              3

Artistas con mayor excentricidad (más periféricos):
       artista  excentricidad
8   La Pantera              9
12  Came Beats             10
10    JC Reyes             10
3        Gonzy             10
22   Yan Block             10

Nodos centro:
- Lola Indigo

Nodos periféricos:
- Gonzy
- JC Reyes
- Came Beats
- Yan Block

Interpretación:
- El diámetro de la red es 10, lo que significa que la distancia máxima entre dos nodos es de 10 pasos.
- El radio de la red es 2, que es la mínima excentricidad de cualquier nodo.
- La red tiene un diámetro relativamente grande, lo que puede indicar una estructura más elongada
  o con comunidades más separadas, donde la información tarda más en propagarse entre extremos.

Implicaciones para la accesibilidad:
- Los nodos centrales (baja excentricidad) pueden comunicarse eficientemente con toda la red.
- Los nodos periféricos (alta excentricidad) están más aislados y requieren más pasos para
  conectarse con partes distantes de la red.

Longitud media del camino más corto: 4.06
- Este valor indica cuán conectada está la red en promedio. Un valor bajo sugiere
  una red bien conectada donde la información puede fluir rápidamente.

6. ANÁLISIS DE COMUNIDADES Y SEGREGACIÓN
--------------------------------------------------
Número de comunidades detectadas: 38

Tamaño de cada comunidad:
Comunidad 0: 33 artistas
Comunidad 1: 10 artistas
Comunidad 2: 1 artistas
Comunidad 3: 14 artistas
Comunidad 4: 1 artistas
Comunidad 5: 1 artistas
Comunidad 6: 1 artistas
Comunidad 7: 34 artistas
Comunidad 8: 30 artistas
Comunidad 9: 1 artistas
Comunidad 10: 1 artistas
Comunidad 11: 1 artistas
Comunidad 12: 1 artistas
Comunidad 13: 31 artistas
Comunidad 14: 9 artistas
Comunidad 15: 1 artistas
Comunidad 16: 1 artistas
Comunidad 17: 1 artistas
Comunidad 18: 1 artistas
Comunidad 19: 1 artistas
Comunidad 20: 9 artistas
Comunidad 21: 1 artistas
Comunidad 22: 1 artistas
Comunidad 23: 1 artistas
Comunidad 24: 47 artistas
Comunidad 25: 1 artistas
Comunidad 26: 1 artistas
Comunidad 27: 2 artistas
Comunidad 28: 1 artistas
Comunidad 29: 7 artistas
Comunidad 30: 1 artistas
Comunidad 31: 1 artistas
Comunidad 32: 8 artistas
Comunidad 33: 1 artistas
Comunidad 34: 1 artistas
Comunidad 35: 1 artistas
Comunidad 36: 1 artistas
Comunidad 37: 1 artistas

Artistas por comunidad (primeros 3 de cada una):

Comunidad 0:
- Lola Indigo (Géneros: N/A)
- Maria Becerra (Géneros: argentine trap)
- TINI (Géneros: latin pop)

Comunidad 1:
- Villano Antillano (Géneros: neoperreo)
- Sevdaliza (Géneros: N/A)
- Tokischa (Géneros: dembow, neoperreo)

Comunidad 2:
- Nesim Najih (Géneros: moombahton)

Comunidad 3:
- Morat (Géneros: colombian pop, latin pop)
- Nicki Nicole (Géneros: argentine trap)
- ELENA ROSE (Géneros: latin r&b)

Comunidad 4:
- Artist Unknown (Géneros: opera)

Comunidad 5:
- artistbasm (Géneros: N/A)

Comunidad 6:
- Belinda Carlisle (Géneros: N/A)

Comunidad 7:
- J Balvin (Géneros: reggaeton, latin)
- Bad Bunny (Géneros: reggaeton, trap latino, latin, urbano latino)
- KAROL G (Géneros: reggaeton, latin, urbano latino)

Comunidad 8:
- Feid (Géneros: reggaeton, urbano latino)
- Bryant Myers (Géneros: trap latino, reggaeton, trap, urbano latino, dembow)
- SAIKO (Géneros: N/A)

Comunidad 9:
- Artist.Zm (Géneros: N/A)

Comunidad 10:
- Wisin & Yandel (Géneros: reggaeton, urbano latino)

Comunidad 11:
- Jerry Di (Géneros: reggaeton)

Comunidad 12:
- Artist Moon (Géneros: N/A)

Comunidad 13:
- Manuel Turizo (Géneros: reggaeton, latin, colombian pop)
- Sebastian Yatra (Géneros: colombian pop, reggaeton, latin)
- Beéle (Géneros: reggaeton)

Comunidad 14:
- Marshmello (Géneros: edm)
- Bastille (Géneros: N/A)
- Kane Brown (Géneros: country, pop country)

Comunidad 15:
- The Artist Ren (Géneros: N/A)

Comunidad 16:
- Jatin-Lalit (Géneros: bollywood, hindi pop, desi)

Comunidad 17:
- Camila Cabello (Géneros: pop)

Comunidad 18:
- Xavier Rudd (Géneros: N/A)

Comunidad 19:
- New Artist Spotlight (Géneros: N/A)

Comunidad 20:
- La Pantera (Géneros: N/A)
- Juseph (Géneros: N/A)
- ABHIR (Géneros: N/A)

Comunidad 21:
- Artist Joe Smith (Géneros: N/A)

Comunidad 22:
- Nachtdienst (Géneros: N/A)

Comunidad 23:
- All Artist Adella (Géneros: dangdut, sholawat)

Comunidad 24:
- Soolking (Géneros: pop urbaine)
- GIMS (Géneros: french pop, pop urbaine)
- DYSTINCT (Géneros: moroccan pop, raï)

Comunidad 25:
- FAVE (Géneros: afrobeats, afrobeat, afropop, alté, afro soul)

Comunidad 26:
- Rich Kalashh (Géneros: N/A)

Comunidad 27:
- nan (Géneros: N/A)
- nan (Géneros: N/A)

Comunidad 28:
- Natanael Cano (Géneros: corridos tumbados, corrido, corridos bélicos, sad sierreño, electro corridos, sierreño, música mexicana, banda)

Comunidad 29:
- Dhurata Dora (Géneros: N/A)
- Yll Limani (Géneros: N/A)
- Don Xhoni (Géneros: N/A)

Comunidad 30:
- The Band CAMINO (Géneros: N/A)

Comunidad 31:
- ACM Awards New Artist Nominees (Géneros: N/A)

Comunidad 32:
- Came Beats (Géneros: N/A)
- Soto Asa (Géneros: neoperreo)
- Yung Beef (Géneros: neoperreo)

Comunidad 33:
- RAC (Géneros: N/A)

Comunidad 34:
- Artists for Haiti (Géneros: N/A)

Comunidad 35:
- Les Artistes Maajabu (Géneros: african gospel, gospel)

Comunidad 36:
- Unknown Artist LTG (Géneros: N/A)

Comunidad 37:
- PM Artist Sessions Project (Géneros: classical)

Modularidad de la partición: 0.7535

Interpretación:
- Se han identificado 38 comunidades distintas en la red.
- La modularidad de 0.75 indica una estructura comunitaria fuerte,
  lo que sugiere que los artistas tienden a agruparse en comunidades bien definidas.

Análisis de homogeneidad de géneros por comunidad:

Comunidad 0 - Géneros principales:
- argentine trap: 11 ocurrencias
- cumbia: 7 ocurrencias
- cuarteto: 6 ocurrencias

Comunidad 1 - Géneros principales:
- trap latino: 5 ocurrencias
- urbano latino: 3 ocurrencias
- neoperreo: 2 ocurrencias

Comunidad 2 - Géneros principales:
- moombahton: 1 ocurrencias

Comunidad 3 - Géneros principales:
- latin pop: 4 ocurrencias
- reggaeton: 3 ocurrencias
- colombian pop: 2 ocurrencias

Comunidad 4 - Géneros principales:
- opera: 1 ocurrencias

Comunidad 7 - Géneros principales:
- reggaeton: 20 ocurrencias
- latin: 14 ocurrencias
- trap latino: 9 ocurrencias

Comunidad 8 - Géneros principales:
- reggaeton: 10 ocurrencias
- urbano latino: 6 ocurrencias
- trap latino: 6 ocurrencias

Comunidad 10 - Géneros principales:
- reggaeton: 1 ocurrencias
- urbano latino: 1 ocurrencias

Comunidad 11 - Géneros principales:
- reggaeton: 1 ocurrencias

Comunidad 13 - Géneros principales:
- latin pop: 10 ocurrencias
- colombian pop: 7 ocurrencias
- reggaeton: 7 ocurrencias

Comunidad 14 - Géneros principales:
- edm: 1 ocurrencias
- country: 1 ocurrencias
- pop country: 1 ocurrencias

Comunidad 16 - Géneros principales:
- bollywood: 1 ocurrencias
- hindi pop: 1 ocurrencias
- desi: 1 ocurrencias

Comunidad 17 - Géneros principales:
- pop: 1 ocurrencias

Comunidad 23 - Géneros principales:
- dangdut: 1 ocurrencias
- sholawat: 1 ocurrencias

Comunidad 24 - Géneros principales:
- pop urbaine: 24 ocurrencias
- french pop: 3 ocurrencias
- drill: 3 ocurrencias

Comunidad 25 - Géneros principales:
- afrobeats: 1 ocurrencias
- afrobeat: 1 ocurrencias
- afropop: 1 ocurrencias

Comunidad 28 - Géneros principales:
- corridos tumbados: 1 ocurrencias
- corrido: 1 ocurrencias
- corridos bélicos: 1 ocurrencias

Comunidad 29 - Géneros principales:
- german hip hop: 2 ocurrencias
- dancehall: 1 ocurrencias

Comunidad 32 - Géneros principales:
- neoperreo: 2 ocurrencias
- drill: 1 ocurrencias
- reggaeton: 1 ocurrencias

Comunidad 35 - Géneros principales:
- african gospel: 1 ocurrencias
- gospel: 1 ocurrencias

Comunidad 37 - Géneros principales:
- classical: 1 ocurrencias

7. ANÁLISIS GLOBAL E INTEGRACIÓN DE MÉTRICAS
--------------------------------------------------
Artistas más influyentes según diferentes métricas:

Top 5 por grado total:
- Mau y Ricky: 31
- Maria Becerra: 23
- Anuel AA: 21
- Lola Indigo: 20
- Soolking: 19

Top 5 por intermediación:
- Lola Indigo: 0.0644
- Maria Becerra: 0.0528
- Manuel Turizo: 0.0396
- Mau y Ricky: 0.0351
- Soolking: 0.0319

Top 5 por PageRank:
- Soolking: 0.0092
- nan: 0.0062
- GIMS: 0.0060
- Lola Indigo: 0.0058
- DYSTINCT: 0.0058

Correlación entre métricas de centralidad:
- grado_total vs grado_salida: 0.9713
- grado_total vs cercania: 0.8718
- grado_salida vs cercania: 0.8496
- grado_entrada vs pagerank: 0.8396
- grado_salida vs hub_score: 0.8305

Distribución de métricas por comunidad:

Comunidad 0:
- Número de artistas: 33
- PageRank promedio: 0.0039
- Grado total promedio: 3.82
- Intermediación promedio: 0.0038

Comunidad 1:
- Número de artistas: 10
- PageRank promedio: 0.0038
- Grado total promedio: 2.40
- Intermediación promedio: 0.0004

Comunidad 2:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 3:
- Número de artistas: 14
- PageRank promedio: 0.0038
- Grado total promedio: 2.43
- Intermediación promedio: 0.0018

Comunidad 4:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 5:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 6:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 7:
- Número de artistas: 34
- PageRank promedio: 0.0038
- Grado total promedio: 3.24
- Intermediación promedio: 0.0013

Comunidad 8:
- Número de artistas: 30
- PageRank promedio: 0.0038
- Grado total promedio: 2.60
- Intermediación promedio: 0.0012

Comunidad 9:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 10:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 11:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 12:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 13:
- Número de artistas: 31
- PageRank promedio: 0.0037
- Grado total promedio: 2.77
- Intermediación promedio: 0.0032

Comunidad 14:
- Número de artistas: 9
- PageRank promedio: 0.0038
- Grado total promedio: 2.11
- Intermediación promedio: 0.0004

Comunidad 15:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 16:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 17:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 18:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 19:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 20:
- Número de artistas: 9
- PageRank promedio: 0.0037
- Grado total promedio: 2.00
- Intermediación promedio: 0.0004

Comunidad 21:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 22:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 23:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 24:
- Número de artistas: 47
- PageRank promedio: 0.0042
- Grado total promedio: 3.13
- Intermediación promedio: 0.0012

Comunidad 25:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 26:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 27:
- Número de artistas: 2
- PageRank promedio: 0.0048
- Grado total promedio: 1.00
- Intermediación promedio: 0.0000

Comunidad 28:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 29:
- Número de artistas: 7
- PageRank promedio: 0.0039
- Grado total promedio: 2.00
- Intermediación promedio: 0.0004

Comunidad 30:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 31:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 32:
- Número de artistas: 8
- PageRank promedio: 0.0038
- Grado total promedio: 2.00
- Intermediación promedio: 0.0004

Comunidad 33:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 34:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 35:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 36:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Comunidad 37:
- Número de artistas: 1
- PageRank promedio: 0.0034
- Grado total promedio: 0.00
- Intermediación promedio: 0.0000

Influencers principales por comunidad:

Comunidad 0:
- Principal influencer: Lola Indigo
- PageRank: 0.0058
- Grado total: 20

Comunidad 1:
- Principal influencer: Bizarrap
- PageRank: 0.0042
- Grado total: 2

Comunidad 2:
- Principal influencer: Nesim Najih
- PageRank: 0.0034
- Grado total: 0

Comunidad 3:
- Principal influencer: Morat
- PageRank: 0.0045
- Grado total: 3

Comunidad 4:
- Principal influencer: Artist Unknown
- PageRank: 0.0034
- Grado total: 0

Comunidad 5:
- Principal influencer: artistbasm
- PageRank: 0.0034
- Grado total: 0

Comunidad 6:
- Principal influencer: Belinda Carlisle
- PageRank: 0.0034
- Grado total: 0

Comunidad 7:
- Principal influencer: Quevedo
- PageRank: 0.0052
- Grado total: 14

Comunidad 8:
- Principal influencer: SAIKO
- PageRank: 0.0053
- Grado total: 16

Comunidad 9:
- Principal influencer: Artist.Zm
- PageRank: 0.0034
- Grado total: 0

Comunidad 10:
- Principal influencer: Wisin & Yandel
- PageRank: 0.0034
- Grado total: 0

Comunidad 11:
- Principal influencer: Jerry Di
- PageRank: 0.0034
- Grado total: 0

Comunidad 12:
- Principal influencer: Artist Moon
- PageRank: 0.0034
- Grado total: 0

Comunidad 13:
- Principal influencer: Manuel Turizo
- PageRank: 0.0047
- Grado total: 12

Comunidad 14:
- Principal influencer: Fuerza Regida
- PageRank: 0.0042
- Grado total: 2

Comunidad 15:
- Principal influencer: The Artist Ren
- PageRank: 0.0034
- Grado total: 0

Comunidad 16:
- Principal influencer: Jatin-Lalit
- PageRank: 0.0034
- Grado total: 0

Comunidad 17:
- Principal influencer: Camila Cabello
- PageRank: 0.0034
- Grado total: 0

Comunidad 18:
- Principal influencer: Xavier Rudd
- PageRank: 0.0034
- Grado total: 0

Comunidad 19:
- Principal influencer: New Artist Spotlight
- PageRank: 0.0034
- Grado total: 0

Comunidad 20:
- Principal influencer: La Pantera
- PageRank: 0.0038
- Grado total: 10

Comunidad 21:
- Principal influencer: Artist Joe Smith
- PageRank: 0.0034
- Grado total: 0

Comunidad 22:
- Principal influencer: Nachtdienst
- PageRank: 0.0034
- Grado total: 0

Comunidad 23:
- Principal influencer: All Artist Adella
- PageRank: 0.0034
- Grado total: 0

Comunidad 24:
- Principal influencer: Soolking
- PageRank: 0.0092
- Grado total: 19

Comunidad 25:
- Principal influencer: FAVE
- PageRank: 0.0034
- Grado total: 0

Comunidad 26:
- Principal influencer: Rich Kalashh
- PageRank: 0.0034
- Grado total: 0

Comunidad 27:
- Principal influencer: nan
- PageRank: 0.0062
- Grado total: 1

Comunidad 28:
- Principal influencer: Natanael Cano
- PageRank: 0.0034
- Grado total: 0

Comunidad 29:
- Principal influencer: Dhurata Dora
- PageRank: 0.0042
- Grado total: 8

Comunidad 30:
- Principal influencer: The Band CAMINO
- PageRank: 0.0034
- Grado total: 0

Comunidad 31:
- Principal influencer: ACM Awards New Artist Nominees
- PageRank: 0.0034
- Grado total: 0

Comunidad 32:
- Principal influencer: Came Beats
- PageRank: 0.0038
- Grado total: 9

Comunidad 33:
- Principal influencer: RAC
- PageRank: 0.0034
- Grado total: 0

Comunidad 34:
- Principal influencer: Artists for Haiti
- PageRank: 0.0034
- Grado total: 0

Comunidad 35:
- Principal influencer: Les Artistes Maajabu
- PageRank: 0.0034
- Grado total: 0

Comunidad 36:
- Principal influencer: Unknown Artist LTG
- PageRank: 0.0034
- Grado total: 0

Comunidad 37:
- Principal influencer: PM Artist Sessions Project
- PageRank: 0.0034
- Grado total: 0

CONCLUSIONES GLOBALES:
--------------------------------------------------
1. Estructura general de la red:
   - La red muestra una estructura de comunidades bien definidas
   - Existen artistas que actúan como puentes entre comunidades
   - La distribución del grado sigue un patrón donde pocos artistas tienen muchas conexiones

2. Artistas más influyentes:
   - Soolking destaca como el artista más influyente según PageRank

3. Relación entre métricas:
   - Las diferentes métricas de centralidad muestran correlaciones que revelan
     cómo la influencia se distribuye en esta red de artistas
   - La comparación entre PageRank y seguidores muestra cómo la influencia en la red
     se relaciona con la popularidad general

Visualización de la red guardada como 'red_artistas.png'
Resultados integrados guardados en 'resultados_analisis_red.csv'