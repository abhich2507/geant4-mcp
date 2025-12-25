# GEANT4 MCP Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Desktop (macOS)                    │
│                                                                   │
│  User: "Run a 5 MeV electron simulation in aluminum"            │
│                                                                   │
│         ▼                                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              MCP Client (built-in)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ MCP Protocol (stdio)
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    Docker Container                              │
│                    (geant4-simulation)                           │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  mcp_server.py (MCP Server)                                │ │
│  │  - Exposes tools to Claude                                 │ │
│  │  - configure_simulation()                                  │ │
│  │  - run_simulation()                                        │ │
│  │  - get_results()                                           │ │
│  └──────────────────┬─────────────────────────────────────────┘ │
│                     │                                             │
│                     │ Python API                                 │
│                     │                                             │
│  ┌──────────────────▼─────────────────────────────────────────┐ │
│  │  simulation.py (GEANT4 Simulation)                         │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  DetectorConstruction                                 │ │ │
│  │  │  - Cubic detector geometry                            │ │ │
│  │  │  - Configurable dimensions                            │ │ │
│  │  │  - Material selection                                 │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  PhysicsList                                          │ │ │
│  │  │  - Standard physics processes                         │ │ │
│  │  │  - Electromagnetic interactions                       │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  PrimaryGenerator                                     │ │ │
│  │  │  - Particle type selection                            │ │ │
│  │  │  - Energy configuration                               │ │ │
│  │  │  - Position and direction                             │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │                                                             │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  GEANT4 Core (Python Bindings)                       │ │ │
│  │  │  - Particle transport                                 │ │ │
│  │  │  - Physics simulation                                 │ │ │
│  │  │  - Energy deposition tracking                         │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Output Storage                                             │ │
│  │  /workspace/output/simulation_results.json                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
                             │
                             │ Volume Mount
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    Host macOS Filesystem                         │
│                    ./output/                                     │
│                    - simulation_results.json                     │
│                    - Custom output files                         │
└───────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Configuration Phase
```
Claude Desktop → MCP Client → mcp_server.py → SimulationConfig
```

### 2. Simulation Execution
```
User Request → configure_simulation() → run_simulation() →
  → Geant4Simulation.initialize() →
  → Geant4Simulation.run() →
  → Multiple Events →
  → Energy Deposition Tracking →
  → Results Collection
```

### 3. Results Retrieval
```
Results → JSON File → get_results() → MCP Response → Claude Desktop
```

## Component Details

### MCP Server (mcp_server.py)
- **Port**: stdio (standard input/output)
- **Protocol**: Model Context Protocol
- **Tools**: 6 available tools for simulation control
- **State**: Maintains current configuration and results

### Simulation Engine (simulation.py)
- **Framework**: GEANT4 Python bindings
- **Particles**: gamma, e-, e+, proton, neutron, etc.
- **Detector**: Configurable cubic geometry
- **Physics**: Standard electromagnetic processes
- **Output**: JSON format with event-by-event data

### Docker Container
- **Base**: Python 3.11
- **GEANT4**: Version 11.2.0 with Python bindings
- **Network**: Bridge mode, port 5000 exposed
- **Volumes**: 
  - `./simulation.py` → `/workspace/simulation.py`
  - `./mcp_server.py` → `/workspace/mcp_server.py`
  - `./output/` → `/workspace/output/`

## Interaction Example

```
User: "Run a 10 MeV proton simulation in lead"

1. Claude Desktop receives request
2. MCP client calls configure_simulation():
   - particle_type: "proton"
   - particle_energy: 10.0
   - cube_material: "G4_Pb"
3. MCP client calls run_simulation()
4. simulation.py executes:
   - Constructs lead cube detector
   - Generates 10 MeV protons
   - Tracks particles through material
   - Records energy deposition
5. Results saved to JSON
6. MCP client calls get_results()
7. Claude Desktop displays summary

Claude: "Simulation complete! 
        100 events processed
        Average energy deposited: 8.7 MeV
        Total tracks created: 450"
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Claude Desktop (macOS) |
| Protocol | Model Context Protocol (MCP) |
| API Server | Python MCP Server |
| Simulation | GEANT4 11.2.0 (Python bindings) |
| Container | Docker + Docker Compose |
| Data Format | JSON |
| OS | macOS (host) + Ubuntu 22.04 (container) |
