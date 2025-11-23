# QC-LLM JavaScript Package

Quantum Coherence validator for Language Models - JavaScript/TypeScript edition

## Installation

```bash
npm install qc-llm-js
```

## Usage

### Basic Validation

```typescript
import { QC_LLM } from 'qc-llm-js';

const validator = new QC_LLM();
const result = validator.validate("Your text here");

console.log(`Coherence: ${(result.coherence * 100).toFixed(1)}%`);
// Output: Coherence: 87.3%
```

### Batch Validation

```typescript
const texts = [
  "First text to validate",
  "Second text to validate",
  "Third text to validate"
];

const results = validator.batchValidate(texts);
results.forEach((result, i) => {
  console.log(`Text ${i + 1}: ${(result.coherence * 100).toFixed(1)}%`);
});
```

### Get Fundamental Frequency

```typescript
import { F0, QC_LLM } from 'qc-llm-js';

console.log(`Fundamental frequency: ${F0} Hz`);
// Or
console.log(`Frequency: ${QC_LLM.getFrequency()} Hz`);
```

## API Reference

### `QC_LLM`

Main validator class.

#### Constructor

```typescript
constructor(modelName?: string)
```

- `modelName`: Optional model name identifier (default: "default")

#### Methods

##### `validate(text: string): CoherenceResult`

Validates a single text.

**Parameters:**
- `text`: Text to validate

**Returns:** `CoherenceResult` object with:
- `coherence`: Overall coherence score [0-1]
- `frequency_alignment`: Alignment with f₀ [0-1]
- `quantum_entropy`: Quantum entropy measure [0-1]
- `recommendation`: Text recommendation
- `frequency`: Target frequency (141.7001 Hz)
- `version`: Validator version

##### `batchValidate(texts: string[]): CoherenceResult[]`

Validates multiple texts.

##### `static getFrequency(): number`

Returns the fundamental frequency f₀ = 141.7001 Hz.

## Mathematical Foundation

The fundamental frequency derives from:

```
f₀ = √2 × f_ref = √2 × (55100/550) ≈ 141.7001 Hz

where:
  f_ref = k × |ζ'(1/2)| × φ³
  k ≈ 16.195 (dimensional scale factor)
```

## License

MIT

## Author

José Manuel Mota Burruezo (JMMB Ψ ✧ ∞³)

## Links

- **Repository**: https://github.com/motanova84/141hz
- **Documentation**: https://motanova84.github.io/141hz
- **DOI**: 10.5281/zenodo.17379721
