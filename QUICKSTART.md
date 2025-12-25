# 🚀 Quick Start Guide

## Prerequisites
- Docker Desktop installed and running on macOS
- Claude Desktop installed

## Step-by-Step Setup (5 minutes + build time)

### 1. Build and Start (30-60 minutes for first build)
```bash
# Option A: Use setup script
./setup.sh

# Option B: Use Make
make setup

# Option C: Manual
docker-compose build
docker-compose up -d
```

### 2. Configure Claude Desktop

Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add this configuration:
```json
{
  "mcpServers": {
    "geant4-simulation": {
      "command": "docker",
      "args": ["exec", "-i", "geant4-simulation", "python3", "/workspace/mcp_server.py"],
      "env": {
        "PYTHONPATH": "/opt/geant4/lib"
      }
    }
  }
}
```

### 3. Restart Claude Desktop

Quit and reopen Claude Desktop.

### 4. Test in Claude Desktop

Ask Claude:
```
Can you configure and run a GEANT4 simulation with 
1 MeV gamma rays hitting a 10x10x10 cm water cube?
```

## Testing Without Claude Desktop

```bash
# Run a test
make test

# Or manually
docker exec -it geant4-simulation python3 simulation.py

# Check results
cat output/simulation_results.json
```

## Common Commands

```bash
# View logs
make logs

# Open shell in container
make shell

# Run simulation
make run

# Stop everything
make stop

# Clean up
make clean
```

## Example Prompts for Claude

1. **Basic simulation:**
   ```
   Run a simulation with 5 MeV electrons in a 20x20x20 cm aluminum cube
   ```

2. **Get results:**
   ```
   What were the results of the last simulation?
   ```

3. **Change parameters:**
   ```
   Configure the simulation to use protons with 100 MeV energy
   and a 30x30x30 cm lead cube
   ```

4. **Save configuration:**
   ```
   Save the current configuration to my_config.json
   ```

## Troubleshooting

### "Container not running"
```bash
docker-compose up -d
```

### "Claude Desktop doesn't see the server"
1. Check container: `docker ps`
2. Verify config file location
3. Restart Claude Desktop
4. Check Developer Tools in Claude Desktop for errors

### Build takes forever
This is normal! GEANT4 is a large library. The first build takes 30-60 minutes.

## What's Inside?

- **simulation.py**: Main GEANT4 simulation logic
- **mcp_server.py**: MCP server for Claude Desktop
- **Dockerfile**: Complete GEANT4 + Python environment
- **docker-compose.yml**: Container orchestration
- **config.json**: Default simulation parameters

## Next Steps

1. ✅ Build and start container
2. ✅ Configure Claude Desktop  
3. ✅ Test simulation
4. 🎉 Start simulating particles!

## Get Help

View full documentation: `cat README.md`

Check container status: `make status`

View logs: `make logs`
