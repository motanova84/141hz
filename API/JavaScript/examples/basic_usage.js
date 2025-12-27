/**
 * QC-LLM JavaScript Example
 * 
 * Demonstrates basic usage of the qc-llm-js package
 */

const { QC_LLM, F0 } = require('../qc-llm-js/src/validator');

console.log('='.repeat(60));
console.log('QC-LLM JavaScript Example');
console.log('='.repeat(60));
console.log(`Fundamental Frequency: f₀ = ${F0} Hz\n`);

// Initialize validator
const validator = new QC_LLM('demo-model');

// Example texts
const examples = [
  {
    name: "High Quality",
    text: "Quantum coherence in language models represents a fundamental alignment with natural information structures. By measuring spectral properties of semantic embeddings against the universal frequency f₀ = 141.7001 Hz, we can quantify the inherent quality and clarity of generated text."
  },
  {
    name: "Medium Quality",
    text: "Language models generate text. Some text is better than other text. Coherence is important for quality."
  },
  {
    name: "Low Quality",
    text: "words text stuff things model coherence quantum stuff"
  }
];

// Validate each example
console.log('Validation Results:\n');
console.log('-'.repeat(60));

examples.forEach((example, i) => {
  console.log(`\n${i + 1}. ${example.name}`);
  console.log(`Text: "${example.text.substring(0, 60)}${example.text.length > 60 ? '...' : ''}"`);
  
  const result = validator.validate(example.text);
  
  console.log(`   Coherence: ${(result.coherence * 100).toFixed(1)}%`);
  console.log(`   Frequency Alignment: ${(result.frequency_alignment * 100).toFixed(1)}%`);
  console.log(`   Quantum Entropy: ${(result.quantum_entropy * 100).toFixed(1)}%`);
  console.log(`   Recommendation: ${result.recommendation}`);
});

console.log('\n' + '='.repeat(60));

// Batch validation example
console.log('\nBatch Validation Example:\n');
const texts = examples.map(e => e.text);
const results = validator.batchValidate(texts);

const avgCoherence = results.reduce((sum, r) => sum + r.coherence, 0) / results.length;
console.log(`Average Coherence: ${(avgCoherence * 100).toFixed(1)}%`);

const highQuality = results.filter(r => r.coherence > 0.8).length;
console.log(`High Quality Texts: ${highQuality}/${results.length}`);

console.log('\n' + '='.repeat(60));
console.log('Done!');
