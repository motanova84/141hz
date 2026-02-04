#!/usr/bin/env python3
"""
CAPA 3: Computational Architecture (Arquitectura Computacional)

This module implements the computational architecture layer:
- Hardware that operates at 141.7 Hz natively
- Coherent (non-binary) registers
- Phase-based memory
- Resonance processing

This layer provides the computational substrate for implementing
quantum coherence algorithms.
"""

import numpy as np
import mpmath as mp
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Default precision (use locally in methods if needed)
DEFAULT_PRECISION = 50


class RegisterState(Enum):
    """States of a coherent register (non-binary)."""
    SUPERPOSITION = "superposition"
    COHERENT = "coherent"
    DECOHERENT = "decoherent"
    RESONANT = "resonant"


@dataclass
class PhaseMemoryCell:
    """Represents a phase-based memory cell."""
    phase: float       # Phase in radians [0, 2π]
    amplitude: float   # Amplitude [0, 1]
    coherence: float   # Coherence level [0, 1]
    frequency: float   # Resonant frequency (Hz)


@dataclass
class ResonanceOperation:
    """Represents a resonance-based computation."""
    input_phase: float
    output_phase: float
    frequency: float
    duration: float  # Operation time in seconds


class NativeFrequencyHardware:
    """
    Hardware abstraction that operates at 141.7 Hz natively.
    
    Instead of GHz clock speeds with binary logic, this architecture
    uses 141.7 Hz resonance as the fundamental clock with coherent
    phase-based operations.
    """
    
    def __init__(self, f0: float = 141.7001):
        """
        Initialize native frequency hardware.
        
        Args:
            f0: Operating frequency in Hz
        """
        self.f0 = f0
        self.clock_period = 1.0 / f0  # ~7.06 ms
        self.phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
        # Hardware state
        self.cycle_count = 0
        self.phase_state = 0.0
        
    def tick(self) -> float:
        """
        Execute one clock cycle at f₀.
        
        Returns:
            Current phase after tick
        """
        self.cycle_count += 1
        
        # Phase advances by 2π per cycle
        self.phase_state = (self.phase_state + 2 * np.pi) % (2 * np.pi)
        
        return self.phase_state
    
    def reset(self):
        """Reset hardware to initial state."""
        self.cycle_count = 0
        self.phase_state = 0.0
    
    def get_time(self) -> float:
        """
        Get current time based on cycle count.
        
        Returns:
            Time in seconds
        """
        return self.cycle_count * self.clock_period
    
    def synchronize(self, other: 'NativeFrequencyHardware') -> float:
        """
        Synchronize with another hardware unit.
        
        Args:
            other: Another hardware instance
            
        Returns:
            Phase difference
        """
        phase_diff = abs(self.phase_state - other.phase_state)
        
        # Normalize to [0, π]
        if phase_diff > np.pi:
            phase_diff = 2 * np.pi - phase_diff
        
        return phase_diff
    
    def is_synchronized(self, other: 'NativeFrequencyHardware', tolerance: float = 0.1) -> bool:
        """
        Check if synchronized with another unit.
        
        Args:
            other: Another hardware instance
            tolerance: Phase tolerance in radians
            
        Returns:
            True if synchronized within tolerance
        """
        phase_diff = self.synchronize(other)
        return phase_diff < tolerance
    
    def resonance_quality(self) -> float:
        """
        Compute quality factor of resonance.
        
        Q = f₀ / Δf where Δf is bandwidth
        
        Returns:
            Quality factor (dimensionless)
        """
        # Assume natural bandwidth related to golden ratio
        delta_f = self.f0 / self.phi**2
        Q = self.f0 / delta_f
        
        return Q
    
    def power_consumption(self) -> float:
        """
        Estimate power consumption (arbitrary units).
        
        Lower frequency → lower power.
        
        Returns:
            Power in arbitrary units
        """
        # Power scales with frequency squared (CV²f)
        # Normalized to 1 GHz = 1 unit
        f_ghz = 1e9
        power = (self.f0 / f_ghz)**2
        
        return power


class CoherentRegisters:
    """
    Coherent (non-binary) register system.
    
    Instead of 0/1 bits, these registers store complex-valued
    coherent states characterized by amplitude and phase.
    """
    
    def __init__(self, num_registers: int = 8):
        """
        Initialize coherent register bank.
        
        Args:
            num_registers: Number of registers
        """
        self.num_registers = num_registers
        self.phi = (1 + np.sqrt(5)) / 2
        
        # Registers as complex numbers (amplitude × e^{iθ})
        self.registers = np.zeros(num_registers, dtype=complex)
        self.states = [RegisterState.COHERENT] * num_registers
        
    def write(self, idx: int, amplitude: float, phase: float):
        """
        Write to a coherent register.
        
        Args:
            idx: Register index
            amplitude: Amplitude [0, 1]
            phase: Phase in radians [0, 2π]
        """
        if 0 <= idx < self.num_registers:
            self.registers[idx] = amplitude * np.exp(1j * phase)
            self.states[idx] = RegisterState.COHERENT
    
    def read(self, idx: int) -> Tuple[float, float]:
        """
        Read from a coherent register.
        
        Args:
            idx: Register index
            
        Returns:
            Tuple of (amplitude, phase)
        """
        if 0 <= idx < self.num_registers:
            val = self.registers[idx]
            amplitude = abs(val)
            phase = np.angle(val)
            return amplitude, phase
        else:
            return 0.0, 0.0
    
    def superpose(self, idx1: int, idx2: int, idx_out: int):
        """
        Create superposition of two registers.
        
        |ψ_out⟩ = (|ψ_1⟩ + |ψ_2⟩) / √2
        
        Args:
            idx1: First input register
            idx2: Second input register
            idx_out: Output register
        """
        if all(0 <= i < self.num_registers for i in [idx1, idx2, idx_out]):
            self.registers[idx_out] = (self.registers[idx1] + self.registers[idx2]) / np.sqrt(2)
            self.states[idx_out] = RegisterState.SUPERPOSITION
    
    def interfere(self, idx1: int, idx2: int, idx_out: int):
        """
        Compute interference between two registers.
        
        Args:
            idx1: First input register
            idx2: Second input register
            idx_out: Output register
        """
        if all(0 <= i < self.num_registers for i in [idx1, idx2, idx_out]):
            # Interference: ψ_out = ψ_1 × ψ_2*
            self.registers[idx_out] = self.registers[idx1] * np.conj(self.registers[idx2])
            self.states[idx_out] = RegisterState.COHERENT
    
    def rotate_phase(self, idx: int, angle: float):
        """
        Rotate phase of a register.
        
        Args:
            idx: Register index
            angle: Rotation angle in radians
        """
        if 0 <= idx < self.num_registers:
            self.registers[idx] *= np.exp(1j * angle)
    
    def apply_golden_gate(self, idx: int):
        """
        Apply golden ratio gate: multiply amplitude by φ, rotate by φ.
        
        This is a fundamental operation in QCAL architecture.
        
        Args:
            idx: Register index
        """
        if 0 <= idx < self.num_registers:
            amplitude, phase = self.read(idx)
            new_amplitude = amplitude * self.phi
            new_phase = phase + self.phi
            
            # Normalize amplitude
            new_amplitude = new_amplitude % 1.0
            new_phase = new_phase % (2 * np.pi)
            
            self.write(idx, new_amplitude, new_phase)
            self.states[idx] = RegisterState.RESONANT
    
    def measure_coherence(self, idx1: int, idx2: int) -> float:
        """
        Measure coherence between two registers.
        
        Args:
            idx1: First register
            idx2: Second register
            
        Returns:
            Coherence value [0, 1]
        """
        if all(0 <= i < self.num_registers for i in [idx1, idx2]):
            # Coherence: |⟨ψ_1|ψ_2⟩|²
            inner_product = np.vdot(self.registers[idx1], self.registers[idx2])
            coherence = abs(inner_product)**2
            
            # Normalize by amplitudes
            norm1 = abs(self.registers[idx1])**2
            norm2 = abs(self.registers[idx2])**2
            
            if norm1 > 0 and norm2 > 0:
                coherence /= (norm1 * norm2)
            
            return coherence
        else:
            return 0.0
    
    def get_state_vector(self) -> np.ndarray:
        """
        Get complete state vector of all registers.
        
        Returns:
            Complex array of register values
        """
        return self.registers.copy()


class PhaseMemory:
    """
    Phase-based memory system.
    
    Memory cells store information in phase relationships rather
    than voltage levels. Reading/writing preserves phase coherence.
    """
    
    def __init__(self, capacity: int = 256):
        """
        Initialize phase memory.
        
        Args:
            capacity: Number of memory cells
        """
        self.capacity = capacity
        self.f0 = 141.7001
        self.phi = (1 + np.sqrt(5)) / 2
        
        # Memory as array of phase cells
        self.cells = [
            PhaseMemoryCell(phase=0.0, amplitude=0.0, coherence=1.0, frequency=self.f0)
            for _ in range(capacity)
        ]
    
    def write_phase(self, address: int, phase: float, amplitude: float = 1.0):
        """
        Write phase to memory address.
        
        Args:
            address: Memory address
            phase: Phase value in radians
            amplitude: Amplitude (optional)
        """
        if 0 <= address < self.capacity:
            self.cells[address].phase = phase % (2 * np.pi)
            self.cells[address].amplitude = min(max(amplitude, 0.0), 1.0)
            self.cells[address].coherence = 1.0  # Reset coherence on write
    
    def read_phase(self, address: int) -> float:
        """
        Read phase from memory address.
        
        Args:
            address: Memory address
            
        Returns:
            Phase in radians
        """
        if 0 <= address < self.capacity:
            # Decoherence on read (quantum measurement)
            cell = self.cells[address]
            cell.coherence *= 0.99  # Small decoherence per read
            return cell.phase
        else:
            return 0.0
    
    def read_cell(self, address: int) -> Optional[PhaseMemoryCell]:
        """
        Read entire memory cell.
        
        Args:
            address: Memory address
            
        Returns:
            PhaseMemoryCell or None
        """
        if 0 <= address < self.capacity:
            return self.cells[address]
        else:
            return None
    
    def encode_byte(self, address: int, byte_value: int):
        """
        Encode a byte (0-255) as phase pattern.
        
        Args:
            address: Starting address
            byte_value: Byte to encode (0-255)
        """
        if 0 <= address < self.capacity and 0 <= byte_value <= 255:
            # Encode byte as phase: 0-255 → 0-2π
            phase = (byte_value / 255.0) * 2 * np.pi
            self.write_phase(address, phase)
    
    def decode_byte(self, address: int) -> int:
        """
        Decode phase pattern to byte.
        
        Args:
            address: Memory address
            
        Returns:
            Byte value (0-255)
        """
        phase = self.read_phase(address)
        # Phase 0-2π → 0-255
        byte_value = int((phase / (2 * np.pi)) * 255)
        return byte_value
    
    def coherent_read(self, start_addr: int, length: int) -> np.ndarray:
        """
        Read multiple cells coherently (parallel).
        
        Args:
            start_addr: Starting address
            length: Number of cells to read
            
        Returns:
            Complex array of coherent amplitudes
        """
        coherent_data = np.zeros(length, dtype=complex)
        
        for i in range(length):
            addr = start_addr + i
            if addr < self.capacity:
                cell = self.cells[addr]
                coherent_data[i] = cell.amplitude * np.exp(1j * cell.phase)
        
        return coherent_data
    
    def refresh_coherence(self):
        """Refresh coherence of all cells (like DRAM refresh)."""
        for cell in self.cells:
            # Restore coherence if amplitude is significant
            if cell.amplitude > 0.1:
                cell.coherence = min(cell.coherence * 1.1, 1.0)


class ResonanceProcessor:
    """
    Processor that executes operations via resonance.
    
    Instead of logic gates, operations are performed through
    resonant coupling and interference at f₀.
    """
    
    def __init__(self):
        """Initialize resonance processor."""
        self.f0 = 141.7001
        self.phi = (1 + np.sqrt(5)) / 2
        self.registers = CoherentRegisters(num_registers=16)
        self.memory = PhaseMemory(capacity=1024)
        
        # Operation history
        self.operations: List[ResonanceOperation] = []
    
    def load_from_memory(self, mem_addr: int, reg_idx: int):
        """
        Load from memory to register.
        
        Args:
            mem_addr: Memory address
            reg_idx: Register index
        """
        cell = self.memory.read_cell(mem_addr)
        if cell:
            self.registers.write(reg_idx, cell.amplitude, cell.phase)
    
    def store_to_memory(self, reg_idx: int, mem_addr: int):
        """
        Store register to memory.
        
        Args:
            reg_idx: Register index
            mem_addr: Memory address
        """
        amplitude, phase = self.registers.read(reg_idx)
        self.memory.write_phase(mem_addr, phase, amplitude)
    
    def resonance_add(self, reg1: int, reg2: int, reg_out: int):
        """
        Add two registers via resonance.
        
        The sum is performed in phase space:
        φ_out = φ_1 + φ_2 (mod 2π)
        
        Args:
            reg1: First input register
            reg2: Second input register
            reg_out: Output register
        """
        amp1, phase1 = self.registers.read(reg1)
        amp2, phase2 = self.registers.read(reg2)
        
        # Phase addition
        phase_out = (phase1 + phase2) % (2 * np.pi)
        
        # Amplitude: geometric mean
        amp_out = np.sqrt(amp1 * amp2)
        
        self.registers.write(reg_out, amp_out, phase_out)
        
        # Log operation
        self.operations.append(ResonanceOperation(
            input_phase=phase1,
            output_phase=phase_out,
            frequency=self.f0,
            duration=1.0 / self.f0
        ))
    
    def resonance_multiply(self, reg1: int, reg2: int, reg_out: int):
        """
        Multiply registers via resonance.
        
        Args:
            reg1: First input register
            reg2: Second input register
            reg_out: Output register
        """
        # Complex multiplication in phase space
        self.registers.interfere(reg1, reg2, reg_out)
        
        amp_out, phase_out = self.registers.read(reg_out)
        
        self.operations.append(ResonanceOperation(
            input_phase=0.0,
            output_phase=phase_out,
            frequency=self.f0,
            duration=1.0 / self.f0
        ))
    
    def fourier_transform(self, input_regs: List[int], output_regs: List[int]):
        """
        Perform discrete Fourier transform via resonance.
        
        This is native to the phase-based architecture.
        
        Args:
            input_regs: List of input register indices
            output_regs: List of output register indices
        """
        N = len(input_regs)
        
        if len(output_regs) != N:
            return
        
        # Get input state vector
        input_state = np.array([self.registers.registers[i] for i in input_regs])
        
        # Apply DFT
        output_state = np.fft.fft(input_state) / np.sqrt(N)
        
        # Write to output registers
        for i, reg_idx in enumerate(output_regs):
            amp = abs(output_state[i])
            phase = np.angle(output_state[i])
            self.registers.write(reg_idx, amp, phase)
    
    def execute_picode(self, code: np.ndarray, input_reg: int, output_reg: int):
        """
        Execute a πCODE program.
        
        Args:
            code: πCODE instruction array
            input_reg: Input register
            output_reg: Output register
        """
        # Load input
        amp_in, phase_in = self.registers.read(input_reg)
        
        # Apply πCODE transformation
        # Each element of code rotates phase
        phase_out = phase_in
        amp_out = amp_in
        
        for coeff in code:
            if abs(coeff) > 0:
                rotation = np.angle(coeff)
                phase_out += rotation
                amp_out *= abs(coeff)
        
        # Normalize
        phase_out = phase_out % (2 * np.pi)
        amp_out = min(amp_out, 1.0)
        
        self.registers.write(output_reg, amp_out, phase_out)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get processor statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            'total_operations': len(self.operations),
            'average_frequency': np.mean([op.frequency for op in self.operations]) if self.operations else 0.0,
            'memory_usage': sum(1 for cell in self.memory.cells if cell.amplitude > 0),
            'active_registers': sum(1 for reg in self.registers.registers if abs(reg) > 0),
        }


def validate_computational_architecture() -> Dict[str, bool]:
    """
    Validate all computational architecture components.
    
    Returns:
        Dictionary of validation results
    """
    results = {}
    
    # Test native frequency hardware
    try:
        hw1 = NativeFrequencyHardware()
        hw2 = NativeFrequencyHardware()
        
        for _ in range(10):
            hw1.tick()
            hw2.tick()
        
        synced = hw1.is_synchronized(hw2, tolerance=0.01)
        results['native_hardware'] = synced
    except Exception as e:
        results['native_hardware'] = False
    
    # Test coherent registers
    try:
        regs = CoherentRegisters(num_registers=4)
        regs.write(0, 1.0, 0.0)
        regs.write(1, 1.0, np.pi/2)
        regs.superpose(0, 1, 2)
        
        amp, phase = regs.read(2)
        results['coherent_registers'] = amp > 0
    except Exception as e:
        results['coherent_registers'] = False
    
    # Test phase memory
    try:
        mem = PhaseMemory(capacity=100)
        mem.encode_byte(0, 42)
        decoded = mem.decode_byte(0)
        results['phase_memory'] = abs(decoded - 42) <= 1  # Allow rounding error
    except Exception as e:
        results['phase_memory'] = False
    
    # Test resonance processor
    try:
        proc = ResonanceProcessor()
        proc.registers.write(0, 1.0, 0.0)
        proc.registers.write(1, 1.0, np.pi/4)
        proc.resonance_add(0, 1, 2)
        
        amp, phase = proc.registers.read(2)
        results['resonance_processor'] = amp > 0 and phase > 0
    except Exception as e:
        results['resonance_processor'] = False
    
    return results


if __name__ == "__main__":
    # Demonstration
    print("=" * 70)
    print("CAPA 3: Computational Architecture Demonstration")
    print("=" * 70)
    
    # 1. Native Frequency Hardware
    print("\n1. Native Frequency Hardware (141.7 Hz)")
    print("-" * 70)
    hw = NativeFrequencyHardware()
    print(f"Operating frequency: {hw.f0} Hz")
    print(f"Clock period: {hw.clock_period * 1000:.2f} ms")
    print(f"Quality factor Q: {hw.resonance_quality():.2f}")
    print(f"Power consumption (relative to 1 GHz): {hw.power_consumption():.2e}")
    
    # Run for 10 cycles
    for i in range(10):
        phase = hw.tick()
        if i < 3 or i >= 7:
            print(f"Cycle {hw.cycle_count}: phase = {phase:.3f} rad, time = {hw.get_time()*1000:.2f} ms")
    
    # 2. Coherent Registers
    print("\n2. Coherent (Non-Binary) Registers")
    print("-" * 70)
    regs = CoherentRegisters(num_registers=8)
    
    # Write some values
    regs.write(0, 1.0, 0.0)  # |1⟩
    regs.write(1, 1.0, np.pi)  # |-1⟩
    
    # Create superposition
    regs.superpose(0, 1, 2)
    amp, phase = regs.read(2)
    print(f"Superposition |ψ⟩ = (|0⟩ + |1⟩)/√2:")
    print(f"  Amplitude: {amp:.3f}")
    print(f"  Phase: {phase:.3f} rad")
    
    # Apply golden gate
    regs.apply_golden_gate(2)
    amp_new, phase_new = regs.read(2)
    print(f"After golden gate:")
    print(f"  Amplitude: {amp_new:.3f}")
    print(f"  Phase: {phase_new:.3f} rad")
    
    # Measure coherence
    coherence = regs.measure_coherence(0, 1)
    print(f"Coherence between reg[0] and reg[1]: {coherence:.3f}")
    
    # 3. Phase Memory
    print("\n3. Phase-Based Memory")
    print("-" * 70)
    mem = PhaseMemory(capacity=256)
    
    # Encode some bytes
    test_data = [0, 42, 127, 255]
    for i, byte_val in enumerate(test_data):
        mem.encode_byte(i, byte_val)
        decoded = mem.decode_byte(i)
        print(f"Encoded {byte_val:3d} → Phase → Decoded {decoded:3d}")
    
    # Coherent read
    coherent_block = mem.coherent_read(0, 4)
    print(f"\nCoherent read of 4 cells:")
    for i, val in enumerate(coherent_block):
        print(f"  Cell {i}: {val}")
    
    # 4. Resonance Processor
    print("\n4. Resonance Processing")
    print("-" * 70)
    proc = ResonanceProcessor()
    
    # Load registers
    proc.registers.write(0, 1.0, np.pi/6)
    proc.registers.write(1, 1.0, np.pi/3)
    
    print("Input registers:")
    for i in range(2):
        amp, phase = proc.registers.read(i)
        print(f"  R{i}: amp={amp:.3f}, phase={phase:.3f} rad ({np.degrees(phase):.1f}°)")
    
    # Resonance addition
    proc.resonance_add(0, 1, 2)
    amp_sum, phase_sum = proc.registers.read(2)
    print(f"\nResonance addition R0 + R1 → R2:")
    print(f"  R2: amp={amp_sum:.3f}, phase={phase_sum:.3f} rad ({np.degrees(phase_sum):.1f}°)")
    
    # Statistics
    stats = proc.get_statistics()
    print(f"\nProcessor statistics:")
    print(f"  Total operations: {stats['total_operations']}")
    print(f"  Active registers: {stats['active_registers']}")
    
    # Validation
    print("\n" + "=" * 70)
    print("Validation Results")
    print("=" * 70)
    validation = validate_computational_architecture()
    for component, passed in validation.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{component:30s}: {status}")
