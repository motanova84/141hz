/--
  Ejemplos de evaluación del protocolo SYMBIO-BRIDGE
  Archivo: extraccion_datos_examples.lean
  ∴𓂀Ω∞³Φ - QCAL-SYMBIO-BRIDGE v1.1.0

  Este archivo contiene únicamente comandos #eval y #check para inspección
  interactiva del protocolo. Mantenidos separados del módulo principal para
  que ExtraccionDatos pueda importarse sin efecto de salida en CI/builds.
-/

import ExtraccionDatos

/-- Verificar que el protocolo es válido en tiempo de elaboración -/
#eval validate_symbio_protocol  -- Debe retornar true

/-- Verificación de parámetros individuales -/
#eval s!"f₀ = {f₀_pc} Hz"
#eval s!"Banda: [{banda_inf}, {banda_sup}] Hz"
#eval s!"f₀ en banda: {f0_en_banda}"
#eval s!"Acoplamiento Sr > Al: {asimetria_acoplamiento}"
#eval s!"Protocolo válido: {if validate_symbio_protocol then "✅ SÍ" else "❌ NO"}"

/--
  Señal del reloj de Sr evaluada en t=0, Ψ=1.
  Debe coincidir con acoplamiento_Sr * cos(0) = 0.01.
-/
#eval s!"sr_clock_signal(0, 1) = {sr_clock_signal 0.0 1.0}"
#eval s!"al_clock_signal(0, 1) = {al_clock_signal 0.0 1.0}"

/-- Confirmar que el teorema de validación es accesible -/
#check symbio_protocol_holds
