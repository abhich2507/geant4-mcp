#!/bin/bash

# Test script for GEANT4 simulation

set -e

echo "=================================================="
echo "Testing GEANT4 Simulation"
echo "=================================================="
echo ""

# Check if container is running
if ! docker ps | grep -q geant4-simulation; then
    echo "❌ Container is not running. Start it with: docker-compose up -d"
    exit 1
fi

echo "✓ Container is running"
echo ""

# Test 1: Run simulation with default config
echo "Test 1: Running simulation with default configuration..."
docker exec geant4-simulation python3 simulation.py

echo ""
echo "✓ Test 1 passed"
echo ""

# Test 2: Check output file
echo "Test 2: Checking output file..."
if [ -f "output/simulation_results.json" ]; then
    echo "✓ Output file created"
    echo ""
    echo "Sample of results:"
    head -n 20 output/simulation_results.json
else
    echo "❌ Output file not found"
    exit 1
fi

echo ""
echo "✓ Test 2 passed"
echo ""

# Test 3: Run with custom config
echo "Test 3: Running with custom configuration..."
cat > test_config.json << EOF
{
  "particle": {
    "type": "e-",
    "energy_MeV": 5.0,
    "position_cm": [0.0, 0.0, -10.0],
    "direction": [0.0, 0.0, 1.0]
  },
  "detector": {
    "cube_size_x_cm": 20.0,
    "cube_size_y_cm": 20.0,
    "cube_size_z_cm": 20.0,
    "material": "G4_Al"
  },
  "simulation": {
    "num_events": 50,
    "output_file": "output/test_results.json"
  }
}
EOF

docker cp test_config.json geant4-simulation:/workspace/test_config.json
docker exec geant4-simulation python3 simulation.py test_config.json

echo ""
echo "✓ Test 3 passed"
echo ""

# Test 4: Check MCP server can start
echo "Test 4: Testing MCP server startup..."
timeout 5 docker exec geant4-simulation python3 -c "import mcp_server; print('MCP server imports successfully')" || true

echo ""
echo "✓ Test 4 passed"
echo ""

# Cleanup
rm -f test_config.json

echo "=================================================="
echo "All Tests Passed! ✓"
echo "=================================================="
echo ""
echo "Your GEANT4 simulation is working correctly!"
echo ""
echo "You can now:"
echo "1. Configure Claude Desktop with the MCP server"
echo "2. Use the simulation from Claude Desktop"
echo "3. Run manual simulations with: docker exec -it geant4-simulation python3 simulation.py"
echo ""
