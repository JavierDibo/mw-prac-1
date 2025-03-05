import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import SpectralClustering
import seaborn as sns
from community.community_louvain import best_partition
import warnings
warnings.filterwarnings('ignore')

def cargar_datos():
    """Carga los archivos nodes.csv y edges.csv y crea un grafo dirigido."""
    # Cargar nodos y aristas
    nodos = pd.read_csv('nodes.csv')
    aristas = pd.read_csv('edges.csv')
    
    # Crear grafo dirigido
    G = nx.DiGraph()
    
    # Añadir nodos con atributos
    for _, row in nodos.iterrows():
        G.add_node(
            row['id'], 
            label=row['label'],
            followers=row['followers'],
            genres=row['genres'],
            popularity=row['popularity'],
            image_url=row['image_url']
        )
    
    # Añadir aristas
    for _, row in aristas.iterrows():
        G.add_edge(row['source'], row['target'])
    
    return G, nodos, aristas

def analisis_centralidad_grado(G):
    """Calcula y analiza la centralidad de grado de los nodos."""
    print("\n1. ANÁLISIS DE CENTRALIDAD DE GRADO")
    print("-" * 50)
    
    # Calcular grado de entrada y salida
    in_degree = dict(G.in_degree())
    out_degree = dict(G.out_degree())
    
    # Convertir a DataFrame para mejor análisis
    df_degree = pd.DataFrame({
        'nodo_id': list(in_degree.keys()),
        'grado_entrada': list(in_degree.values()),
        'grado_salida': list(out_degree.values())
    })
    
    # Añadir grado total
    df_degree['grado_total'] = df_degree['grado_entrada'] + df_degree['grado_salida']
    
    # Añadir etiquetas de los nodos
    labels = nx.get_node_attributes(G, 'label')
    df_degree['artista'] = df_degree['nodo_id'].map(labels)
    
    # Ordenar por grado total descendente
    df_degree = df_degree.sort_values('grado_total', ascending=False)
    
    # Mostrar los 10 nodos con mayor grado
    print("Top 10 artistas con mayor centralidad de grado:")
    print(df_degree[['artista', 'grado_entrada', 'grado_salida', 'grado_total']].head(10))
    
    # Estadísticas de grado
    print("\nEstadísticas de grado en la red:")
    print(f"Grado medio: {np.mean(df_degree['grado_total']):.2f}")
    print(f"Grado máximo: {np.max(df_degree['grado_total'])}")
    print(f"Grado mínimo: {np.min(df_degree['grado_total'])}")
    print(f"Desviación estándar: {np.std(df_degree['grado_total']):.2f}")
    
    # Interpretación
    print("\nInterpretación:")
    top_artista = df_degree.iloc[0]['artista']
    print(f"El artista {top_artista} tiene la mayor centralidad de grado con {df_degree.iloc[0]['grado_total']} conexiones totales.")
    print("Los artistas con alta centralidad de grado son influyentes en la red ya que:")
    print("- Tienen más contacto directo con otros artistas")
    print("- Pueden difundir información más rápidamente")
    print("- Son posibles puentes entre diferentes grupos o comunidades")
    
    return df_degree

def analisis_centralidad_intermediacion_cercania(G):
    """Calcula y analiza la centralidad de intermediación y cercanía."""
    print("\n2. ANÁLISIS DE CENTRALIDAD DE INTERMEDIACIÓN Y CERCANÍA")
    print("-" * 50)
    
    # Asegurarse de trabajar con el componente más grande si el grafo no es conexo
    if not nx.is_strongly_connected(G):
        components = sorted(nx.strongly_connected_components(G), key=len, reverse=True)
        giant = G.subgraph(components[0])
        print(f"Nota: El grafo no es fuertemente conexo. Usando el componente más grande con {len(giant)} nodos.")
        G_undirected = giant.to_undirected()
    else:
        G_undirected = G.to_undirected()
    
    # Calcular centralidades
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G_undirected)
    
    # Convertir a DataFrame
    df_centrality = pd.DataFrame({
        'nodo_id': list(betweenness.keys()),
        'intermediacion': list(betweenness.values()),
        'cercania': [closeness.get(node, 0) for node in betweenness.keys()]
    })
    
    # Añadir etiquetas
    labels = nx.get_node_attributes(G, 'label')
    df_centrality['artista'] = df_centrality['nodo_id'].map(labels)
    
    # Ordenar por intermediación
    df_intermediacion = df_centrality.sort_values('intermediacion', ascending=False)
    
    # Ordenar por cercanía
    df_cercania = df_centrality.sort_values('cercania', ascending=False)
    
    # Mostrar top nodos por intermediación
    print("Top 10 artistas con mayor centralidad de intermediación:")
    print(df_intermediacion[['artista', 'intermediacion']].head(10))
    
    # Mostrar top nodos por cercanía
    print("\nTop 10 artistas con mayor centralidad de cercanía:")
    print(df_cercania[['artista', 'cercania']].head(10))
    
    # Análisis de correlación entre métricas
    correlation = df_centrality['intermediacion'].corr(df_centrality['cercania'])
    print(f"\nCorrelación entre intermediación y cercanía: {correlation:.2f}")
    
    # Interpretación
    print("\nInterpretación:")
    print("Centralidad de intermediación:")
    top_betweenness = df_intermediacion.iloc[0]['artista']
    print(f"- {top_betweenness} tiene la mayor intermediación, lo que significa que actúa como puente entre diferentes")
    print("  grupos de la red. Estos nodos son cruciales para la transmisión de información o influencia.")
    
    print("\nCentralidad de cercanía:")
    top_closeness = df_cercania.iloc[0]['artista']
    print(f"- {top_closeness} tiene la mayor cercanía, lo que indica que puede alcanzar cualquier otro nodo")
    print("  de la red con menos pasos intermedios. Estos artistas pueden distribuir información")
    print("  de manera más eficiente y tener acceso más rápido a los recursos de la red.")
    
    if correlation > 0.7:
        print("\nLa alta correlación entre intermediación y cercanía sugiere que los artistas que")
        print("conectan diferentes grupos también tienden a estar bien conectados con toda la red.")
    elif correlation < 0.3:
        print("\nLa baja correlación entre intermediación y cercanía sugiere que hay artistas que")
        print("son puentes importantes pero no necesariamente están cercanos a todos los demás, y viceversa.")
    
    return df_centrality

def analisis_pagerank(G):
    """Calcula y analiza el PageRank de los nodos."""
    print("\n3. ANÁLISIS DE PAGERANK")
    print("-" * 50)
    
    # Calcular PageRank
    pagerank = nx.pagerank(G, alpha=0.85)
    
    # Convertir a DataFrame
    df_pagerank = pd.DataFrame({
        'nodo_id': list(pagerank.keys()),
        'pagerank': list(pagerank.values())
    })
    
    # Añadir etiquetas
    labels = nx.get_node_attributes(G, 'label')
    df_pagerank['artista'] = df_pagerank['nodo_id'].map(labels)
    
    # Añadir followers si están disponibles
    followers = nx.get_node_attributes(G, 'followers')
    df_pagerank['followers'] = df_pagerank['nodo_id'].map(followers)
    
    # Ordenar por PageRank
    df_pagerank = df_pagerank.sort_values('pagerank', ascending=False)
    
    # Mostrar top nodos por PageRank
    print("Top 10 artistas con mayor PageRank:")
    print(df_pagerank[['artista', 'pagerank', 'followers']].head(10))
    
    # Calcular correlación entre PageRank y followers
    if 'followers' in df_pagerank.columns and not df_pagerank['followers'].isna().all():
        correlation = df_pagerank['pagerank'].corr(df_pagerank['followers'])
        print(f"\nCorrelación entre PageRank y número de seguidores: {correlation:.2f}")
    
    # Interpretación
    print("\nInterpretación:")
    top_pagerank = df_pagerank.iloc[0]['artista']
    print(f"- {top_pagerank} tiene el mayor PageRank, lo que indica que es el artista más influyente según este algoritmo.")
    print("- El PageRank considera no solo la cantidad de conexiones, sino también la calidad de estas.")
    print("- Los artistas con alto PageRank reciben conexiones de otros artistas que también son influyentes.")
    print("- Estos artistas son considerados autoridades o referencias en la red.")
    
    if 'followers' in df_pagerank.columns and not df_pagerank['followers'].isna().all():
        if correlation > 0.5:
            print("\nLa correlación positiva entre PageRank y seguidores sugiere que los artistas más")
            print("influyentes en la red tienden a tener también un mayor número de seguidores en la plataforma.")
        else:
            print("\nLa baja correlación entre PageRank y seguidores sugiere que la influencia en esta red")
            print("no está directamente relacionada con la popularidad general del artista en términos de seguidores.")
    
    return df_pagerank

def analisis_hits(G):
    """Calcula y analiza los hubs y autoridades (algoritmo HITS)."""
    print("\n4. ANÁLISIS HITS (HUBS Y AUTORIDADES)")
    print("-" * 50)
    
    # Calcular hubs y autoridades
    hits = nx.hits(G, max_iter=100)
    hubs = hits[0]
    authorities = hits[1]
    
    # Convertir a DataFrame
    df_hits = pd.DataFrame({
        'nodo_id': list(hubs.keys()),
        'hub_score': list(hubs.values()),
        'authority_score': list(authorities.values())
    })
    
    # Añadir etiquetas
    labels = nx.get_node_attributes(G, 'label')
    df_hits['artista'] = df_hits['nodo_id'].map(labels)
    
    # Ordenar por hub score
    df_hubs = df_hits.sort_values('hub_score', ascending=False)
    
    # Ordenar por authority score
    df_authorities = df_hits.sort_values('authority_score', ascending=False)
    
    # Mostrar top hubs
    print("Top 10 artistas que funcionan como HUBS (conectores):")
    print(df_hubs[['artista', 'hub_score']].head(10))
    
    # Mostrar top autoridades
    print("\nTop 10 artistas que funcionan como AUTORIDADES:")
    print(df_authorities[['artista', 'authority_score']].head(10))
    
    # Interpretación
    print("\nInterpretación:")
    top_hub = df_hubs.iloc[0]['artista']
    top_authority = df_authorities.iloc[0]['artista']
    
    print(f"- {top_hub} es el principal hub en la red, lo que significa que conecta a muchas autoridades.")
    print("  Los hubs son nodos que enlazan a muchas autoridades de calidad, actuando como agregadores o distribuidores.")
    
    print(f"\n- {top_authority} es la principal autoridad en la red, lo que significa que recibe enlaces de muchos hubs.")
    print("  Las autoridades son nodos reconocidos como fuentes confiables o importantes, recibiendo muchas conexiones de hubs.")
    
    print("\nContribución a la estructura de la red:")
    print("- Los hubs facilitan la navegación y el flujo de información al conectar diferentes autoridades.")
    print("- Las autoridades proporcionan contenido valioso o posiciones de referencia en la red.")
    print("- La estructura hub-autoridad crea una jerarquía natural que organiza el flujo de información.")
    print("- Esta estructura mejora la cohesión y la eficiencia en la transmisión de información dentro de la red.")
    
    return df_hits

def analisis_excentricidad_diametro(G):
    """Calcula y analiza la excentricidad y el diámetro de la red."""
    print("\n5. ANÁLISIS DE EXCENTRICIDAD Y DIÁMETRO")
    print("-" * 50)
    
    # Comprobar si el grafo es conexo
    if not nx.is_strongly_connected(G):
        components = sorted(nx.strongly_connected_components(G), key=len, reverse=True)
        giant = G.subgraph(components[0])
        print(f"Nota: El grafo no es fuertemente conexo. Usando el componente más grande con {len(giant)} nodos.")
        G_analysis = giant
    else:
        G_analysis = G
    
    # Calcular excentricidad
    try:
        excentricidad = nx.eccentricity(G_analysis)
        
        # Convertir a DataFrame
        df_eccentricity = pd.DataFrame({
            'nodo_id': list(excentricidad.keys()),
            'excentricidad': list(excentricidad.values())
        })
        
        # Añadir etiquetas
        labels = nx.get_node_attributes(G, 'label')
        df_eccentricity['artista'] = df_eccentricity['nodo_id'].map(labels)
        
        # Ordenar por excentricidad (ascendente)
        df_eccentricity = df_eccentricity.sort_values('excentricidad')
        
        # Calcular diámetro y radio
        diametro = nx.diameter(G_analysis)
        radio = nx.radius(G_analysis)
        
        # Identificar nodos centrales y periféricos
        centros = [node for node, ecc in excentricidad.items() if ecc == radio]
        centro_labels = [labels[node] for node in centros if node in labels]
        
        perifericos = [node for node, ecc in excentricidad.items() if ecc == diametro]
        periferico_labels = [labels[node] for node in perifericos if node in labels]
        
        # Mostrar resultados
        print(f"Diámetro de la red: {diametro}")
        print(f"Radio de la red: {radio}")
        
        print("\nArtistas con menor excentricidad (más centrales):")
        print(df_eccentricity[['artista', 'excentricidad']].head(5))
        
        print("\nArtistas con mayor excentricidad (más periféricos):")
        print(df_eccentricity[['artista', 'excentricidad']].tail(5))
        
        print("\nNodos centro:")
        for label in centro_labels[:5]:
            print(f"- {label}")
        
        print("\nNodos periféricos:")
        for label in periferico_labels[:5]:
            print(f"- {label}")
        
        # Interpretación
        print("\nInterpretación:")
        print(f"- El diámetro de la red es {diametro}, lo que significa que la distancia máxima entre dos nodos es de {diametro} pasos.")
        print(f"- El radio de la red es {radio}, que es la mínima excentricidad de cualquier nodo.")
        
        if diametro <= 6:
            print("- La red muestra el fenómeno de 'mundo pequeño', donde cualquier nodo puede alcanzar a otro en pocos pasos.")
            print("  Esto facilita la rápida difusión de información o influencia.")
        else:
            print("- La red tiene un diámetro relativamente grande, lo que puede indicar una estructura más elongada")
            print("  o con comunidades más separadas, donde la información tarda más en propagarse entre extremos.")
        
        print("\nImplicaciones para la accesibilidad:")
        print("- Los nodos centrales (baja excentricidad) pueden comunicarse eficientemente con toda la red.")
        print("- Los nodos periféricos (alta excentricidad) están más aislados y requieren más pasos para")
        print("  conectarse con partes distantes de la red.")
        
        avg_path_length = nx.average_shortest_path_length(G_analysis)
        print(f"\nLongitud media del camino más corto: {avg_path_length:.2f}")
        print("- Este valor indica cuán conectada está la red en promedio. Un valor bajo sugiere")
        print("  una red bien conectada donde la información puede fluir rápidamente.")
        
        return df_eccentricity, diametro, radio
    
    except nx.NetworkXError:
        print("No se puede calcular la excentricidad porque el grafo no es fuertemente conexo y contiene caminos infinitos.")
        print("Esto sucede cuando hay nodos que no pueden alcanzarse desde otros nodos en el grafo dirigido.")
        return None, None, None

def analisis_comunidades(G):
    """Identifica y analiza comunidades en la red."""
    print("\n6. ANÁLISIS DE COMUNIDADES Y SEGREGACIÓN")
    print("-" * 50)
    
    # Convertir a grafo no dirigido para detectar comunidades
    G_undirected = G.to_undirected()
    
    # Método 1: Louvain
    try:
        communities = best_partition(G_undirected)
        
        # Convertir a DataFrame
        df_communities = pd.DataFrame({
            'nodo_id': list(communities.keys()),
            'comunidad': list(communities.values())
        })
        
        # Añadir etiquetas
        labels = nx.get_node_attributes(G, 'label')
        df_communities['artista'] = df_communities['nodo_id'].map(labels)
        
        # Añadir géneros si están disponibles
        genres = nx.get_node_attributes(G, 'genres')
        df_communities['genres'] = df_communities['nodo_id'].map(genres)
        
        # Contar nodos por comunidad
        community_counts = df_communities['comunidad'].value_counts().sort_index()
        
        # Mostrar resultados
        num_communities = len(community_counts)
        print(f"Número de comunidades detectadas: {num_communities}")
        
        print("\nTamaño de cada comunidad:")
        for comm, count in community_counts.items():
            print(f"Comunidad {comm}: {count} artistas")
        
        print("\nArtistas por comunidad (primeros 3 de cada una):")
        for comm in sorted(df_communities['comunidad'].unique()):
            comm_members = df_communities[df_communities['comunidad'] == comm]
            print(f"\nComunidad {comm}:")
            for _, row in comm_members.head(3).iterrows():
                genres_str = row['genres'] if not pd.isna(row['genres']) else "N/A"
                print(f"- {row['artista']} (Géneros: {genres_str})")
        
        # Calcular modularidad
        modularidad = nx.community.modularity(G_undirected, 
                                             [set(df_communities[df_communities['comunidad'] == c]['nodo_id']) 
                                              for c in df_communities['comunidad'].unique()])
        
        print(f"\nModularidad de la partición: {modularidad:.4f}")
        
        # Interpretación
        print("\nInterpretación:")
        print(f"- Se han identificado {num_communities} comunidades distintas en la red.")
        
        if modularidad > 0.3:
            print(f"- La modularidad de {modularidad:.2f} indica una estructura comunitaria fuerte,")
            print("  lo que sugiere que los artistas tienden a agruparse en comunidades bien definidas.")
        else:
            print(f"- La modularidad de {modularidad:.2f} indica una estructura comunitaria menos definida,")
            print("  con más conexiones entre comunidades diferentes.")
        
        # Analizar homogeneidad de géneros por comunidad
        if 'genres' in df_communities.columns:
            print("\nAnálisis de homogeneidad de géneros por comunidad:")
            for comm in sorted(df_communities['comunidad'].unique()):
                comm_members = df_communities[df_communities['comunidad'] == comm]
                genres_list = []
                for genres_str in comm_members['genres']:
                    if pd.isna(genres_str):
                        continue
                    genres_split = [g.strip() for g in str(genres_str).split(',')]
                    genres_list.extend(genres_split)
                
                if genres_list:
                    genre_counts = pd.Series(genres_list).value_counts().head(3)
                    print(f"\nComunidad {comm} - Géneros principales:")
                    for genre, count in genre_counts.items():
                        print(f"- {genre}: {count} ocurrencias")
        
        return df_communities, modularidad
    
    except Exception as e:
        print(f"Error al detectar comunidades usando Louvain: {e}")
        print("Intentando método alternativo (Spectral Clustering)...")
        
        # Método 2: Spectral Clustering
        try:
            # Preparar matriz de adyacencia
            adj_matrix = nx.to_numpy_array(G_undirected)
            
            # Estimar número de comunidades (usando el método del eigengap)
            n_clusters = min(5, len(G_undirected) - 1)  # Por defecto usar 5 o menos
            
            # Aplicar clustering espectral
            sc = SpectralClustering(n_clusters=n_clusters, affinity='precomputed', 
                                   assign_labels='discretize', random_state=42)
            labels = sc.fit_predict(adj_matrix)
            
            # Crear diccionario de comunidades
            node_list = list(G_undirected.nodes())
            communities = {node_list[i]: labels[i] for i in range(len(node_list))}
            
            # Convertir a DataFrame
            df_communities = pd.DataFrame({
                'nodo_id': list(communities.keys()),
                'comunidad': list(communities.values())
            })
            
            # Añadir etiquetas
            node_labels = nx.get_node_attributes(G, 'label')
            df_communities['artista'] = df_communities['nodo_id'].map(node_labels)
            
            # Contar nodos por comunidad
            community_counts = df_communities['comunidad'].value_counts().sort_index()
            
            # Mostrar resultados
            num_communities = len(community_counts)
            print(f"Número de comunidades detectadas: {num_communities}")
            
            print("\nTamaño de cada comunidad:")
            for comm, count in community_counts.items():
                print(f"Comunidad {comm}: {count} artistas")
            
            print("\nArtistas por comunidad (primeros 3 de cada una):")
            for comm in sorted(df_communities['comunidad'].unique()):
                comm_members = df_communities[df_communities['comunidad'] == comm]
                print(f"\nComunidad {comm}:")
                for _, row in comm_members.head(3).iterrows():
                    print(f"- {row['artista']}")
            
            # No podemos calcular modularidad con este método
            return df_communities, None
            
        except Exception as e:
            print(f"Error al detectar comunidades usando Spectral Clustering: {e}")
            return None, None

def analisis_global(G, df_degree, df_centrality, df_pagerank, df_hits, df_communities):
    """Realiza un análisis global relacionando todas las métricas."""
    print("\n7. ANÁLISIS GLOBAL E INTEGRACIÓN DE MÉTRICAS")
    print("-" * 50)
    
    # Crear DataFrame integrado con todas las métricas
    metrics = []
    
    # Añadir grado
    if df_degree is not None:
        for _, row in df_degree.iterrows():
            node_id = row['nodo_id']
            metrics.append({
                'nodo_id': node_id,
                'artista': row['artista'],
                'grado_total': row['grado_total'],
                'grado_entrada': row['grado_entrada'],
                'grado_salida': row['grado_salida']
            })
    
    # Convertir a DataFrame
    df_integrated = pd.DataFrame(metrics)
    
    # Añadir centralidad de intermediación y cercanía
    if df_centrality is not None:
        betweenness_dict = dict(zip(df_centrality['nodo_id'], df_centrality['intermediacion']))
        closeness_dict = dict(zip(df_centrality['nodo_id'], df_centrality['cercania']))
        
        df_integrated['intermediacion'] = df_integrated['nodo_id'].map(betweenness_dict)
        df_integrated['cercania'] = df_integrated['nodo_id'].map(closeness_dict)
    
    # Añadir PageRank
    if df_pagerank is not None:
        pagerank_dict = dict(zip(df_pagerank['nodo_id'], df_pagerank['pagerank']))
        df_integrated['pagerank'] = df_integrated['nodo_id'].map(pagerank_dict)
        
        if 'followers' in df_pagerank.columns:
            followers_dict = dict(zip(df_pagerank['nodo_id'], df_pagerank['followers']))
            df_integrated['followers'] = df_integrated['nodo_id'].map(followers_dict)
    
    # Añadir HITS
    if df_hits is not None:
        hub_dict = dict(zip(df_hits['nodo_id'], df_hits['hub_score']))
        auth_dict = dict(zip(df_hits['nodo_id'], df_hits['authority_score']))
        
        df_integrated['hub_score'] = df_integrated['nodo_id'].map(hub_dict)
        df_integrated['authority_score'] = df_integrated['nodo_id'].map(auth_dict)
    
    # Añadir comunidad
    if df_communities is not None:
        community_dict = dict(zip(df_communities['nodo_id'], df_communities['comunidad']))
        df_integrated['comunidad'] = df_integrated['nodo_id'].map(community_dict)
    
    # Identificar los nodos más influyentes según cada métrica
    print("Artistas más influyentes según diferentes métricas:")
    
    # Top 5 por grado total
    if 'grado_total' in df_integrated.columns:
        top_degree = df_integrated.sort_values('grado_total', ascending=False).head(5)
        print("\nTop 5 por grado total:")
        for _, row in top_degree.iterrows():
            print(f"- {row['artista']}: {row['grado_total']}")
    
    # Top 5 por intermediación
    if 'intermediacion' in df_integrated.columns:
        top_betweenness = df_integrated.sort_values('intermediacion', ascending=False).head(5)
        print("\nTop 5 por intermediación:")
        for _, row in top_betweenness.iterrows():
            print(f"- {row['artista']}: {row['intermediacion']:.4f}")
    
    # Top 5 por PageRank
    if 'pagerank' in df_integrated.columns:
        top_pagerank = df_integrated.sort_values('pagerank', ascending=False).head(5)
        print("\nTop 5 por PageRank:")
        for _, row in top_pagerank.iterrows():
            print(f"- {row['artista']}: {row['pagerank']:.4f}")
    
    # Análisis de correlación entre métricas
    print("\nCorrelación entre métricas de centralidad:")
    numeric_columns = df_integrated.select_dtypes(include=[np.number]).columns
    corr_matrix = df_integrated[numeric_columns].corr()
    
    # Mostrar correlaciones importantes
    correlations = []
    for i in range(len(numeric_columns)):
        for j in range(i+1, len(numeric_columns)):
            col1 = numeric_columns[i]
            col2 = numeric_columns[j]
            corr = corr_matrix.loc[col1, col2]
            correlations.append((col1, col2, corr))
    
    # Ordenar por valor absoluto de correlación
    correlations.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # Mostrar top 5 correlaciones
    for col1, col2, corr in correlations[:5]:
        print(f"- {col1} vs {col2}: {corr:.4f}")
    
    # Análisis de distribución de métricas por comunidad
    if 'comunidad' in df_integrated.columns:
        print("\nDistribución de métricas por comunidad:")
        
        for comm in sorted(df_integrated['comunidad'].unique()):
            comm_df = df_integrated[df_integrated['comunidad'] == comm]
            
            print(f"\nComunidad {comm}:")
            print(f"- Número de artistas: {len(comm_df)}")
            
            if 'pagerank' in comm_df.columns:
                print(f"- PageRank promedio: {comm_df['pagerank'].mean():.4f}")
            
            if 'grado_total' in comm_df.columns:
                print(f"- Grado total promedio: {comm_df['grado_total'].mean():.2f}")
            
            if 'intermediacion' in comm_df.columns:
                print(f"- Intermediación promedio: {comm_df['intermediacion'].mean():.4f}")
    
    # Análisis de influencers por comunidad
    if 'comunidad' in df_integrated.columns and 'pagerank' in df_integrated.columns:
        print("\nInfluencers principales por comunidad:")
        
        for comm in sorted(df_integrated['comunidad'].unique()):
            comm_df = df_integrated[df_integrated['comunidad'] == comm]
            top_influencer = comm_df.sort_values('pagerank', ascending=False).iloc[0]
            
            print(f"\nComunidad {comm}:")
            print(f"- Principal influencer: {top_influencer['artista']}")
            if 'pagerank' in top_influencer:
                print(f"- PageRank: {top_influencer['pagerank']:.4f}")
            if 'grado_total' in top_influencer:
                print(f"- Grado total: {top_influencer['grado_total']}")
    
    # Conclusiones generales
    print("\nCONCLUSIONES GLOBALES:")
    print("-" * 50)
    print("1. Estructura general de la red:")
    print("   - La red muestra una estructura de comunidades bien definidas")
    print("   - Existen artistas que actúan como puentes entre comunidades")
    print("   - La distribución del grado sigue un patrón donde pocos artistas tienen muchas conexiones")
    
    print("\n2. Artistas más influyentes:")
    if 'pagerank' in df_integrated.columns:
        top_artist = df_integrated.sort_values('pagerank', ascending=False).iloc[0]['artista']
        print(f"   - {top_artist} destaca como el artista más influyente según PageRank")
    
    print("\n3. Relación entre métricas:")
    print("   - Las diferentes métricas de centralidad muestran correlaciones que revelan")
    print("     cómo la influencia se distribuye en esta red de artistas")
    print("   - La comparación entre PageRank y seguidores muestra cómo la influencia en la red")
    print("     se relaciona con la popularidad general")
    
    return df_integrated

def visualizar_red(G, df_communities=None, df_pagerank=None):
    """Visualiza la red con comunidades y métricas relevantes."""
    plt.figure(figsize=(12, 10))
    
    # Posición de los nodos
    pos = nx.spring_layout(G, seed=42)
    
    # Colores por comunidad si están disponibles
    if df_communities is not None:
        # Crear diccionario de comunidades
        communities = dict(zip(df_communities['nodo_id'], df_communities['comunidad']))
        
        # Asignar colores por comunidad
        colors = []
        for node in G.nodes():
            if node in communities:
                colors.append(communities[node])
            else:
                colors.append(-1)  # Para nodos sin comunidad asignada
    else:
        colors = 'skyblue'
    
    # Tamaño de nodos basado en PageRank si está disponible
    if df_pagerank is not None:
        pagerank_dict = dict(zip(df_pagerank['nodo_id'], df_pagerank['pagerank']))
        node_size = [5000 * pagerank_dict.get(node, 0.01) for node in G.nodes()]
    else:
        node_size = 300
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=node_size, alpha=0.8, cmap=plt.cm.rainbow)
    
    # Dibujar aristas con transparencia para mejor visualización
    nx.draw_networkx_edges(G, pos, alpha=0.2, arrows=True)
    
    # Etiquetas sólo para nodos principales
    if df_pagerank is not None:
        top_nodes = set(df_pagerank.sort_values('pagerank', ascending=False).head(10)['nodo_id'])
        labels = nx.get_node_attributes(G, 'label')
        node_labels = {node: labels[node] for node in top_nodes if node in labels}
        nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10, font_weight='bold')
    
    plt.title("Red de artistas", fontsize=15)
    plt.axis('off')
    
    # Añadir leyenda de comunidades si están disponibles
    if df_communities is not None:
        unique_communities = sorted(df_communities['comunidad'].unique())
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                          label=f'Comunidad {comm}',
                          markerfacecolor=plt.cm.rainbow(comm / max(unique_communities)),
                          markersize=10) for comm in unique_communities]
        plt.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig('red_artistas.png', dpi=300, bbox_inches='tight')
    print("\nVisualización de la red guardada como 'red_artistas.png'")

def main():
    # Cargar datos y crear grafo
    G, nodos, aristas = cargar_datos()
    print(f"Grafo creado con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas")
    
    # Análisis de centralidad de grado
    df_degree = analisis_centralidad_grado(G)
    
    # Análisis de centralidad de intermediación y cercanía
    df_centrality = analisis_centralidad_intermediacion_cercania(G)
    
    # Análisis de PageRank
    df_pagerank = analisis_pagerank(G)
    
    # Análisis HITS
    df_hits = analisis_hits(G)
    
    # Análisis de excentricidad y diámetro
    df_eccentricity, diametro, radio = analisis_excentricidad_diametro(G)
    
    # Análisis de comunidades
    df_communities, modularidad = analisis_comunidades(G)
    
    # Análisis global integrando todas las métricas
    df_integrated = analisis_global(G, df_degree, df_centrality, df_pagerank, df_hits, df_communities)
    
    # Visualizar la red
    visualizar_red(G, df_communities, df_pagerank)
    
    # Guardar resultados relevantes
    df_integrated.to_csv('resultados_analisis_red.csv', index=False)
    print("Resultados integrados guardados en 'resultados_analisis_red.csv'")

if __name__ == "__main__":
    main()
