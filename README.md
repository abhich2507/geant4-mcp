# GEANT4 Simulation with MCP Server

A complete GEANT4 simulation system using Python bindings, integrated with Claude Desktop via Model Context Protocol (MCP) server, all running in Docker on macOS.

## Features

- **GEANT4 Python Simulation**: Full particle physics simulation using GEANT4 Python bindings
- **Configurable Parameters**: 
  - Particle type (gamma, e-, e+, proton, neutron, etc.)
  - Particle energy (MeV)
  - Cubic detector dimensions (configurable X, Y, Z)
  - Detector material (various GEANT4 materials)
- **MCP Server Integration**: Control simulations directly from Claude Desktop
- **Docker Container**: Complete isolated environment with all dependencies
- **JSON Output**: Easy-to-parse simulation results

## Quick Start

### 1. Build and Start Docker Container

```bash
# Build the Docker image (this will take 30-60 minutes for GEANT4)
docker-compose build

# Start the container
docker-compose up -d
```

### 2. Configure Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "geant4-simulation": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "geant4-simulation",
        "python3",
        "/workspace/mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/opt/geant4/lib"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

Restart Claude Desktop to load the MCP server.

### 4. Use from Claude Desktop

You can now control the simulation from Claude Desktop:

```
Configure a simulation with:
- 1 MeV gamma particles
- 20x20x20 cm water cube
- Run 1000 events
```

## Manual Usage (Without Claude Desktop)

### Run Simulation Directly

```bash
# Enter the container
docker exec -it geant4-simulation bash

# Run with default configuration
python3 simulation.py

# Run with custom configuration
python3 simulation.py config.json
```

### Run MCP Server Standalone

```bash
docker exec -it geant4-simulation python3 mcp_server.py
```

## Available MCP Tools

When using Claude Desktop, the following tools are available:

### 1. `configure_simulation`
Configure simulation parameters:
- `particle_type`: Particle type (gamma, e-, e+, proton, etc.)
- `particle_energy`: Energy in MeV
- `particle_position`: Initial position [x, y, z] in cm
- `particle_direction`: Direction vector [x, y, z]
- `cube_size_x/y/z`: Detector dimensions in cm
- `cube_material`: Material (G4_WATER, G4_Al, G4_Pb, etc.)
- `num_events`: Number of events to simulate

### 2. `run_simulation`
Run the simulation with current configuration

### 3. `get_simulation_status`
Get current configuration and status

### 4. `get_results`
Retrieve detailed simulation results

### 5. `save_configuration`
Save current configuration to file

### 6. `load_configuration`
Load configuration from file

## Configuration File Format

```json
{
  "particle": {
    "type": "gamma",
    "energy_MeV": 1.0,
    "position_cm": [0.0, 0.0, -10.0],
    "direction": [0.0, 0.0, 1.0]
  },
  "detector": {
    "cube_size_x_cm": 10.0,
    "cube_size_y_cm": 10.0,
    "cube_size_z_cm": 10.0,
    "material": "G4_WATER"
  },
  "simulation": {
    "num_events": 100,
    "output_file": "output/simulation_results.json"
  }
}
```

## Output Format

Results are saved in JSON format:

```json
{
  "config": { ... },
  "results": [
    {
      "event_id": 0,
      "primary": { ... },
      "energy_deposited_MeV": 0.85,
      "tracks_created": 5,
      "interactions": 3
    }
  ],
  "summary": {
    "total_events": 100,
    "total_energy_deposited_MeV": 87.3,
    "avg_energy_deposited_MeV": 0.873
  }
}
```

## Common Materials

- `G4_WATER`: Water
- `G4_Al`: Aluminum
- `G4_Pb`: Lead
- `G4_Fe`: Iron
- `G4_Cu`: Copper
- `G4_AIR`: Air
- `G4_CONCRETE`: Concrete
- `G4_TISSUE_SOFT_ICRP`: Soft tissue

## Common Particles

- `gamma`: Photons
- `e-`: Electrons
- `e+`: Positrons
- `proton`: Protons
- `neutron`: Neutrons
- `alpha`: Alpha particles
- `mu-`: Muons

## Development

### Project Structure

```
geant4-mcp/
├── simulation.py          # Main GEANT4 simulation
├── mcp_server.py         # MCP server for Claude Desktop
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker compose configuration
├── requirements.txt      # Python dependencies
├── config.json          # Default configuration
├── output/              # Simulation results
└── README.md           # This file
```

### Rebuilding After Changes

```bash
# Rebuild container
docker-compose build

# Restart container
docker-compose restart
```

### Viewing Logs

```bash
# View MCP server logs
docker-compose logs -f

# View container logs
docker logs geant4-simulation
```

## Troubleshooting

### Container won't start
```bash
docker-compose down
docker-compose up -d
docker-compose logs
```

### Claude Desktop doesn't see the server
1. Check container is running: `docker ps`
2. Verify configuration file location
3. Restart Claude Desktop
4. Check MCP server logs in Claude Desktop Developer Tools

### Python import errors
The GEANT4 Python bindings may take a long time to compile. Wait for the initial build to complete.

## Performance Notes

- **First Build**: 30-60 minutes (GEANT4 compilation)
- **Container Start**: ~10 seconds
- **Simulation Speed**: ~100-1000 events/second (depends on complexity)

## License

This project is provided as-is for educational and research purposes.

## Requirements

- Docker Desktop for macOS
- Claude Desktop
- 10+ GB disk space
- 8+ GB RAM recommended
