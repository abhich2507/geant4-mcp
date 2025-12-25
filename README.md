# GEANT4 Simulation with MCP Server

A complete GEANT4 particle physics simulation system using Python bindings, integrated with Claude Desktop via Model Context Protocol (MCP) server. Fully containerized with Docker for easy deployment on macOS, Windows, and Linux.

> **Ready to Use**: Clone this repo and run with Docker - no manual GEANT4 installation required!

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
- **ROOT File Support**: Output data in ROOT TTree format for advanced analysis
- **Plotting Tools**: Generate physics plots directly from Claude Desktop
- **Cross-Platform**: Works on macOS, Windows (WSL2), and Linux

## What Users Get

After cloning this repository, users can:

1. **Build and run in 3 commands**:
   ```bash
   git clone https://github.com/<your-username>/geant4-mcp.git
   cd geant4-mcp
   docker-compose up -d
   ```

2. **Control from Claude Desktop** - Configure and run simulations through natural language

3. **No GEANT4 installation needed** - Everything is containerized

4. **Complete working example** - Default configuration runs out of the box

## Quick Start

### Prerequisites

- **macOS/Linux**: Docker Desktop installed
- **Windows**: Docker Desktop with WSL2 enabled
- Claude Desktop application
- 10+ GB disk space
- 8+ GB RAM recommended

### 1. Build and Start Docker Container

#### macOS/Linux:
```bash
# Build the Docker image (this will take 30-60 minutes for GEANT4)
docker-compose build

# Start the container
docker-compose up -d
```

#### Windows (PowerShell or Command Prompt):
```powershell
# Build the Docker image (this will take 30-60 minutes for GEANT4)
docker-compose build

# Start the container
docker-compose up -d
```

> **Note for Windows**: Make sure Docker Desktop is running and WSL2 integration is enabled in Settings → Resources → WSL Integration.

### 2. Configure Claude Desktop

Add the following to your Claude Desktop configuration file:

#### macOS:
**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json`

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

#### Windows:
**Location**: `%APPDATA%\Claude\claude_desktop_config.json`

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

> **Windows Tip**: You can open this location by typing `%APPDATA%\Claude` in Windows Explorer address bar or by running:
> ```powershell
> notepad "$env:APPDATA\Claude\claude_desktop_config.json"
> ```

#### Linux:
**Location**: `~/.config/Claude/claude_desktop_config.json`

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

**macOS**:
```bash
pkill -9 "Claude" && open -a "Claude"
```

**Windows**:
- Close Claude Desktop completely (check system tray)
- Reopen from Start Menu

**Linux**:
```bash
killall claude && claude &
```

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

#### macOS/Linux:
```bash
# Enter the container
docker exec -it geant4-simulation bash

# Run with default configuration
python3 simulation.py

# Run with custom configuration
python3 simulation.py config.json
```

#### Windows (PowerShell):
```powershell
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

#### macOS/Linux:
```bash
# Rebuild container
docker-compose build

# Restart container
docker-compose restart
```

#### Windows (PowerShell):
```powershell
# Rebuild container
docker-compose build

# Restart container
docker-compose restart
```

### Viewing Logs

#### All Platforms:
```bash
# View MCP server logs
docker-compose logs -f

# View container logs
docker logs geant4-simulation
```

## Troubleshooting

### Container won't start
#### macOS/Linux:
```bash
docker-compose down
docker-compose up -d
docker-compose logs
```

#### Windows (PowerShell):
```powershell
docker-compose down
docker-compose up -d
docker-compose logs
```

### Claude Desktop doesn't see the server
1. Check container is running: `docker ps`
2. Verify configuration file location:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`
3. Restart Claude Desktop completely
4. Check MCP server logs in Claude Desktop Developer Tools

### Windows-Specific Issues

#### Docker not found
- Ensure Docker Desktop is installed and running
- Check that Docker Desktop is set to start on login
- Verify WSL2 is enabled: `wsl --status` in PowerShell

#### WSL2 Integration Issues
1. Open Docker Desktop Settings
2. Go to Resources → WSL Integration
3. Enable integration with your WSL2 distro
4. Click "Apply & Restart"

#### Permission Denied Errors
- Run PowerShell/Command Prompt as Administrator
- Ensure your user is in the `docker-users` group

#### Path Issues in Windows
If you see path-related errors, ensure you're using forward slashes in Docker commands or let Docker handle the path conversion automatically.

### Python import errors
The GEANT4 Python bindings may take a long time to compile. Wait for the initial build to complete.

## Performance Notes

- **First Build**: 30-60 minutes (GEANT4 compilation)
- **Container Start**: ~10 seconds
- **Simulation Speed**: ~100-1000 events/second (depends on complexity)
- **Windows Note**: Performance with WSL2 is comparable to native Linux. If using Hyper-V backend, expect 10-20% slower compilation times.

## Platform-Specific Notes

### macOS
- **Apple Silicon (M1/M2/M3)**: Docker runs via Rosetta 2 translation layer. First build may take longer.
- **Intel Macs**: Native x86_64 performance.
- Configuration location: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
- **Requires**: Windows 10/11 with WSL2 enabled
- **Docker Backend**: WSL2 backend recommended (not Hyper-V)
- **File Performance**: Keep project files in WSL2 filesystem for better performance
- Configuration location: `%APPDATA%\Claude\claude_desktop_config.json`
- To access WSL filesystem: `\\wsl$\Ubuntu\home\<username>\`

### Linux
- **Native Performance**: Best performance on native Linux
- **Docker**: Requires `docker` and `docker-compose` installed
- Configuration location: `~/.config/Claude/claude_desktop_config.json`

## Requirements

### All Platforms
- Claude Desktop application
- 10+ GB disk space
- 8+ GB RAM recommended

### macOS
- macOS 11+ (Big Sur or later)
- Docker Desktop for Mac

### Windows  
- Windows 10/11 (64-bit)
- WSL2 enabled
- Docker Desktop for Windows
- Ubuntu WSL2 distro (recommended)

### Linux
- Modern Linux distribution (Ubuntu 20.04+, Fedora 35+, etc.)
- Docker Engine or Docker Desktop
- docker-compose

## Installation Guides

### Windows Setup from Scratch

1. **Enable WSL2**:
   ```powershell
   # Run in PowerShell as Administrator
   wsl --install
   # Restart computer
   ```

2. **Install Ubuntu on WSL2**:
   ```powershell
   wsl --install -d Ubuntu
   # Set up username and password when prompted
   ```

3. **Install Docker Desktop**:
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and enable WSL2 integration
   - Go to Settings → Resources → WSL Integration
   - Enable integration with Ubuntu

4. **Clone project in WSL2**:
   ```bash
   # Open Ubuntu terminal
   cd ~
   git clone <repository-url>
   cd geant4-mcp
   ```

5. **Continue with Quick Start section above**

### macOS Setup from Scratch

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Docker Desktop**:
   ```bash
   brew install --cask docker
   # Or download from: https://www.docker.com/products/docker-desktop
   ```

3. **Open Docker Desktop** and complete setup

4. **Continue with Quick Start section above**

### Linux Setup from Scratch

1. **Install Docker** (Ubuntu/Debian):
   ```bash
   sudo apt-get update
   sudo apt-get install docker.io docker-compose
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   # Log out and back in for group changes to take effect
   ```

2. **For other distros**, see: https://docs.docker.com/engine/install/

3. **Continue with Quick Start section above**

## Publishing and Sharing

### Publishing to GitHub

This project is ready to be published on GitHub! Users will be able to:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/geant4-mcp.git
   cd geant4-mcp
   ```

2. **Build and run** following the Quick Start instructions above

3. **All dependencies are containerized** - users don't need to install GEANT4 or Python packages manually

### What's Included for Users

✅ **Ready to Run**:
- Complete Docker setup (Dockerfile + docker-compose.yml)
- All Python code (simulation.py, mcp_server.py)
- Default configuration (config.json)
- Documentation (README.md + additional guides)

✅ **No Manual Setup Required**:
- GEANT4 is compiled automatically in Docker
- All Python dependencies installed via requirements.txt
- MCP server ready to connect to Claude Desktop

✅ **Cross-Platform**:
- Works on macOS (Intel + Apple Silicon)
- Works on Windows (with WSL2)
- Works on Linux (native)

### Before Publishing

**Optional but Recommended**:

1. **Review sensitive data**:
   ```bash
   # Check what will be committed
   git status
   ```

2. **Test on a fresh clone** (optional):
   ```bash
   cd /tmp
   git clone /path/to/your/repo test-clone
   cd test-clone
   docker-compose build
   docker-compose up -d
   ```

3. **Add a license** (if not already present):
   ```bash
   # Choose a license at https://choosealicense.com/
   # Common choices: MIT, Apache 2.0, GPL-3.0
   ```

### What Users Need

Users only need to have installed:
- **Git** (to clone the repository)
- **Docker Desktop** (for their platform)
- **Claude Desktop** (to use the MCP integration)

Everything else is handled automatically by Docker!

### Repository Setup

If you haven't pushed to GitHub yet:

```bash
# Initialize git (if needed)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: GEANT4 simulation with MCP server"

# Add your GitHub repository as remote
git remote add origin https://github.com/<your-username>/geant4-mcp.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Recommended GitHub Settings

1. **Add Topics/Tags**:
   - `geant4`
   - `particle-physics`
   - `simulation`
   - `mcp-server`
   - `docker`
   - `claude-desktop`
   - `python`

2. **Add Description**:
   > "GEANT4 particle physics simulation with MCP server integration for Claude Desktop. Fully containerized with Docker."

3. **Enable Issues** - So users can report problems or ask questions

4. **Add GitHub Actions** (optional) - For automated Docker builds

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This software uses GEANT4, which is distributed under the [Geant4 Software License](https://geant4.web.cern.ch/license).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Citation

If you use this software in your research, please cite:

```bibtex
@software{geant4_mcp_2025,
  title={GEANT4 Simulation with MCP Server},
  author={Your Name},
  year={2025},
  url={https://github.com/<your-username>/geant4-mcp}
}
```

## Acknowledgments

- [GEANT4 Collaboration](https://geant4.web.cern.ch/) for the particle physics simulation toolkit
- [Anthropic](https://www.anthropic.com/) for Claude Desktop and MCP protocol
- [CERN ROOT](https://root.cern/) for data analysis framework

