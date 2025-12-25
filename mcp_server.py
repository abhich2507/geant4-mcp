#!/usr/bin/env python3
"""
MCP Server for GEANT4 Simulation
Provides tools for Claude Desktop to control and run GEANT4 simulations
"""

import asyncio
import json
from pathlib import Path
from typing import Any
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import AnyUrl

# Import simulation
from simulation import Geant4Simulation, SimulationConfig

# Create MCP server
app = Server("geant4-simulation-server")

# Global simulation instance
current_simulation = None
current_config = SimulationConfig()


@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools for the MCP server"""
    return [
        Tool(
            name="configure_simulation",
            description=(
                "Configure the GEANT4 simulation parameters including particle type, "
                "energy, detector dimensions, and material. Returns the current configuration."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "particle_type": {
                        "type": "string",
                        "description": "Particle type (gamma, e-, e+, proton, neutron, etc.)",
                        "default": "gamma"
                    },
                    "particle_energy": {
                        "type": "number",
                        "description": "Particle energy in MeV",
                        "default": 1.0
                    },
                    "particle_position": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Particle initial position [x, y, z] in cm",
                        "default": [0.0, 0.0, -10.0]
                    },
                    "particle_direction": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Particle direction unit vector [x, y, z]",
                        "default": [0.0, 0.0, 1.0]
                    },
                    "cube_size_x": {
                        "type": "number",
                        "description": "Detector cube size in X dimension (cm)",
                        "default": 10.0
                    },
                    "cube_size_y": {
                        "type": "number",
                        "description": "Detector cube size in Y dimension (cm)",
                        "default": 10.0
                    },
                    "cube_size_z": {
                        "type": "number",
                        "description": "Detector cube size in Z dimension (cm)",
                        "default": 10.0
                    },
                    "cube_material": {
                        "type": "string",
                        "description": "Detector material (G4_WATER, G4_Al, G4_Pb, etc.)",
                        "default": "G4_WATER"
                    },
                    "num_events": {
                        "type": "integer",
                        "description": "Number of events to simulate",
                        "default": 100
                    }
                }
            }
        ),
        Tool(
            name="run_simulation",
            description=(
                "Run the GEANT4 simulation with the current configuration. "
                "Returns summary of results including energy deposition."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "num_events": {
                        "type": "integer",
                        "description": "Number of events to run (overrides config if provided)"
                    }
                }
            }
        ),
        Tool(
            name="get_simulation_status",
            description="Get the current simulation configuration and status",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_results",
            description=(
                "Get detailed results from the last simulation run, "
                "including event-by-event data and summary statistics"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "include_events": {
                        "type": "boolean",
                        "description": "Include detailed event data (default: false)",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="save_configuration",
            description="Save the current simulation configuration to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename to save configuration (default: config.json)"
                    }
                }
            }
        ),
        Tool(
            name="load_configuration",
            description="Load simulation configuration from a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename to load configuration from"
                    }
                },
                "required": ["filename"]
            }
        )
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls from Claude"""
    global current_simulation, current_config
    
    if arguments is None:
        arguments = {}
    
    try:
        if name == "configure_simulation":
            # Update configuration
            if "particle_type" in arguments:
                current_config.particle_type = arguments["particle_type"]
            if "particle_energy" in arguments:
                current_config.particle_energy = arguments["particle_energy"]
            if "particle_position" in arguments:
                current_config.particle_position = arguments["particle_position"]
            if "particle_direction" in arguments:
                current_config.particle_direction = arguments["particle_direction"]
            if "cube_size_x" in arguments:
                current_config.cube_size_x = arguments["cube_size_x"]
            if "cube_size_y" in arguments:
                current_config.cube_size_y = arguments["cube_size_y"]
            if "cube_size_z" in arguments:
                current_config.cube_size_z = arguments["cube_size_z"]
            if "cube_material" in arguments:
                current_config.cube_material = arguments["cube_material"]
            if "num_events" in arguments:
                current_config.num_events = arguments["num_events"]
            
            config_dict = current_config.to_dict()
            return [
                TextContent(
                    type="text",
                    text=f"Configuration updated successfully:\n{json.dumps(config_dict, indent=2)}"
                )
            ]
        
        elif name == "run_simulation":
            # Create new simulation with current config
            current_simulation = Geant4Simulation(current_config)
            current_simulation.initialize()
            
            # Run simulation
            num_events = arguments.get("num_events", current_config.num_events)
            current_simulation.run(num_events)
            
            # Save results
            current_simulation.save_results()
            
            # Get summary
            summary = current_simulation.get_summary()
            
            return [
                TextContent(
                    type="text",
                    text=f"Simulation completed successfully!\n{summary}"
                )
            ]
        
        elif name == "get_simulation_status":
            status = {
                "configuration": current_config.to_dict(),
                "simulation_run": current_simulation is not None,
                "results_available": current_simulation is not None and len(current_simulation.results) > 0
            }
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps(status, indent=2)
                )
            ]
        
        elif name == "get_results":
            if current_simulation is None or not current_simulation.results:
                return [
                    TextContent(
                        type="text",
                        text="No simulation results available. Run a simulation first."
                    )
                ]
            
            include_events = arguments.get("include_events", False)
            
            results = {
                "summary": {
                    "total_events": len(current_simulation.results),
                    "total_energy_deposited_MeV": sum(r["energy_deposited_MeV"] for r in current_simulation.results),
                    "avg_energy_deposited_MeV": sum(r["energy_deposited_MeV"] for r in current_simulation.results) / len(current_simulation.results)
                }
            }
            
            if include_events:
                results["events"] = current_simulation.results
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps(results, indent=2)
                )
            ]
        
        elif name == "save_configuration":
            filename = arguments.get("filename", "config.json")
            filepath = Path(filename)
            
            # Ensure directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            # Save configuration
            with open(filepath, 'w') as f:
                json.dump(current_config.to_dict(), f, indent=2)
            
            return [
                TextContent(
                    type="text",
                    text=f"Configuration saved to {filepath}"
                )
            ]
        
        elif name == "load_configuration":
            filename = arguments["filename"]
            filepath = Path(filename)
            
            if not filepath.exists():
                return [
                    TextContent(
                        type="text",
                        text=f"Configuration file not found: {filepath}"
                    )
                ]
            
            # Load configuration
            with open(filepath, 'r') as f:
                config_data = json.load(f)
            
            current_config = SimulationConfig.from_dict(config_data)
            
            return [
                TextContent(
                    type="text",
                    text=f"Configuration loaded from {filepath}:\n{json.dumps(current_config.to_dict(), indent=2)}"
                )
            ]
        
        else:
            return [
                TextContent(
                    type="text",
                    text=f"Unknown tool: {name}"
                )
            ]
    
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=f"Error executing {name}: {str(e)}"
            )
        ]


async def main():
    """Main entry point for the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="geant4-simulation",
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
