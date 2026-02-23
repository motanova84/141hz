#!/usr/bin/env python3
"""
Tests for validate_qcal_random_noise.py

Verifica que la validación de ruido aleatorio funciona correctamente
y que los criterios de éxito son razonables.
"""

import unittest
import sys
import os
import json
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.validate_qcal_random_noise import (
    generar_textos_aleatorios,
    generar_textos_semanticos,
    qcal_embed_text,
    proyectar_svd,
    calcular_silhouette_score,
    clustering_simple_kmeans,
    validar_qcal_ruido_aleatorio,
    F0, PHI, KAPPA_PI, ZETA_PRIME_HALF
)


class TestGeneracionTextos(unittest.TestCase):
    """Tests para generación de textos."""
    
    def test_generar_textos_aleatorios(self):
        """Verifica que se generan textos aleatorios correctamente."""
        textos = generar_textos_aleatorios(n_samples=10, min_length=20, max_length=50)
        
        self.assertEqual(len(textos), 10)
        for texto in textos:
            self.assertIsInstance(texto, str)
            self.assertGreater(len(texto), 0)
            words = texto.split()
            self.assertGreaterEqual(len(words), 20)
            self.assertLessEqual(len(words), 50)
    
    def test_generar_textos_semanticos(self):
        """Verifica que se generan textos semánticos correctamente."""
        textos = generar_textos_semanticos(n_samples=10)
        
        self.assertEqual(len(textos), 10)
        for texto in textos:
            self.assertIsInstance(texto, str)
            self.assertGreater(len(texto), 0)
    
    def test_textos_semanticos_contienen_keywords(self):
        """Verifica que textos semánticos contienen palabras clave QCAL."""
        textos = generar_textos_semanticos(n_samples=30)  # Más muestras para mayor confianza
        
        # Al menos algunos textos deben contener keywords QCAL
        keywords = ['frecuencia', 'cuántic', 'coherencia', 'operador', 'función',
                   'espectral', 'resonancia', 'eigenvalor', 'autovalor', 'noétic']
        textos_con_keywords = 0
        
        for texto in textos:
            texto_lower = texto.lower()
            if any(kw in texto_lower for kw in keywords):
                textos_con_keywords += 1
        
        # Al menos 30% de textos deben tener keywords (ajustado a un umbral más realista)
        self.assertGreater(textos_con_keywords, len(textos) * 0.3)


class TestEmbedding(unittest.TestCase):
    """Tests para embedding QCAL."""
    
    def test_qcal_embed_dimension(self):
        """Verifica que el embedding tiene la dimensión correcta."""
        texto = "La frecuencia fundamental es 141.7001 Hz"
        embedding = qcal_embed_text(texto, dimension=64)
        
        self.assertEqual(embedding.shape, (64,))
    
    def test_qcal_embed_normalizacion(self):
        """Verifica que el embedding está normalizado."""
        texto = "La frecuencia fundamental es 141.7001 Hz"
        embedding = qcal_embed_text(texto, dimension=64)
        
        norm = np.linalg.norm(embedding)
        self.assertAlmostEqual(norm, 1.0, places=5)
    
    def test_qcal_embed_determinista(self):
        """Verifica que el embedding es determinista."""
        texto = "La frecuencia fundamental es 141.7001 Hz"
        embedding1 = qcal_embed_text(texto, dimension=64)
        embedding2 = qcal_embed_text(texto, dimension=64)
        
        np.testing.assert_array_almost_equal(embedding1, embedding2)
    
    def test_qcal_embed_diferentes_textos(self):
        """Verifica que textos diferentes tienen embeddings diferentes."""
        texto1 = "La frecuencia fundamental es 141.7001 Hz"
        texto2 = "El operador noético tiene autovalores complejos"
        
        embedding1 = qcal_embed_text(texto1, dimension=64)
        embedding2 = qcal_embed_text(texto2, dimension=64)
        
        # Los embeddings no deben ser idénticos
        diferencia = np.linalg.norm(embedding1 - embedding2)
        self.assertGreater(diferencia, 0.01)


class TestProyeccion(unittest.TestCase):
    """Tests para proyección SVD."""
    
    def test_proyectar_svd_dimension(self):
        """Verifica que la proyección tiene la dimensión correcta."""
        # Crear datos de prueba
        n_samples = 50
        n_features = 64
        embeddings = np.random.randn(n_samples, n_features)
        
        projected = proyectar_svd(embeddings, n_components=16)
        
        self.assertEqual(projected.shape, (n_samples, 16))
    
    def test_proyectar_svd_preserva_distancias(self):
        """Verifica que SVD preserva distancias relativas aproximadamente."""
        # Crear datos con estructura
        n_samples = 100
        n_features = 64
        
        # Dos clusters bien separados
        cluster1 = np.random.randn(50, n_features) + np.array([5.0] * n_features)
        cluster2 = np.random.randn(50, n_features) - np.array([5.0] * n_features)
        embeddings = np.vstack([cluster1, cluster2])
        
        # Proyectar
        projected = proyectar_svd(embeddings, n_components=16)
        
        # Calcular distancias intra-cluster y inter-cluster
        dist_intra1 = np.mean([
            np.linalg.norm(projected[i] - projected[j])
            for i in range(25) for j in range(i+1, 50)
        ])
        
        dist_inter = np.mean([
            np.linalg.norm(projected[i] - projected[j])
            for i in range(50) for j in range(50, 100)
        ])
        
        # La distancia inter-cluster debe ser mayor que intra-cluster
        self.assertGreater(dist_inter, dist_intra1)


class TestClustering(unittest.TestCase):
    """Tests para clustering y silueta."""
    
    def test_clustering_kmeans_basico(self):
        """Verifica que K-means devuelve etiquetas correctas."""
        # Crear datos con 3 clusters claros
        n_per_cluster = 20
        cluster1 = np.random.randn(n_per_cluster, 16) + np.array([10.0] * 16)
        cluster2 = np.random.randn(n_per_cluster, 16) - np.array([10.0] * 16)
        cluster3 = np.random.randn(n_per_cluster, 16) + np.array([0.0] * 16)
        
        embeddings = np.vstack([cluster1, cluster2, cluster3])
        
        labels = clustering_simple_kmeans(embeddings, n_clusters=3, max_iter=100)
        
        self.assertEqual(len(labels), n_per_cluster * 3)
        self.assertEqual(len(np.unique(labels)), 3)
    
    def test_silhouette_score_clusters_buenos(self):
        """Verifica que clusters bien separados tienen silueta alta."""
        # Crear datos con 2 clusters muy separados
        n_per_cluster = 30
        cluster1 = np.random.randn(n_per_cluster, 16) + np.array([20.0] * 16)
        cluster2 = np.random.randn(n_per_cluster, 16) - np.array([20.0] * 16)
        
        embeddings = np.vstack([cluster1, cluster2])
        labels = np.array([0] * n_per_cluster + [1] * n_per_cluster)
        
        score = calcular_silhouette_score(embeddings, labels)
        
        # Clusters bien separados deben tener silueta > 0.5
        self.assertGreater(score, 0.5)
    
    def test_silhouette_score_ruido(self):
        """Verifica que ruido aleatorio tiene silueta baja."""
        # Crear datos completamente aleatorios
        n_samples = 100
        embeddings = np.random.randn(n_samples, 16)
        
        # Clustering arbitrario
        labels = clustering_simple_kmeans(embeddings, n_clusters=5, max_iter=50)
        
        score = calcular_silhouette_score(embeddings, labels)
        
        # Ruido debe tener silueta muy baja (cercana a 0)
        self.assertLess(score, 0.3)


class TestValidacionCompleta(unittest.TestCase):
    """Tests para validación completa."""
    
    def test_validacion_retorna_dict(self):
        """Verifica que la validación retorna un diccionario."""
        resultados = validar_qcal_ruido_aleatorio(
            n_samples=50,  # Menos muestras para test rápido
            dimension_embedding=32,
            dimension_proyeccion=16,
            n_clusters=5,
            seed=12345
        )
        
        self.assertIsInstance(resultados, dict)
    
    def test_validacion_contiene_campos_requeridos(self):
        """Verifica que los resultados contienen todos los campos esperados."""
        resultados = validar_qcal_ruido_aleatorio(
            n_samples=50,
            dimension_embedding=32,
            dimension_proyeccion=16,
            n_clusters=5,
            seed=12345
        )
        
        # Campos obligatorios
        self.assertIn('timestamp', resultados)
        self.assertIn('seed', resultados)
        self.assertIn('parametros', resultados)
        self.assertIn('constantes_qcal', resultados)
        self.assertIn('silhouette_scores', resultados)
        self.assertIn('criterios_validacion', resultados)
        self.assertIn('validacion_exitosa', resultados)
        self.assertIn('distribucion_clusters', resultados)
    
    def test_validacion_reproducible(self):
        """Verifica que la validación es reproducible con la misma semilla."""
        resultados1 = validar_qcal_ruido_aleatorio(
            n_samples=50,
            dimension_embedding=32,
            dimension_proyeccion=16,
            n_clusters=5,
            seed=99999
        )
        
        resultados2 = validar_qcal_ruido_aleatorio(
            n_samples=50,
            dimension_embedding=32,
            dimension_proyeccion=16,
            n_clusters=5,
            seed=99999
        )
        
        # Los scores deben ser idénticos
        self.assertAlmostEqual(
            resultados1['silhouette_scores']['aleatorio'],
            resultados2['silhouette_scores']['aleatorio'],
            places=10
        )
        self.assertAlmostEqual(
            resultados1['silhouette_scores']['semantico'],
            resultados2['silhouette_scores']['semantico'],
            places=10
        )
    
    def test_constantes_qcal_correctas(self):
        """Verifica que las constantes QCAL son las correctas."""
        resultados = validar_qcal_ruido_aleatorio(
            n_samples=50,
            dimension_embedding=32,
            dimension_proyeccion=16,
            n_clusters=5,
            seed=12345
        )
        
        constantes = resultados['constantes_qcal']
        self.assertAlmostEqual(constantes['f0_hz'], 141.7001, places=4)
        self.assertAlmostEqual(constantes['phi'], 1.618033988749895, places=10)
        self.assertAlmostEqual(constantes['kappa_pi'], 2.5782, places=4)


class TestConstantes(unittest.TestCase):
    """Tests para constantes QCAL."""
    
    def test_constantes_definidas(self):
        """Verifica que todas las constantes están definidas."""
        self.assertIsNotNone(F0)
        self.assertIsNotNone(PHI)
        self.assertIsNotNone(KAPPA_PI)
        self.assertIsNotNone(ZETA_PRIME_HALF)
    
    def test_valores_constantes(self):
        """Verifica que las constantes tienen valores correctos."""
        self.assertAlmostEqual(F0, 141.7001, places=4)
        self.assertAlmostEqual(PHI, 1.618033988749895, places=10)
        self.assertAlmostEqual(KAPPA_PI, 2.5782, places=4)
        self.assertAlmostEqual(ZETA_PRIME_HALF, -1.460, places=3)


if __name__ == '__main__':
    unittest.main()
