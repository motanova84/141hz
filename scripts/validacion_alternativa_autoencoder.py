#!/usr/bin/env python3
"""
Validación Alternativa 3: Autoencoders No Supervisados
=======================================================

Hipótesis: Un artefacto instrumental se "aprende" fácilmente.
Una señal real no es fácilmente comprimible sin pérdida.

Implementa:
- Entrenar autoencoder sobre datos limpios sin 141.7 Hz
- Probar reconstrucción de ringdown con y sin 141.7 Hz
- Medir error de reconstrucción sistemático
"""

import numpy as np
from scipy import signal
import warnings
warnings.filterwarnings('ignore')


class SimpleAutoencoder:
    """
    Autoencoder simple usando numpy puro (sin dependencias ML)
    Basado en PCA (Principal Component Analysis) para reducción dimensional
    """

    def __init__(self, n_components=10):
        """
        Parameters:
        -----------
        n_components : int
            Número de componentes principales a retener
        """
        self.n_components = n_components
        self.mean = None
        self.components = None
        self.explained_variance = None

    def fit(self, X):
        """
        Entrenar el autoencoder (calcular PCA)

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            Datos de entrenamiento
        """
        X = np.asarray(X)

        # Centrar los datos
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean

        # Calcular matriz de covarianza
        cov_matrix = np.cov(X_centered.T)

        # Calcular eigenvalores y eigenvectores
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        # Ordenar por eigenvalues (mayor a menor)
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Retener solo n_components
        self.components = eigenvectors[:, :self.n_components]
        self.explained_variance = eigenvalues[:self.n_components]

        return self

    def encode(self, X):
        """
        Codificar datos (proyección en espacio reducido)

        Parameters:
        -----------
        X : array-like
            Datos a codificar

        Returns:
        --------
        array : Datos codificados
        """
        X = np.asarray(X)
        X_centered = X - self.mean
        return np.dot(X_centered, self.components)

    def decode(self, X_encoded):
        """
        Decodificar datos (reconstrucción)

        Parameters:
        -----------
        X_encoded : array-like
            Datos codificados

        Returns:
        --------
        array : Datos reconstruidos
        """
        return np.dot(X_encoded, self.components.T) + self.mean

    def reconstruct(self, X):
        """
        Reconstruir datos (encode + decode)

        Parameters:
        -----------
        X : array-like
            Datos originales

        Returns:
        --------
        array : Datos reconstruidos
        """
        return self.decode(self.encode(X))


def generar_datos_entrenamiento_sin_f0(n_samples=100, n_features=1024,
                                        fs=4096, f_exclude=141.7001,
                                        exclude_bandwidth=5):
    """
    Genera datos de entrenamiento sin la frecuencia objetivo

    Parameters:
    -----------
    n_samples : int
        Número de muestras
    n_features : int
        Longitud de cada muestra temporal
    fs : float
        Frecuencia de muestreo
    f_exclude : float
        Frecuencia a excluir
    exclude_bandwidth : float
        Ancho de banda a excluir alrededor de f_exclude (Hz)

    Returns:
    --------
    array : Datos de entrenamiento, shape (n_samples, n_features)
    """
    datos = []

    for _ in range(n_samples):
        # Generar ruido blanco
        noise = np.random.normal(0, 1, n_features)

        # Aplicar filtro notch para eliminar f_exclude
        # Crear filtro notch
        Q = 30  # Quality factor
        b, a = signal.iirnotch(f_exclude, Q, fs)

        # Aplicar filtro
        filtered = signal.filtfilt(b, a, noise)

        # También crear banda de exclusión más amplia
        if exclude_bandwidth > 0:
            lowcut = f_exclude - exclude_bandwidth
            highcut = f_exclude + exclude_bandwidth

            # Filtro bandstop
            sos = signal.butter(4, [lowcut, highcut], btype='bandstop',
                               fs=fs, output='sos')
            filtered = signal.sosfiltfilt(sos, filtered)

        datos.append(filtered)

    return np.array(datos)


def calcular_error_reconstruccion(data_original, data_reconstruida):
    """
    Calcula métricas de error de reconstrucción

    Parameters:
    -----------
    data_original : array-like
        Datos originales
    data_reconstruida : array-like
        Datos reconstruidos

    Returns:
    --------
    dict : Métricas de error
    """
    original = np.asarray(data_original)
    reconstruida = np.asarray(data_reconstruida)

    # Error medio cuadrático (MSE)
    mse = np.mean((original - reconstruida) ** 2)

    # Error medio absoluto (MAE)
    mae = np.mean(np.abs(original - reconstruida))

    # Error cuadrático medio normalizado (NMSE)
    if np.std(original) > 0:
        nmse = mse / np.var(original)
    else:
        nmse = 0.0

    # Correlación entre original y reconstruido
    if np.std(original) > 0 and np.std(reconstruida) > 0:
        correlation = np.corrcoef(original.flatten(), reconstruida.flatten())[0, 1]
    else:
        correlation = 0.0

    return {
        'mse': float(mse),
        'mae': float(mae),
        'nmse': float(nmse),
        'correlation': float(correlation),
        'rmse': float(np.sqrt(mse))
    }


def analizar_reconstruccion_espectral(data_original, data_reconstruida,
                                      fs=4096, f_target=141.7001):
    """
    Analiza el error de reconstrucción en el dominio espectral

    Parameters:
    -----------
    data_original, data_reconstruida : array-like
        Datos original y reconstruido
    fs : float
        Frecuencia de muestreo
    f_target : float
        Frecuencia objetivo para análisis

    Returns:
    --------
    dict : Análisis espectral del error
    """
    original = np.asarray(data_original)
    reconstruida = np.asarray(data_reconstruida)

    # Calcular PSD de cada señal
    freqs_orig, psd_orig = signal.welch(original, fs=fs, nperseg=min(len(original)//4, 1024))
    freqs_rec, psd_rec = signal.welch(reconstruida, fs=fs, nperseg=min(len(reconstruida)//4, 1024))

    # Error espectral
    error = original - reconstruida
    freqs_err, psd_err = signal.welch(error, fs=fs, nperseg=min(len(error)//4, 1024))

    # Encontrar índice de frecuencia objetivo
    idx_target = np.argmin(np.abs(freqs_err - f_target))

    # Potencia del error en f_target
    error_power_f0 = psd_err[idx_target]
    original_power_f0 = psd_orig[idx_target]

    # Ratio de error en f_target vs banda adyacente
    banda_width = 20
    idx_banda_start = np.argmin(np.abs(freqs_err - (f_target - banda_width)))
    idx_banda_end = np.argmin(np.abs(freqs_err - (f_target + banda_width)))

    # Excluir región cercana a f_target
    exclude_width = 3
    idx_exclude_start = max(0, idx_target - exclude_width)
    idx_exclude_end = min(len(psd_err), idx_target + exclude_width)

    banda_indices = np.concatenate([
        np.arange(idx_banda_start, idx_exclude_start),
        np.arange(idx_exclude_end, idx_banda_end)
    ])

    error_power_banda = np.mean(psd_err[banda_indices]) if len(banda_indices) > 0 else 0

    if error_power_banda > 0:
        error_ratio_f0 = error_power_f0 / error_power_banda
    else:
        error_ratio_f0 = 0

    return {
        'error_power_f0': float(error_power_f0),
        'original_power_f0': float(original_power_f0),
        'error_power_banda': float(error_power_banda),
        'error_ratio_f0': float(error_ratio_f0),
        'freqs': freqs_err,
        'psd_error': psd_err,
        'psd_original': psd_orig,
        'psd_reconstruida': psd_rec
    }


def validar_autoencoder_no_supervisado(data_con_f0, data_sin_f0=None,
                                       fs=4096, f_target=141.7001,
                                       n_components=10):
    """
    Validación completa usando autoencoder

    Parameters:
    -----------
    data_con_f0 : array-like
        Datos que contienen la frecuencia objetivo
    data_sin_f0 : array-like, optional
        Datos sin la frecuencia objetivo (para entrenamiento)
        Si es None, se generan automáticamente
    fs : float
        Frecuencia de muestreo
    f_target : float
        Frecuencia objetivo
    n_components : int
        Número de componentes del autoencoder

    Returns:
    --------
    dict : Resultados de validación
    """
    print("=" * 70)
    print("VALIDACIÓN ALTERNATIVA 3: AUTOENCODER NO SUPERVISADO")
    print("=" * 70)
    print(f"Frecuencia objetivo: {f_target} Hz")
    print(f"Componentes principales: {n_components}")
    print()

    # 1. Preparar datos de entrenamiento
    print("1. Generando datos de entrenamiento sin f0...")

    if data_sin_f0 is None:
        n_samples = 100
        n_features = len(data_con_f0)
        data_sin_f0 = generar_datos_entrenamiento_sin_f0(
            n_samples, n_features, fs, f_target
        )
    else:
        data_sin_f0 = np.asarray(data_sin_f0)
        if len(data_sin_f0.shape) == 1:
            data_sin_f0 = data_sin_f0.reshape(1, -1)

    print(f"   Muestras de entrenamiento: {data_sin_f0.shape[0]}")
    print(f"   Longitud de señal: {data_sin_f0.shape[1]}")
    print()

    # 2. Entrenar autoencoder
    print("2. Entrenando autoencoder (PCA)...")
    autoencoder = SimpleAutoencoder(n_components=n_components)
    autoencoder.fit(data_sin_f0)

    varianza_explicada = np.sum(autoencoder.explained_variance) / np.sum(np.var(data_sin_f0, axis=0))
    print(f"   Varianza explicada: {varianza_explicada*100:.2f}%")
    print()

    # 3. Probar reconstrucción con datos que contienen f0
    print("3. Probando reconstrucción de datos con f0...")

    data_con_f0 = np.asarray(data_con_f0)
    if len(data_con_f0.shape) == 1:
        data_con_f0_2d = data_con_f0.reshape(1, -1)
    else:
        data_con_f0_2d = data_con_f0

    reconstruccion_con_f0 = autoencoder.reconstruct(data_con_f0_2d)

    # 4. Calcular errores
    print("4. Analizando errores de reconstrucción...")

    # Error temporal
    error_temporal = calcular_error_reconstruccion(
        data_con_f0_2d[0], reconstruccion_con_f0[0]
    )

    print(f"   MSE: {error_temporal['mse']:.6e}")
    print(f"   NMSE: {error_temporal['nmse']:.4f}")
    print(f"   Correlación: {error_temporal['correlation']:.4f}")
    print()

    # Error espectral
    print("5. Análisis espectral del error...")
    error_espectral = analizar_reconstruccion_espectral(
        data_con_f0_2d[0], reconstruccion_con_f0[0], fs, f_target
    )

    print(f"   Potencia de error en f0: {error_espectral['error_power_f0']:.6e}")
    print(f"   Potencia de error en banda: {error_espectral['error_power_banda']:.6e}")
    print(f"   Ratio error f0/banda: {error_espectral['error_ratio_f0']:.2f}x")
    print()

    # Criterios de validación
    # Una señal real estructurada debe:
    # 1. Tener error de reconstrucción significativo (NMSE > 0.1)
    # 2. Tener error concentrado en f0 (ratio > 2.0)
    # 3. Baja correlación de reconstrucción (< 0.9)

    validacion_exitosa = (
        error_temporal['nmse'] > 0.1 and
        error_espectral['error_ratio_f0'] > 2.0 and
        error_temporal['correlation'] < 0.9
    )

    # Conclusión
    print("=" * 70)
    print("CONCLUSIÓN:")
    print("=" * 70)

    if validacion_exitosa:
        print("✅ La frecuencia 141.7001 Hz contiene información estructurada no trivial")
        print("   - Error de reconstrucción significativo (NMSE > 0.1)")
        print("   - Error concentrado en f0 (ratio > 2.0x)")
        print("   - Baja compresibilidad sin pérdida")
        print("   - Compatible con señal física real, no artefacto instrumental")
    else:
        print("❌ La señal es fácilmente reconstruible por el autoencoder")
        if error_temporal['nmse'] <= 0.1:
            print(f"   - Error bajo (NMSE = {error_temporal['nmse']:.4f} ≤ 0.1)")
        if error_espectral['error_ratio_f0'] <= 2.0:
            print(f"   - Error no concentrado en f0 (ratio = {error_espectral['error_ratio_f0']:.2f} ≤ 2.0)")
        if error_temporal['correlation'] >= 0.9:
            print(f"   - Alta correlación (r = {error_temporal['correlation']:.4f} ≥ 0.9)")
        print("   - Posible artefacto instrumental comprimible")

    print()

    return {
        'n_components': n_components,
        'varianza_explicada': float(varianza_explicada),
        'error_temporal': error_temporal,
        'error_espectral': error_espectral,
        'validacion_exitosa': validacion_exitosa,
        'autoencoder': autoencoder
    }


if __name__ == '__main__':
    print("Script de validación con autoencoder no supervisado")
    print("Genera datos sintéticos para demostración")
    print()

    # Generar datos sintéticos
    fs = 4096
    duration = 1.0
    t = np.linspace(0, duration, int(fs * duration))
    f0 = 141.7001

    # Datos CON f0: señal + ruido
    signal_component = 0.5 * np.sin(2 * np.pi * f0 * t)
    noise = np.random.normal(0, 0.3, len(t))
    data_con_f0 = signal_component + noise

    # Ejecutar validación
    resultado = validar_autoencoder_no_supervisado(
        data_con_f0, fs=fs, f_target=f0, n_components=15
    )

    print("\n✓ Validación completada")
    print(f"✓ Estado: {'APROBADA' if resultado['validacion_exitosa'] else 'FALLIDA'}")
