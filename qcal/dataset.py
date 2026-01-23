#!/usr/bin/env python3
"""
QCAL Dataset Generator
======================

Generates datasets for evaluating spectral embeddings.
Creates 100-1000 short phrases in simple domains (definitions, QA).

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import random
from typing import List, Tuple, Dict


class DatasetGenerator:
    """Generate datasets for spectral embedding evaluation."""
    
    def __init__(self, random_state: int = 42):
        """
        Initialize dataset generator.
        
        Args:
            random_state: Random seed for reproducibility
        """
        self.random_state = random_state
        random.seed(random_state)
        
    def generate_definitions(self, n_samples: int = 200) -> List[str]:
        """
        Generate definition-style sentences.
        
        Args:
            n_samples: Number of samples to generate
            
        Returns:
            List of definition sentences
        """
        # Template-based definitions
        subjects = [
            "quantum mechanics", "gravity", "resonance", "frequency", "wave",
            "coherence", "energy", "momentum", "amplitude", "phase",
            "photon", "electron", "proton", "neutron", "quark",
            "mathematics", "algebra", "geometry", "topology", "analysis",
            "physics", "chemistry", "biology", "astronomy", "cosmology",
            "light", "sound", "heat", "force", "mass",
            "space", "time", "dimension", "field", "particle"
        ]
        
        properties = [
            "describes", "explains", "represents", "defines", "characterizes",
            "measures", "quantifies", "determines", "governs", "controls"
        ]
        
        concepts = [
            "the behavior of matter and energy",
            "the fundamental forces of nature",
            "the structure of the universe",
            "the properties of subatomic particles",
            "the relationship between space and time",
            "the wave-particle duality",
            "the quantization of energy",
            "the conservation laws",
            "the symmetries in physics",
            "the emergence of complex systems",
            "the mathematical patterns in nature",
            "the geometric structures",
            "the topological invariants",
            "the spectral properties",
            "the resonance phenomena"
        ]
        
        definitions = []
        for _ in range(n_samples):
            subject = random.choice(subjects)
            prop = random.choice(properties)
            concept = random.choice(concepts)
            
            definition = f"{subject} {prop} {concept}"
            definitions.append(definition.capitalize() + ".")
        
        return definitions
    
    def generate_qa_pairs(self, n_samples: int = 200) -> List[Tuple[str, str]]:
        """
        Generate question-answer pairs.
        
        Args:
            n_samples: Number of QA pairs to generate
            
        Returns:
            List of (question, answer) tuples
        """
        qa_templates = [
            ("What is {concept}?", "{concept} is {description}"),
            ("How does {concept} work?", "{concept} works by {mechanism}"),
            ("Why is {concept} important?", "{concept} is important because {reason}"),
            ("Where is {concept} found?", "{concept} is found in {location}"),
            ("When does {concept} occur?", "{concept} occurs when {condition}"),
        ]
        
        concepts = [
            "quantum entanglement", "gravitational waves", "spectral resonance",
            "coherent states", "phase transitions", "energy quantization",
            "wave interference", "harmonic oscillation", "frequency modulation",
            "topological order", "symmetry breaking", "field coupling",
            "particle decay", "nuclear fusion", "photon emission",
            "electron tunneling", "quantum superposition", "uncertainty principle",
            "conservation of energy", "conservation of momentum"
        ]
        
        descriptions = [
            "a fundamental quantum phenomenon",
            "a manifestation of spacetime curvature",
            "a spectral property of matter",
            "a coherent quantum state",
            "a critical point in phase space",
            "a discrete energy level",
            "a wave superposition effect",
            "a periodic oscillation",
            "a frequency-dependent process"
        ]
        
        mechanisms = [
            "quantum mechanical interactions",
            "gravitational field dynamics",
            "resonant energy transfer",
            "coherent phase evolution",
            "symmetry transformations",
            "wave propagation",
            "particle exchange",
            "field oscillations"
        ]
        
        reasons = [
            "it governs fundamental interactions",
            "it explains observable phenomena",
            "it enables quantum technologies",
            "it reveals the structure of spacetime",
            "it connects different physical scales",
            "it preserves conservation laws",
            "it determines system behavior"
        ]
        
        locations = [
            "quantum systems",
            "gravitational fields",
            "atomic spectra",
            "cosmic structures",
            "particle accelerators",
            "condensed matter",
            "plasma environments"
        ]
        
        conditions = [
            "quantum states interact",
            "energy levels align",
            "symmetries are broken",
            "fields couple resonantly",
            "critical thresholds are reached",
            "phase coherence emerges"
        ]
        
        qa_pairs = []
        for _ in range(n_samples):
            q_template, a_template = random.choice(qa_templates)
            concept = random.choice(concepts)
            
            # Fill template based on question type
            if "What is" in q_template:
                answer = a_template.format(
                    concept=concept,
                    description=random.choice(descriptions)
                )
            elif "How does" in q_template:
                answer = a_template.format(
                    concept=concept,
                    mechanism=random.choice(mechanisms)
                )
            elif "Why is" in q_template:
                answer = a_template.format(
                    concept=concept,
                    reason=random.choice(reasons)
                )
            elif "Where is" in q_template:
                answer = a_template.format(
                    concept=concept,
                    location=random.choice(locations)
                )
            else:  # When does
                answer = a_template.format(
                    concept=concept,
                    condition=random.choice(conditions)
                )
            
            question = q_template.format(concept=concept)
            qa_pairs.append((question, answer))
        
        return qa_pairs
    
    def generate_semantic_clusters(self, n_clusters: int = 5, samples_per_cluster: int = 40) -> Dict[str, List[str]]:
        """
        Generate semantically clustered sentences.
        
        Useful for evaluating clustering coherence.
        
        Args:
            n_clusters: Number of semantic clusters
            samples_per_cluster: Samples per cluster
            
        Returns:
            Dictionary mapping cluster names to sentences
        """
        cluster_themes = {
            "quantum_mechanics": {
                "terms": ["quantum", "wave", "particle", "superposition", "entanglement", 
                         "uncertainty", "measurement", "state", "operator", "observable"],
                "verbs": ["exhibits", "demonstrates", "displays", "manifests", "shows"],
                "properties": ["discrete energy levels", "wave-particle duality", 
                              "quantum coherence", "probabilistic behavior", "quantum tunneling"]
            },
            "relativity": {
                "terms": ["spacetime", "gravity", "curvature", "metric", "geodesic",
                         "light", "mass", "energy", "momentum", "velocity"],
                "verbs": ["curves", "warps", "bends", "distorts", "affects"],
                "properties": ["time dilation", "length contraction", "gravitational lensing",
                              "event horizons", "relativistic effects"]
            },
            "thermodynamics": {
                "terms": ["entropy", "temperature", "heat", "energy", "system",
                         "equilibrium", "process", "state", "function", "law"],
                "verbs": ["increases", "decreases", "conserves", "transforms", "exchanges"],
                "properties": ["thermal equilibrium", "energy conservation", "entropy maximization",
                              "reversible processes", "irreversible changes"]
            },
            "electromagnetism": {
                "terms": ["electric", "magnetic", "field", "charge", "current",
                         "force", "wave", "photon", "radiation", "dipole"],
                "verbs": ["generates", "induces", "creates", "propagates", "radiates"],
                "properties": ["electromagnetic waves", "field coupling", "charge conservation",
                              "wave propagation", "electromagnetic induction"]
            },
            "cosmology": {
                "terms": ["universe", "galaxy", "star", "cosmic", "expansion",
                         "dark matter", "dark energy", "redshift", "background", "structure"],
                "verbs": ["expands", "evolves", "forms", "clusters", "radiates"],
                "properties": ["cosmic expansion", "structure formation", "primordial fluctuations",
                              "large-scale structure", "cosmological evolution"]
            }
        }
        
        clusters = {}
        
        # Select n_clusters from available themes
        selected_themes = random.sample(list(cluster_themes.keys()), min(n_clusters, len(cluster_themes)))
        
        for theme_name in selected_themes:
            theme = cluster_themes[theme_name]
            sentences = []
            
            for _ in range(samples_per_cluster):
                term = random.choice(theme["terms"])
                verb = random.choice(theme["verbs"])
                prop = random.choice(theme["properties"])
                
                # Generate sentence
                templates = [
                    f"The {term} {verb} {prop}",
                    f"{term.capitalize()} {verb} {prop}",
                    f"Studies show that {term} {verb} {prop}",
                    f"Observations indicate {term} {verb} {prop}",
                    f"Research confirms {term} {verb} {prop}"
                ]
                
                sentence = random.choice(templates) + "."
                sentences.append(sentence)
            
            clusters[theme_name] = sentences
        
        return clusters
    
    def generate_full_dataset(self, n_total: int = 500) -> List[str]:
        """
        Generate complete dataset with mixed content.
        
        Args:
            n_total: Total number of samples
            
        Returns:
            List of all sentences
        """
        all_sentences = []
        
        # Definitions (40%)
        n_defs = int(n_total * 0.4)
        all_sentences.extend(self.generate_definitions(n_defs))
        
        # QA pairs (30% as pairs = 15% questions + 15% answers = 30% total samples)
        n_qa_pairs = int(n_total * 0.15)
        qa_pairs = self.generate_qa_pairs(n_qa_pairs)
        for q, a in qa_pairs:
            all_sentences.append(q)
            all_sentences.append(a)
        
        # Clustered content (remaining ~30%)
        n_remaining = n_total - len(all_sentences)
        if n_remaining > 0:
            samples_per_cluster = max(n_remaining // 5, 1)
            clusters = self.generate_semantic_clusters(
                n_clusters=5,
                samples_per_cluster=samples_per_cluster
            )
            for sentences in clusters.values():
                all_sentences.extend(sentences)
        
        # Shuffle to mix content types
        random.shuffle(all_sentences)
        
        return all_sentences[:n_total]
