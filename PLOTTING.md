# GEANT4 Simulation Plotting Guide

## Available Plots

When you run a simulation, you can generate plots from the ROOT file using the `create_plots` tool.

### Automatic Plots Generated

1. **Energy Deposition Histogram** (`energy_deposition_hist.png`)
   - Shows distribution of energy deposited across all events
   - Helps identify typical energy deposition values

2. **Truth vs Deposited Energy** (`truth_vs_deposited.png`)
   - Scatter plot comparing initial particle energy to deposited energy
   - Shows energy loss patterns

3. **Secondary Tracks Distribution** (`tracks_distribution.png`)
   - Histogram of number of secondary particles created
   - Indicates interaction complexity

4. **Energy vs Event** (`energy_vs_event.png`)
   - Line plot showing energy deposition for each event
   - Helps identify outliers or trends

5. **Cumulative Energy** (`cumulative_energy.png`)
   - Running total of energy deposited over events
   - Shows total energy accumulation

6. **Summary Dashboard** (`summary_dashboard.png`)
   - 4-panel overview with key statistics
   - Best for quick analysis

## Using with Claude Desktop

Once you've restarted Claude Desktop with the MCP server configured, you can ask:

```
"Create plots from the simulation results"
```

or

```
"Show me visualizations of the energy deposition data"
```

or

```
"Generate all plots from the ROOT file"
```

## Manual Plotting

You can also run the inspection script manually:

```bash
# In the container
docker exec geant4-simulation python3 /workspace/inspect_root.py

# View plots (on host)
open output/plots/summary_dashboard.png
```

## Plot Locations

All plots are saved to:
- Container: `/workspace/output/plots/`
- Host: `./output/plots/`

## Available Data in ROOT File

The ROOT file contains a TTree named "events" with these branches:

- **event_id**: Event number
- **particle_id**: PDG particle code (22=gamma, 11=e-, etc.)
- **truth_energy**: Initial particle energy (MeV)
- **energy_deposited**: Energy deposited in detector (MeV)
- **tracks_created**: Number of secondary tracks
- **interactions**: Number of interactions
- **pos_x, pos_y, pos_z**: Initial particle position (cm)
- **dir_x, dir_y, dir_z**: Initial particle direction

## Custom Analysis

You can create custom plots using Python:

```python
import uproot
import matplotlib.pyplot as plt

# Open ROOT file
with uproot.open("output/simulation_results.root") as f:
    tree = f["events"]
    
    # Read data
    energy = tree["energy_deposited"].array()
    
    # Create custom plot
    plt.hist(energy, bins=50)
    plt.xlabel("Energy (MeV)")
    plt.ylabel("Events")
    plt.savefig("my_custom_plot.png")
```
