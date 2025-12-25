#!/bin/bash

# Setup script for GEANT4 MCP Server

set -e

echo "=================================================="
echo "GEANT4 Simulation with MCP Server - Setup"
echo "=================================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop for macOS."
    echo "   Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✓ Docker is installed"

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Create output directory
mkdir -p output
echo "✓ Created output directory"

# Build Docker image
echo ""
echo "Building Docker image (this will take 30-60 minutes)..."
echo "You can safely cancel and restart this process if needed."
echo ""

docker-compose build

echo ""
echo "✓ Docker image built successfully"
echo ""

# Start the container
echo "Starting container..."
docker-compose up -d

echo ""
echo "✓ Container started"
echo ""

# Wait for container to be ready
echo "Waiting for container to be ready..."
sleep 5

# Check if container is running
if docker ps | grep -q geant4-simulation; then
    echo "✓ Container is running"
else
    echo "❌ Container failed to start. Check logs with: docker-compose logs"
    exit 1
fi

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure Claude Desktop:"
echo "   Add the following to:"
echo "   ~/Library/Application Support/Claude/claude_desktop_config.json"
echo ""
cat claude_desktop_config.json
echo ""
echo "2. Restart Claude Desktop"
echo ""
echo "3. Test the simulation:"
echo "   docker exec -it geant4-simulation python3 simulation.py"
echo ""
echo "4. View logs:"
echo "   docker-compose logs -f"
echo ""
echo "5. Stop the container:"
echo "   docker-compose down"
echo ""
