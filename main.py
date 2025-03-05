import logging
import time
from analyzer import (
    cargar_datos,
    analisis_centralidad_grado,
    analisis_centralidad_intermediacion_cercania,
    analisis_pagerank,
    analisis_hits,
    analisis_excentricidad_diametro,
    analisis_comunidades,
    analisis_global,
    visualizar_red
)

def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('network_analysis.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main function to run the network analysis."""
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Start timing
        start_time = time.time()
        logger.info("Starting network analysis...")

        # Load data and create graph
        logger.info("Loading data and creating graph...")
        G, nodos, aristas = cargar_datos()
        logger.info(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

        # Run all analyses
        logger.info("Running degree centrality analysis...")
        df_degree = analisis_centralidad_grado(G)

        logger.info("Running betweenness and closeness centrality analysis...")
        df_centrality = analisis_centralidad_intermediacion_cercania(G)

        logger.info("Running PageRank analysis...")
        df_pagerank = analisis_pagerank(G)

        logger.info("Running HITS analysis...")
        df_hits = analisis_hits(G)

        logger.info("Running eccentricity and diameter analysis...")
        df_eccentricity, diametro, radio = analisis_excentricidad_diametro(G)

        logger.info("Running community analysis...")
        df_communities, modularidad = analisis_comunidades(G)

        logger.info("Running global analysis...")
        df_integrated = analisis_global(
            G, df_degree, df_centrality, df_pagerank, 
            df_hits, df_communities
        )

        logger.info("Generating network visualization...")
        visualizar_red(G, df_communities, df_pagerank)

        # Save results
        df_integrated.to_csv('resultados_analisis_red.csv', index=False)
        logger.info("Results saved to 'resultados_analisis_red.csv'")

        # Calculate and log execution time
        execution_time = time.time() - start_time
        logger.info(f"Analysis completed successfully in {execution_time:.2f} seconds")

    except FileNotFoundError as e:
        logger.error(f"Required data files not found: {e}")
    except Exception as e:
        logger.error(f"An error occurred during analysis: {e}", exc_info=True)

if __name__ == "__main__":
    main() 