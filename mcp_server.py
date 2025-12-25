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
        ),
        Tool(
            name="create_plots",
            description=(
                "Create plots from the ROOT file simulation results. "
                "Generates multiple plots including energy deposition histograms, "
                "scatter plots, and summary dashboards. Returns image paths."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "root_file": {
                        "type": "string",
                        "description": "Path to ROOT file (default: output/simulation_results.root)",
                        "default": "output/simulation_results.root"
                    }
                }
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
        
        elif name == "create_plots":
            import uproot
            import numpy as np
            import matplotlib.pyplot as plt
            import base64
            from io import BytesIO
            
            root_file = arguments.get("root_file", "output/simulation_results.root")
            
            if not Path(root_file).exists():
                return [
                    TextContent(
                        type="text",
                        text=f"ROOT file not found: {root_file}. Run a simulation first."
                    )
                ]
            
            # Read ROOT file
            with uproot.open(root_file) as f:
                tree = f["events"]
                energy_deposited = tree["energy_deposited"].array()
                truth_energy = tree["truth_energy"].array()
                tracks = tree["tracks_created"].array()
                event_id = tree["event_id"].array()
            
            # Create output directory
            output_dir = Path("output/plots")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            plot_files = []
            
            # Plot 1: Energy Deposition Histogram
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
            plot_files.append(str(plot1))
            
            # Plot 2: Summary Dashboard
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            
            axes[0, 0].hist(energy_deposited, bins=30, alpha=0.7, color='blue', edgecolor='black')
            axes[0, 0].set_xlabel('Energy Deposited (MeV)')
            axes[0, 0].set_ylabel('Events')
            axes[0, 0].set_title('Energy Distribution')
            axes[0, 0].grid(True, alpha=0.3)
            
            axes[0, 1].scatter(event_id, energy_deposited, alpha=0.5, s=10)
            axes[0, 1].set_xlabel('Event ID')
            axes[0, 1].set_ylabel('Energy Deposited (MeV)')
            axes[0, 1].set_title('Energy per Event')
            axes[0, 1].grid(True, alpha=0.3)
            
            axes[1, 0].hist(tracks, bins=range(0, int(np.max(tracks))+2), alpha=0.7, color='green', edgecolor='black')
            axes[1, 0].set_xlabel('Tracks Created')
            axes[1, 0].set_ylabel('Events')
            axes[1, 0].set_title('Secondary Tracks')
            axes[1, 0].grid(True, alpha=0.3)
            
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
            plot2 = output_dir / "summary_dashboard.png"
            plt.savefig(plot2, dpi=150)
            plt.close()
            plot_files.append(str(plot2))
            
            # Return text with plot locations
            result_text = f"Created {len(plot_files)} plots from {root_file}:\n\n"
            for plot_file in plot_files:
                result_text += f"✓ {plot_file}\n"
            
            result_text += f"\nStatistics:\n"
            result_text += f"  Total Events: {len(event_id)}\n"
            result_text += f"  Mean Energy Deposited: {np.mean(energy_deposited):.4f} MeV\n"
            result_text += f"  Std Dev: {np.std(energy_deposited):.4f} MeV\n"
            result_text += f"  Total Energy Deposited: {np.sum(energy_deposited):.2f} MeV\n"
            
            return [
                TextContent(
                    type="text",
                    text=result_text
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
