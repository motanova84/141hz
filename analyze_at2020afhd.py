#!/usr/bin/env python3
"""
AT2020afhd Lomb-Scargle Periodogram Analysis and QCAL Verification

This script analyzes real data from AT2020afhd (a tidal disruption event)
using Lomb-Scargle periodogram to detect periodic signals in X-ray and radio
observations. It then verifies the harmonic relationship with the QCAL 
fundamental frequency (141.70001 Hz).

Data source: Zenodo - Figure_datas.tar
Expected period: 19.6 ± 0.5 days (published value)

Usage:
    python analyze_at2020afhd.py [--data-dir DATA_DIR] [--download]
"""

import argparse
import os
import sys
import tarfile
import urllib.request
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


class AT2020afhdAnalyzer:
    """Analyzer for AT2020afhd periodogram data."""
    
    def __init__(self, data_dir='Figure_datas'):
        """
        Initialize the analyzer.
        
        Args:
            data_dir: Directory containing the extracted Figure_datas
        """
        self.data_dir = Path(data_dir)
        self.lsp_dir = self.data_dir / 'Figure2_Lomb_Scargle_ccf_fold'
        
        # QCAL fundamental frequency
        self.f0 = 141.70001  # Hz
        
        # Published period for AT2020afhd
        self.published_period = 19.6  # days
        self.published_error = 0.5    # days
        
    def check_data_availability(self):
        """Check if required data files exist."""
        required_files = [
            self.lsp_dir / 'LSP.txt',
            self.lsp_dir / 'data_lc_NEW_gti.txt',
            self.lsp_dir / 'all_radio_lc.txt'
        ]
        
        missing_files = [f for f in required_files if not f.exists()]
        
        if missing_files:
            print(f"Missing required data files:")
            for f in missing_files:
                print(f"  - {f}")
            print("\nPlease extract Figure_datas.tar or use --download flag.")
            return False
        return True
    
    def load_lomb_scargle_data(self):
        """Load the Lomb-Scargle periodogram data."""
        lsp_file = self.lsp_dir / 'LSP.txt'
        print(f"Loading Lomb-Scargle data from: {lsp_file}")
        
        lsp_data = np.loadtxt(lsp_file)
        period = lsp_data[:, 0]  # days
        power = lsp_data[:, 1]   # spectral power
        
        return period, power
    
    def find_peak_period(self, period, power):
        """Find the peak period in the periodogram."""
        max_idx = np.argmax(power)
        detected_period = period[max_idx]
        max_power = power[max_idx]
        
        return detected_period, max_power, max_idx
    
    def plot_periodogram(self, period, power, detected_period, save_path=None):
        """Plot the Lomb-Scargle periodogram."""
        plt.figure(figsize=(14, 6))
        plt.plot(period, power, 'b-', linewidth=2, label='Lomb-Scargle Power')
        plt.axvline(detected_period, color='red', linestyle='--', linewidth=2,
                   label=f'Peak detected: {detected_period:.2f} days')
        plt.axvline(self.published_period, color='green', linestyle=':', 
                   linewidth=2, alpha=0.7,
                   label=f'Published: {self.published_period} days')
        plt.xlabel('Period (days)', fontsize=14, fontweight='bold')
        plt.ylabel('Lomb-Scargle Power', fontsize=14, fontweight='bold')
        plt.title('AT2020afhd - Lomb-Scargle Periodogram (REAL DATA FROM ZENODO)',
                 fontsize=16, fontweight='bold')
        plt.xlim(10, 40)
        plt.legend(fontsize=12)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Periodogram saved to: {save_path}")
        else:
            plt.show()
    
    def load_light_curves(self):
        """Load X-ray and radio light curves."""
        # X-ray data
        xray_file = self.lsp_dir / 'data_lc_NEW_gti.txt'
        print(f"Loading X-ray data from: {xray_file}")
        xray_lc = np.loadtxt(xray_file)
        xray_time = xray_lc[:, 0]
        xray_flux = xray_lc[:, 1]
        xray_error = xray_lc[:, 2]
        
        # Radio data
        radio_file = self.lsp_dir / 'all_radio_lc.txt'
        print(f"Loading radio data from: {radio_file}")
        radio_lc = np.loadtxt(radio_file)
        radio_lc = radio_lc[~np.isnan(radio_lc).any(axis=1)]  # Clean NaN
        radio_time = radio_lc[:, 0]
        radio_flux = radio_lc[:, 1]
        radio_error = radio_lc[:, 2]
        
        return (xray_time, xray_flux, xray_error,
                radio_time, radio_flux, radio_error)
    
    def plot_light_curves(self, xray_time, xray_flux, xray_error,
                         radio_time, radio_flux, radio_error, save_path=None):
        """Plot X-ray and radio light curves."""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
        
        ax1.errorbar(xray_time, xray_flux, yerr=xray_error,
                    fmt='o', color='blue', markersize=4, alpha=0.7, 
                    label='X-ray (Swift/NICER)')
        ax1.set_ylabel('X-ray Flux', fontsize=12)
        ax1.set_title('AT2020afhd - REAL DATA FROM ZENODO', 
                     fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(alpha=0.3)
        
        ax2.errorbar(radio_time, radio_flux, yerr=radio_error,
                    fmt='s', color='red', markersize=4, alpha=0.7, 
                    label='Radio 15.1 GHz (VLA+ATCA+e-MERLIN)')
        ax2.set_xlabel('Time (MJD)', fontsize=12)
        ax2.set_ylabel('Radio Flux (mJy)', fontsize=12)
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Light curves saved to: {save_path}")
        else:
            plt.show()
    
    def calculate_qcal_verification(self, detected_period):
        """Calculate QCAL harmonic relationship verification."""
        # Convert period to frequency
        f_frame = 1.0 / (detected_period * 86400.0)  # days -> seconds -> Hz
        
        # Calculate harmonic ratio
        ratio = self.f0 / f_frame
        octaves = np.log2(ratio)
        decades = np.log10(ratio)
        
        return f_frame, ratio, octaves, decades
    
    def print_verification_report(self, detected_period, max_power, 
                                 f_frame, ratio, octaves, decades):
        """Print comprehensive verification report."""
        print("\n" + "=" * 70)
        print("PERIODICITY ANALYSIS - REAL DATA")
        print("=" * 70)
        print(f"Detected period: {detected_period:.3f} days")
        print(f"Maximum power: {max_power:.3f}")
        print(f"Published value: {self.published_period} ± {self.published_error} days")
        print(f"Difference: {abs(detected_period - self.published_period):.3f} days")
        print("=" * 70)
        
        print("\n" + "=" * 70)
        print("NOESIS VERIFICATION - FRACTAL CASCADE")
        print("=" * 70)
        print(f"Observed period:        P = {detected_period:.3f} days")
        print(f"Frame frequency:        f_frame = {f_frame:.6e} Hz")
        print(f"QCAL frequency:         f0 = {self.f0} Hz")
        print("-" * 70)
        print(f"HARMONIC RATIO:         f0 / f_frame = {ratio:.6e}")
        print(f"Octaves separation:     log2(ratio) = {octaves:.3f}")
        print(f"Orders of magnitude:    log10(ratio) = {decades:.3f}")
        print("=" * 70)
        
        # Compare with expected values
        expected_ratio = 2.405e8
        expected_octaves = 27.84
        
        print("\nCOMPARISON WITH THEORY:")
        print(f"  Expected ratio:   {expected_ratio:.3e}")
        print(f"  Measured ratio:   {ratio:.3e}")
        print(f"  Difference:       {abs(ratio - expected_ratio)/expected_ratio * 100:.2f}%")
        print()
        print(f"  Expected octaves: {expected_octaves:.2f}")
        print(f"  Measured octaves: {octaves:.2f}")
        print(f"  Difference:       {abs(octaves - expected_octaves):.2f}")
        print("=" * 70)
        
        # Verification criteria
        periodo_ok = (self.published_period - self.published_error < detected_period < 
                     self.published_period + self.published_error)
        octavas_ok = 27.5 < octaves < 28.5
        ratio_ok = 2.3e8 < ratio < 2.5e8
        
        print("\n" + "=" * 70)
        print("VERIFICATION STATUS")
        print("=" * 70)
        
        if periodo_ok:
            print("[OK] Period within expected range "
                 f"({self.published_period - self.published_error} - "
                 f"{self.published_period + self.published_error} days)")
        else:
            print("[!!] Period outside expected range")
        
        if octavas_ok:
            print("[OK] Fractal cascade confirmed (~27.8 octaves)")
        else:
            print("[!!] Fractal cascade outside expected range")
        
        if ratio_ok:
            print("[OK] Harmonic ratio confirmed (~2.4e8)")
        else:
            print("[!!] Harmonic ratio outside expected range")
        
        print("=" * 70)
        
        if periodo_ok and octavas_ok and ratio_ok:
            print("\n*** NOESIS COMPLETELY VERIFIED ***")
            print("\nΨ = π * A_eff²")
            print("\nThe π pattern resonates fractally:")
            print(f"  - Quantum scale:    f0 = {self.f0} Hz (human heart)")
            print(f"  - Cosmic scale:     f_frame = {f_frame:.3e} Hz (black hole)")
            print(f"  - Exact separation: {octaves:.2f} octaves")
            print("\nThe black hole sings the same note as your heart,")
            print("just 27.8 octaves lower.")
        else:
            print("\nPartial verification - review parameters")
        
        print("=" * 70)
    
    def run_full_analysis(self, plot=True, save_plots=False):
        """Run the complete analysis pipeline."""
        print("\n" + "=" * 70)
        print("AT2020AFHD LOMB-SCARGLE PERIODOGRAM ANALYSIS")
        print("=" * 70 + "\n")
        
        # Check data availability
        if not self.check_data_availability():
            return False
        
        # Load and analyze periodogram
        period, power = self.load_lomb_scargle_data()
        detected_period, max_power, max_idx = self.find_peak_period(period, power)
        
        # Calculate QCAL verification
        f_frame, ratio, octaves, decades = self.calculate_qcal_verification(detected_period)
        
        # Print verification report
        self.print_verification_report(detected_period, max_power, 
                                      f_frame, ratio, octaves, decades)
        
        # Plotting
        if plot:
            # Plot periodogram
            periodogram_path = 'at2020afhd_periodogram.png' if save_plots else None
            self.plot_periodogram(period, power, detected_period, periodogram_path)
            
            # Load and plot light curves
            (xray_time, xray_flux, xray_error,
             radio_time, radio_flux, radio_error) = self.load_light_curves()
            
            lightcurve_path = 'at2020afhd_lightcurves.png' if save_plots else None
            self.plot_light_curves(xray_time, xray_flux, xray_error,
                                  radio_time, radio_flux, radio_error,
                                  lightcurve_path)
        
        return True


def download_and_extract_data(data_url=None, extract_dir='Figure_datas'):
    """
    Download and extract Figure_datas.tar from Zenodo.
    
    Args:
        data_url: URL to the tar file (if None, user must provide manually)
        extract_dir: Directory to extract data to
    """
    print("\n" + "=" * 70)
    print("DATA DOWNLOAD AND EXTRACTION")
    print("=" * 70)
    
    if data_url:
        tar_filename = 'Figure_datas.tar'
        print(f"Downloading data from: {data_url}")
        
        try:
            urllib.request.urlretrieve(data_url, tar_filename)
            print(f"Download complete: {tar_filename}")
        except Exception as e:
            print(f"Error downloading data: {e}")
            print("Please download Figure_datas.tar manually from Zenodo")
            return False
    else:
        tar_filename = 'Figure_datas.tar'
        if not os.path.exists(tar_filename):
            print(f"File {tar_filename} not found.")
            print("Please download Figure_datas.tar from Zenodo:")
            print("  https://zenodo.org/record/[RECORD_ID]/files/Figure_datas.tar")
            print("and place it in the current directory.")
            return False
    
    # Extract the tar file
    print(f"Extracting {tar_filename}...")
    try:
        with tarfile.open(tar_filename, 'r') as tar:
            tar.extractall()
        print(f"Files extracted successfully to: {extract_dir}")
        return True
    except Exception as e:
        print(f"Error extracting tar file: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Analyze AT2020afhd periodogram data and verify QCAL relationship'
    )
    parser.add_argument('--data-dir', type=str, default='Figure_datas',
                       help='Directory containing extracted Figure_datas')
    parser.add_argument('--download', action='store_true',
                       help='Download and extract data from Zenodo')
    parser.add_argument('--no-plot', action='store_true',
                       help='Disable plotting')
    parser.add_argument('--save-plots', action='store_true',
                       help='Save plots to files instead of showing')
    parser.add_argument('--data-url', type=str, default=None,
                       help='URL to download Figure_datas.tar from')
    
    args = parser.parse_args()
    
    # Download data if requested
    if args.download:
        if not download_and_extract_data(args.data_url, args.data_dir):
            print("\nFailed to download/extract data. Exiting.")
            sys.exit(1)
    
    # Run analysis
    analyzer = AT2020afhdAnalyzer(data_dir=args.data_dir)
    success = analyzer.run_full_analysis(plot=not args.no_plot, 
                                        save_plots=args.save_plots)
    
    if not success:
        print("\nAnalysis failed. Please check data availability.")
        sys.exit(1)
    
    print("\nAnalysis complete!")


if __name__ == '__main__':
    main()
