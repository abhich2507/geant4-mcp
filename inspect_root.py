#!/usr/bin/env python3
"""Inspect ROOT file contents and create plots"""

import uproot
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Open ROOT file
with uproot.open("output/simulation_results.root") as f:
    print("=" * 60)
    print("ROOT File Inspection")
    print("=" * 60)
    
    # List trees
    print(f"\nTrees in file: {list(f.keys())}")
    
    # Get events tree
    tree = f["events"]
    
    # List branches
    print(f"\nBranches: {list(tree.keys())}")
    print(f"Number of entries: {tree.num_entries}")
    
    # Show first 5 entries
    print("\n" + "=" * 60)
    print("Sample Data (First 5 Events)")
    print("=" * 60)
    
    event_id = tree["event_id"].array()
    particle_id = tree["particle_id"].array()
    truth_energy = tree["truth_energy"].array()
    energy_deposited = tree["energy_deposited"].array()
    tracks = tree["tracks_created"].array()
    
    for i in range(min(5, len(event_id))):
        print(f"\nEvent {event_id[i]}:")
        print(f"  Particle ID (PDG): {particle_id[i]} (gamma=22)")
        print(f"  Truth Energy: {truth_energy[i]:.3f} MeV")
        print(f"  Energy Deposited: {energy_deposited[i]:.3f} MeV")
        print(f"  Tracks Created: {tracks[i]}")
    
    # Statistics
    print("\n" + "=" * 60)
    print("Statistics")
    print("=" * 60)
    print(f"Mean Energy Deposited: {np.mean(energy_deposited):.4f} MeV")
    print(f"Std Energy Deposited: {np.std(energy_deposited):.4f} MeV")
    print(f"Min Energy Deposited: {np.min(energy_deposited):.4f} MeV")
    print(f"Max Energy Deposited: {np.max(energy_deposited):.4f} MeV")
    
    # Create plots
    print("\n" + "=" * 60)
    print("Creating Plots")
    print("=" * 60)
    
    output_dir = Path("output/plots")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Plot 1: Energy Deposition Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(energy_deposited, bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.xlabel('Energy Deposited (MeV)', fontsize=12)
    plt.ylabel('Number of Events', fontsize=12)
    plt.title('Energy Deposition Distribution', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plot1 = output_dir / "energy_deposition_hist.png"
    plt.savefig(plot1, dpi=150)
    plt.close()
    print(f"✓ Saved: {plot1}")
    
    # Plot 2: Truth Energy vs Deposited Energy
    plt.figure(figsize=(10, 6))
    plt.scatter(truth_energy, energy_deposited, alpha=0.5, s=20)
    plt.xlabel('Truth Energy (MeV)', fontsize=12)
    plt.ylabel('Energy Deposited (MeV)', fontsize=12)
    plt.title('Truth Energy vs Deposited Energy', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plot2 = output_dir / "truth_vs_deposited.png"
    plt.savefig(plot2, dpi=150)
    plt.close()
    print(f"✓ Saved: {plot2}")
    
    # Plot 3: Number of Tracks Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(tracks, bins=range(0, int(np.max(tracks))+2), alpha=0.7, color='green', edgecolor='black')
    plt.xlabel('Number of Tracks Created', fontsize=12)
    plt.ylabel('Number of Events', fontsize=12)
    plt.title('Secondary Tracks Distribution', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plot3 = output_dir / "tracks_distribution.png"
    plt.savefig(plot3, dpi=150)
    plt.close()
    print(f"✓ Saved: {plot3}")
    
    # Plot 4: Event-by-event Energy Deposition
    plt.figure(figsize=(12, 6))
    plt.plot(event_id, energy_deposited, marker='o', markersize=3, linestyle='-', alpha=0.6)
    plt.xlabel('Event ID', fontsize=12)
    plt.ylabel('Energy Deposited (MeV)', fontsize=12)
    plt.title('Energy Deposition per Event', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plot4 = output_dir / "energy_vs_event.png"
    plt.savefig(plot4, dpi=150)
    plt.close()
    print(f"✓ Saved: {plot4}")
    
    # Plot 5: Cumulative Energy Deposition
    cumulative_energy = np.cumsum(energy_deposited)
    plt.figure(figsize=(12, 6))
    plt.plot(event_id, cumulative_energy, linewidth=2, color='red')
    plt.xlabel('Event ID', fontsize=12)
    plt.ylabel('Cumulative Energy Deposited (MeV)', fontsize=12)
    plt.title('Cumulative Energy Deposition', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plot5 = output_dir / "cumulative_energy.png"
    plt.savefig(plot5, dpi=150)
    plt.close()
    print(f"✓ Saved: {plot5}")
    
    # Plot 6: Summary Dashboard
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Histogram
    axes[0, 0].hist(energy_deposited, bins=30, alpha=0.7, color='blue', edgecolor='black')
    axes[0, 0].set_xlabel('Energy Deposited (MeV)')
    axes[0, 0].set_ylabel('Events')
    axes[0, 0].set_title('Energy Distribution')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Scatter
    axes[0, 1].scatter(event_id, energy_deposited, alpha=0.5, s=10)
    axes[0, 1].set_xlabel('Event ID')
    axes[0, 1].set_ylabel('Energy Deposited (MeV)')
    axes[0, 1].set_title('Energy per Event')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Tracks
    axes[1, 0].hist(tracks, bins=range(0, int(np.max(tracks))+2), alpha=0.7, color='green', edgecolor='black')
    axes[1, 0].set_xlabel('Tracks Created')
    axes[1, 0].set_ylabel('Events')
    axes[1, 0].set_title('Secondary Tracks')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Stats text
    stats_text = f"""Statistics Summary
    
Total Events: {len(event_id)}
Mean Energy: {np.mean(energy_deposited):.4f} MeV
Std Dev: {np.std(energy_deposited):.4f} MeV
Min: {np.min(energy_deposited):.4f} MeV
Max: {np.max(energy_deposited):.4f} MeV

Total Deposited: {np.sum(energy_deposited):.2f} MeV
Mean Tracks: {np.mean(tracks):.1f}"""
    
    axes[1, 1].text(0.1, 0.5, stats_text, fontsize=11, family='monospace', 
                    verticalalignment='center', transform=axes[1, 1].transAxes)
    axes[1, 1].axis('off')
    
    plt.suptitle('GEANT4 Simulation Summary', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plot6 = output_dir / "summary_dashboard.png"
    plt.savefig(plot6, dpi=150)
    plt.close()
    print(f"✓ Saved: {plot6}")
    
    print(f"\nAll plots saved to: {output_dir}/")
    print("Plot files:")
    for plot_file in sorted(output_dir.glob("*.png")):
        print(f"  - {plot_file.name}")
