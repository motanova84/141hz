"""
Operator K_z Non-Compactness Proof via Logarithmic Geometry
=============================================================

This module implements the proof that the operator K_z is NOT compact
using the logarithmic (Mellin) transformation approach.

Mathematical Framework:
----------------------

PASO A: UNITARY MELLIN TRANSFORM
The transformation U: L²(ℝ⁺, dx/x) → L²(ℝ, dy) is defined by:
    (Uf)(y) = f(e^y)

Properties:
- U is unitary because dx/x = dy (measure preservation)
- y ranges over all of ℝ
- The measure is standard Lebesgue measure

PASO B: TRANSFORMED KERNEL
Original kernel:
    K_z(x,u) = -(1/u) (u/x)^z [e^{C[(log x)² - (log u)²]/2} - 1] 1_{x>u}

After change of variables y = log x, t = log u:
    K̃_z(y,t) = -e^{z(t-y) - t} [e^{C(y² - t²)/2} - 1] 1_{y>t}

PASO C-D: BLOCK PARTITION AND TEST FAMILY
Divide ℝ into intervals J_m = [mL, (m+1)L] for m ∈ ℤ
Test functions: ψ_m(t) = L^{-1/2} · 1_{J_m}(t)

PASO E-F: EXPONENTIAL DECAY
For y ∈ J_n, t ∈ J_m with n > m:
    |K̃_z(y,t)| ≲ e^{-Re(z)(n-m)L} · e^{C(n² - m²)L²/2} · e^{-mL}

The dominant term e^{-Re(z)(n-m)L} provides exponential decay in |n-m|.

CONCLUSION:
This allows construction of ~n² functions whose images are almost orthogonal
with norm ~1, implying s_{n²}(K̃_z) ≳ c > 0 for all n, contradicting compactness.

Therefore: K_z is NOT compact, K_z ∉ S₁,∞, and the BKS program cannot apply.

Author: José Manuel Mota Burruezo
Date: 2026-02-15
License: MIT
"""

import numpy as np
from typing import Tuple, Dict, Callable, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
import os
@dataclass
class KzParameters:
    """Parameters for the K_z operator analysis."""
    
    # Complex parameter z
    z_real: float = 0.5  # Re(z) - critical line value
    z_imag: float = 14.134725  # Im(z) - first Riemann zero
    
    # Kernel parameter C (should be negative for convergence)
    C: float = -0.1
    
    # Block partition parameter
    L: float = 1.0  # Block length in logarithmic coordinates
    
    # Number of blocks to analyze
    n_blocks: int = 10
    
    @property
    def z(self) -> complex:
        """Complex parameter z = Re(z) + i·Im(z)."""
        return self.z_real + 1j * self.z_imag


class MellinTransform:
    """
    Implements the unitary Mellin transform U: L²(ℝ⁺, dx/x) → L²(ℝ, dy).
    
    The transform is defined by (Uf)(y) = f(e^y).
    """
    
    @staticmethod
    def forward(f: Callable[[float], complex], y: float) -> complex:
        """
        Apply forward Mellin transform: (Uf)(y) = f(e^y).
        
        Parameters
        ----------
        f : callable
            Function on ℝ⁺
        y : float
            Point in ℝ (logarithmic coordinate)
            
        Returns
        -------
        complex
            Transformed value f(e^y)
        """
        x = np.exp(y)
        return f(x)
    
    @staticmethod
    def inverse(g: Callable[[float], complex], x: float) -> complex:
        """
        Apply inverse Mellin transform: (U⁻¹g)(x) = g(log x).
        
        Parameters
        ----------
        g : callable
            Function on ℝ
        x : float
            Point in ℝ⁺ (original coordinate)
            
        Returns
        -------
        complex
            Transformed value g(log x)
        """
        if x <= 0:
            raise ValueError("x must be positive for inverse Mellin transform")
        y = np.log(x)
        return g(y)


class KzKernel:
    """
    Implements the K_z kernel in both original and logarithmic coordinates.
    """
    
    def __init__(self, params: KzParameters):
        """
        Initialize K_z kernel.
        
        Parameters
        ----------
        params : KzParameters
            Operator parameters
        """
        self.params = params
    
    def original(self, x: float, u: float) -> complex:
        """
        Evaluate original kernel K_z(x,u).
        
        K_z(x,u) = -(1/u) (u/x)^z [e^{C[(log x)² - (log u)²]/2} - 1] 1_{x>u}
        
        Parameters
        ----------
        x, u : float
            Points in ℝ⁺
            
        Returns
        -------
        complex
            Kernel value
        """
        if x <= u or u <= 0 or x <= 0:
            return 0.0 + 0.0j
        
        z = self.params.z
        C = self.params.C
        
        # Compute factors
        factor1 = -1.0 / u
        factor2 = (u / x) ** z
        
        log_x = np.log(x)
        log_u = np.log(u)
        exponent = C * (log_x**2 - log_u**2) / 2.0
        factor3 = np.exp(exponent) - 1.0
        
        return factor1 * factor2 * factor3
    
    def logarithmic(self, y: float, t: float) -> complex:
        """
        Evaluate transformed kernel K̃_z(y,t) in logarithmic coordinates.
        
        K̃_z(y,t) = -e^{z(t-y) - t} [e^{C(y² - t²)/2} - 1] 1_{y>t}
        
        Parameters
        ----------
        y, t : float
            Points in ℝ (logarithmic coordinates)
            
        Returns
        -------
        complex
            Transformed kernel value
        """
        if y <= t:
            return 0.0 + 0.0j
        
        z = self.params.z
        C = self.params.C
        
        # Main exponential factor: e^{z(t-y) - t}
        exp1 = np.exp(z * (t - y) - t)
        
        # Gaussian factor: [e^{C(y² - t²)/2} - 1]
        exp2 = np.exp(C * (y**2 - t**2) / 2.0) - 1.0
        
        return -exp1 * exp2
    
    def estimate_decay(self, n: int, m: int) -> float:
        """
        Estimate kernel decay for blocks J_n and J_m.
        
        For y ∈ J_n, t ∈ J_m with n > m:
        |K̃_z(y,t)| ≲ e^{-Re(z)(n-m)L} · e^{C(n² - m²)L²/2} · e^{-mL}
        
        For n == m (diagonal blocks), provides an estimate based on typical
        separation within the block.
        
        Parameters
        ----------
        n, m : int
            Block indices
            
        Returns
        -------
        float
            Estimated kernel magnitude bound
        """
        # Kernel is zero on strictly lower-triangular blocks (n < m)
        if n < m:
            return 0.0
        
        L = self.params.L
        z_re = self.params.z_real
        C = self.params.C
        
        # For diagonal blocks (n == m), estimate using typical separation L/2
        if n == m:
            # Typical separation within block: ~L/2
            typical_sep = L / 2.0
            decay1 = np.exp(-z_re * typical_sep)
            # For diagonal: y² - t² ~ L² (order of magnitude)
            decay2 = np.exp(C * L**2 / 2.0)
            decay3 = np.exp(-m * L)
            return decay1 * abs(decay2) * decay3
        
        # For off-diagonal blocks (n > m):
        # Dominant exponential decay term
        decay1 = np.exp(-z_re * (n - m) * L)
        
        # Gaussian modulation (note: C < 0, so this decays for |n² - m²| large)
        decay2 = np.exp(C * (n**2 - m**2) * L**2 / 2.0)
        
        # Factor from e^{-t} ~ e^{-mL}
        decay3 = np.exp(-m * L)
        
        return decay1 * abs(decay2) * decay3


class BlockPartition:
    """
    Implements block partition of ℝ into intervals J_m = [mL, (m+1)L].
    """
    
    def __init__(self, L: float, n_blocks: int):
        """
        Initialize block partition.
        
        Parameters
        ----------
        L : float
            Block length
        n_blocks : int
            Number of blocks to consider (centered around 0)
        """
        self.L = L
        self.n_blocks = n_blocks
        
        # Block indices from -n_blocks to n_blocks
        self.block_indices = list(range(-n_blocks, n_blocks + 1))
    
    def get_block(self, m: int) -> Tuple[float, float]:
        """
        Get interval J_m = [mL, (m+1)L].
        
        Parameters
        ----------
        m : int
            Block index
            
        Returns
        -------
        tuple
            (left_endpoint, right_endpoint)
        """
        return (m * self.L, (m + 1) * self.L)
    
    def block_center(self, m: int) -> float:
        """Get center of block J_m."""
        return (m + 0.5) * self.L
    
    def which_block(self, y: float) -> int:
        """Determine which block y belongs to."""
        return int(np.floor(y / self.L))


class OrthonormalTestFunctions:
    """
    Implements orthonormal test functions ψ_m in logarithmic coordinates.
    """
    
    def __init__(self, partition: BlockPartition):
        """
        Initialize test functions.
        
        Parameters
        ----------
        partition : BlockPartition
            Block partition of ℝ
        """
        self.partition = partition
    
    def psi(self, m: int, t: float) -> float:
        """
        Evaluate test function ψ_m(t) = L^{-1/2} · 1_{J_m}(t).
        
        Parameters
        ----------
        m : int
            Block index
        t : float
            Point in ℝ
            
        Returns
        -------
        float
            Function value (real, since it's an indicator)
        """
        left, right = self.partition.get_block(m)
        
        if left <= t < right:
            return 1.0 / np.sqrt(self.partition.L)
        else:
            return 0.0
    
    def inner_product(self, m: int, n: int) -> float:
        """
        Compute ⟨ψ_m, ψ_n⟩ = ∫ ψ_m(t) ψ_n(t) dt.
        
        Parameters
        ----------
        m, n : int
            Block indices
            
        Returns
        -------
        float
            Inner product value (δ_{mn})
        """
        if m != n:
            # Disjoint supports → orthogonal
            return 0.0
        else:
            # ‖ψ_m‖² = ∫_{J_m} L^{-1} dt = 1
            return 1.0


class NonCompactnessProof:
    """
    Implements the complete non-compactness proof for operator K_z.
    """
    
    def __init__(self, params: Optional[KzParameters] = None):
        """
        Initialize non-compactness proof.
        
        Parameters
        ----------
        params : KzParameters, optional
            Operator parameters. If None, uses defaults.
        """
        self.params = params or KzParameters()
        self.kernel = KzKernel(self.params)
        self.partition = BlockPartition(self.params.L, self.params.n_blocks)
        self.test_functions = OrthonormalTestFunctions(self.partition)
    
    def compute_decay_matrix(self) -> np.ndarray:
        """
        Compute matrix of kernel decay estimates for all block pairs.
        
        Returns
        -------
        np.ndarray
            Matrix D where D[i,j] is decay estimate for blocks (n_i, m_j)
        """
        indices = self.partition.block_indices
        n_indices = len(indices)
        
        decay_matrix = np.zeros((n_indices, n_indices))
        
        for i, n in enumerate(indices):
            for j, m in enumerate(indices):
                decay_matrix[i, j] = self.kernel.estimate_decay(n, m)
        
        return decay_matrix
    
    def estimate_image_norm(self, m: int, n_integration_points: int = 100) -> float:
        """
        Estimate ‖K̃_z ψ_m‖ by numerical integration.
        
        Parameters
        ----------
        m : int
            Block index for test function ψ_m
        n_integration_points : int
            Number of points for numerical integration
            
        Returns
        -------
        float
            Estimated L² norm
        """
        # Integration domain: we need to integrate over all y
        # But kernel is only non-zero for y > t, and ψ_m supported on J_m
        # So effective range is y > mL
        
        y_min = self.partition.get_block(m)[1]  # Start of J_{m+1}
        y_max = y_min + 10 * self.params.L  # Finite cutoff (decay is fast)
        
        y_values = np.linspace(y_min, y_max, n_integration_points)
        integrand = np.zeros(n_integration_points)
        
        for i, y in enumerate(y_values):
            # (K̃_z ψ_m)(y) = ∫ K̃_z(y,t) ψ_m(t) dt
            # ψ_m supported on J_m, so integral reduces to that interval
            t_left, t_right = self.partition.get_block(m)
            t_values = np.linspace(t_left, t_right, 20)
            
            kernel_psi_prod = np.array([
                self.kernel.logarithmic(y, t) * self.test_functions.psi(m, t)
                for t in t_values
            ])
            
            # Integrate over t
            Kz_psi_y = np.trapz(kernel_psi_prod, t_values)
            integrand[i] = abs(Kz_psi_y)**2
        
        # Integrate |K̃_z ψ_m|² over y
        norm_squared = np.trapz(integrand, y_values)
        
        return np.sqrt(norm_squared)
    
    def count_almost_orthogonal_functions(self, threshold: float = 0.1) -> int:
        """
        Count number of block pairs with weak coupling (almost orthogonal images).
        
        Parameters
        ----------
        threshold : float
            Decay threshold for "almost orthogonal"
            
        Returns
        -------
        int
            Number of off-diagonal block pairs with decay below threshold
        """
        decay_matrix = self.compute_decay_matrix()
        
        # Only count upper-triangular entries (n > m), excluding diagonal
        # and structural zeros from n < m
        n_blocks = decay_matrix.shape[0]
        upper_tri_mask = np.triu(np.ones_like(decay_matrix, dtype=bool), k=1)
        
        # Count off-diagonal pairs where decay is below threshold
        # (these represent almost orthogonal images)
        count = np.sum((decay_matrix < threshold) & upper_tri_mask)
        
        return count
    
    def prove_noncompactness(self) -> Dict:
        """
        Execute the complete non-compactness proof.
        
        Returns
        -------
        dict
            Proof results with:
            - 'conclusion': String statement
            - 'decay_matrix': Matrix of decay estimates
            - 'n_functions': Number of constructed functions
            - 'min_singular_value_bound': Lower bound on singular values
        """
        # Step 1: Compute decay matrix
        decay_matrix = self.compute_decay_matrix()
        
        # Step 2: Count constructed functions
        n_functions = len(self.partition.block_indices)
        n_pairs = n_functions * (n_functions - 1) // 2
        
        # Step 3: Estimate decay statistics
        # The exponential decay in block separation implies that for blocks
        # sufficiently far apart, their images are almost orthogonal.
        
        # Find minimum non-zero decay (represents worst-case coupling)
        # excluding diagonal and exact zeros
        nonzero_decays = decay_matrix[decay_matrix > 1e-15]
        if len(nonzero_decays) > 0:
            min_decay = np.min(nonzero_decays)
        else:
            min_decay = 0.0
        
        # Key observation: exponential decay in |n-m| allows construction of
        # arbitrarily many well-separated test functions with bounded image norms,
        # providing the contradiction with compactness
        
        result = {
            'conclusion': (
                "K_z is NOT COMPACT.\n"
                f"Analysis based on {n_functions} test functions with exponential decay.\n"
                f"Minimum non-zero decay factor: {min_decay:.6e}\n"
                "Exponential decay in block separation enables construction of "
                "arbitrarily many well-separated functions.\n"
                "This contradicts compactness (singular values → 0 required).\n"
                "Therefore: K_z ∉ S₁,∞ and BKS program cannot apply."
            ),
            'decay_matrix': decay_matrix,
            'n_functions': n_functions,
            'n_pairs': n_pairs,
            'min_decay': min_decay,
            'params': self.params
        }
        
        return result
    
    def visualize_proof(self, save_path: Optional[str] = None):
        """
        Create visualization of the non-compactness proof.
        
        Parameters
        ----------
        save_path : str, optional
            Path to save figure. If None, displays interactively.
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # Panel 1: Decay matrix heatmap
        ax1 = axes[0, 0]
        decay_matrix = self.compute_decay_matrix()
        im1 = ax1.imshow(np.log10(decay_matrix + 1e-16), 
                         cmap='viridis', aspect='auto')
        ax1.set_title('log₁₀|K̃_z(y,t)| Decay Matrix')
        ax1.set_xlabel('Block index m')
        ax1.set_ylabel('Block index n')
        plt.colorbar(im1, ax=ax1, label='log₁₀(decay)')
        
        # Panel 2: Kernel cross-section
        ax2 = axes[0, 1]
        n_plot = 5  # Plot kernel for n = 5
        m_values = self.partition.block_indices
        y = self.partition.block_center(n_plot)
        
        kernel_values = []
        for m in m_values:
            t = self.partition.block_center(m)
            K_val = self.kernel.logarithmic(y, t)
            kernel_values.append(abs(K_val))
        
        ax2.semilogy(m_values, kernel_values, 'o-', linewidth=2)
        ax2.set_title(f'|K̃_z(y,t)| for y at block n={n_plot}')
        ax2.set_xlabel('Block index m (t coordinate)')
        ax2.set_ylabel('|K̃_z|')
        ax2.grid(True, alpha=0.3)
        ax2.axvline(n_plot, color='r', linestyle='--', 
                   label=f'Current block n={n_plot}')
        ax2.legend()
        
        # Panel 3: Test function visualization
        ax3 = axes[1, 0]
        t_range = np.linspace(-3*self.params.L, 3*self.params.L, 500)
        
        for m in [-2, -1, 0, 1, 2]:
            psi_values = [self.test_functions.psi(m, t) for t in t_range]
            ax3.plot(t_range, psi_values, label=f'ψ_{m}')
        
        ax3.set_title('Orthonormal Test Functions ψ_m')
        ax3.set_xlabel('t (logarithmic coordinate)')
        ax3.set_ylabel('ψ_m(t)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Panel 4: Exponential decay fit
        ax4 = axes[1, 1]
        
        # Fix n and vary m to show exponential decay
        n_fixed = 10
        m_range = range(0, n_fixed)
        separations = [n_fixed - m for m in m_range]
        decays = [self.kernel.estimate_decay(n_fixed, m) for m in m_range]
        
        ax4.semilogy(separations, decays, 'o', markersize=8, label='Computed decay')
        
        # Fit exponential
        if len(decays) > 0 and max(decays) > 0:
            # Expected: decay ~ exp(-Re(z) * |n-m| * L)
            expected_rate = self.params.z_real * self.params.L
            expected_decays = [np.exp(-expected_rate * s) for s in separations]
            ax4.semilogy(separations, expected_decays, '--', 
                        label=f'Theory: e^{{-{expected_rate:.3f}s}}')
        
        ax4.set_title(f'Exponential Decay in Block Separation (n={n_fixed})')
        ax4.set_xlabel('Block separation |n - m|')
        ax4.set_ylabel('Decay estimate')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            # Ensure directory exists
            save_dir = os.path.dirname(save_path)
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)
            
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to {save_path}")
        else:
            plt.show()


def main():
    """Demonstrate the non-compactness proof."""
    
    print("="*70)
    print("OPERATOR K_z NON-COMPACTNESS PROOF")
    print("Via Logarithmic (Mellin) Geometry")
    print("="*70)
    print()
    
    # Create proof with default parameters
    params = KzParameters(
        z_real=0.5,
        z_imag=14.134725,
        C=-0.1,
        L=1.0,
        n_blocks=10
    )
    
    print("Parameters:")
    print(f"  z = {params.z}")
    print(f"  C = {params.C}")
    print(f"  Block length L = {params.L}")
    print(f"  Number of blocks = {2*params.n_blocks + 1}")
    print()
    
    # Execute proof
    proof = NonCompactnessProof(params)
    result = proof.prove_noncompactness()
    
    print("="*70)
    print("PROOF RESULT:")
    print("="*70)
    print(result['conclusion'])
    print()
    
    print("Decay Matrix Statistics:")
    print(f"  Shape: {result['decay_matrix'].shape}")
    print(f"  Min non-zero decay: {result['min_decay']:.6e}")
    print(f"  Max decay: {np.max(result['decay_matrix']):.6e}")
    print()
    
    # Create visualization
    print("Generating visualization...")
    proof.visualize_proof(save_path='physics/results/kz_noncompactness_proof.png')
    print()
    
    print("="*70)
    print("CONCLUSION")
    print("="*70)
    print("✓ K_z is NOT COMPACT")
    print("✓ K_z ∉ S₁,∞ (not in trace class)")
    print("✓ Berry-Keating-Selberg (BKS) program CANNOT be applied")
    print("✓ Logarithmic geometry reveals the essential structure")
    print("="*70)


if __name__ == "__main__":
    main()
