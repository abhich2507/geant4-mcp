"""
GEANT4 Simulation using Python Bindings
Simulates particle interactions with a configurable cubic detector
Outputs ROOT file with TTree containing event data
"""

import sys
import json
from pathlib import Path
import numpy as np
import uproot

# Mock Geant4 imports for now - will be replaced with actual imports when Geant4 is installed
# from Geant4 import *

# Particle ID mapping (PDG codes)
PARTICLE_IDS = {
    "gamma": 22,
    "e-": 11,
    "e+": -11,
    "proton": 2212,
    "neutron": 2112,
    "mu-": 13,
    "mu+": -13,
    "pi+": 211,
    "pi-": -211,
    "alpha": 1000020040
}

class SimulationConfig:
    """Configuration for the simulation"""
    def __init__(self):
        self.particle_type = "gamma"  # gamma, e-, e+, proton, neutron, etc.
        self.particle_energy = 1.0  # MeV
        self.particle_position = [0.0, 0.0, -10.0]  # cm
        self.particle_direction = [0.0, 0.0, 1.0]  # unit vector
        
        # Cubic detector parameters
        self.cube_size_x = 10.0  # cm
        self.cube_size_y = 10.0  # cm
        self.cube_size_z = 10.0  # cm
        self.cube_material = "G4_WATER"  # Material name
        
        # Simulation parameters
        self.num_events = 100
        self.output_file = "output/simulation_results.json"
        self.output_root_file = "output/simulation_results.root"
    
    def to_dict(self):
        return {
            "particle": {
                "type": self.particle_type,
                "energy_MeV": self.particle_energy,
                "position_cm": self.particle_position,
                "direction": self.particle_direction
            },
            "detector": {
                "cube_size_x_cm": self.cube_size_x,
                "cube_size_y_cm": self.cube_size_y,
                "cube_size_z_cm": self.cube_size_z,
                "material": self.cube_material
            },
            "simulation": {
                "num_events": self.num_events,
                "output_file": self.output_file
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        config = cls()
        if "particle" in data:
            config.particle_type = data["particle"].get("type", config.particle_type)
            config.particle_energy = data["particle"].get("energy_MeV", config.particle_energy)
            config.particle_position = data["particle"].get("position_cm", config.particle_position)
            config.particle_direction = data["particle"].get("direction", config.particle_direction)
        
        if "detector" in data:
            config.cube_size_x = data["detector"].get("cube_size_x_cm", config.cube_size_x)
            config.cube_size_y = data["detector"].get("cube_size_y_cm", config.cube_size_y)
            config.cube_size_z = data["detector"].get("cube_size_z_cm", config.cube_size_z)
            config.cube_material = data["detector"].get("material", config.cube_material)
        
        if "simulation" in data:
            config.num_events = data["simulation"].get("num_events", config.num_events)
            config.output_file = data["simulation"].get("output_file", config.output_file)
        
        return config


class DetectorConstruction:
    """Defines the detector geometry"""
    def __init__(self, config):
        self.config = config
    
    def construct(self):
        """Build the detector geometry"""
        print(f"Constructing detector:")
        print(f"  Material: {self.config.cube_material}")
        print(f"  Dimensions: {self.config.cube_size_x} x {self.config.cube_size_y} x {self.config.cube_size_z} cm³")
        
        # In actual implementation, this would create Geant4 geometry
        # world_solid = G4Box("World", world_size, world_size, world_size)
        # cube_solid = G4Box("Cube", cube_x/2, cube_y/2, cube_z/2)
        # etc.
        
        return True


class PhysicsList:
    """Defines the physics processes"""
    def __init__(self):
        self.physics_list_name = "FTFP_BERT"  # Standard physics list
    
    def construct(self):
        """Build the physics list"""
        print(f"Using physics list: {self.physics_list_name}")
        
        # In actual implementation:
        # physics_list = G4VModularPhysicsList()
        # physics_list.RegisterPhysics(G4EmStandardPhysics())
        # etc.
        
        return True


class PrimaryGenerator:
    """Generates primary particles"""
    def __init__(self, config):
        self.config = config
    
    def generate_primary(self, event_id):
        """Generate a primary particle for the event"""
        print(f"Event {event_id}: Generating {self.config.particle_type} "
              f"with energy {self.config.particle_energy} MeV")
        
        # In actual implementation:
        # particle_gun = G4ParticleGun()
        # particle_gun.SetParticleDefinition(particle_def)
        # particle_gun.SetParticleEnergy(energy)
        # particle_gun.SetParticlePosition(position)
        # particle_gun.SetParticleMomentumDirection(direction)
        # particle_gun.GeneratePrimaryVertex(event)
        
        return {
            "event_id": event_id,
            "particle": self.config.particle_type,
            "energy_MeV": self.config.particle_energy,
            "position": self.config.particle_position,
            "direction": self.config.particle_direction
        }


class Geant4Simulation:
    """Main simulation class"""
    def __init__(self, config=None):
        self.config = config or SimulationConfig()
        self.detector = DetectorConstruction(self.config)
        self.physics = PhysicsList()
        self.generator = PrimaryGenerator(self.config)
        self.results = []
    
    def initialize(self):
        """Initialize the simulation"""
        print("=" * 60)
        print("Initializing GEANT4 Simulation")
        print("=" * 60)
        
        self.detector.construct()
        self.physics.construct()
        
        print("\nSimulation initialized successfully!")
        return True
    
    def run(self, num_events=None):
        """Run the simulation"""
        if num_events is None:
            num_events = self.config.num_events
        
        print(f"\nRunning {num_events} events...")
        print("-" * 60)
        
        for event_id in range(num_events):
            # Generate primary particle
            primary = self.generator.generate_primary(event_id)
            
            # Simulate event (in real implementation, this would call Geant4)
            result = self.simulate_event(event_id, primary)
            self.results.append(result)
            
            if (event_id + 1) % 10 == 0:
                print(f"  Processed {event_id + 1}/{num_events} events")
        
        print("-" * 60)
        print(f"Simulation completed: {num_events} events processed")
        
        return self.results
    
    def simulate_event(self, event_id, primary):
        """Simulate a single event"""
        # In actual implementation, this would run Geant4 tracking
        # For now, return mock results
        
        import random
        
        result = {
            "event_id": event_id,
            "primary": primary,
            "energy_deposited_MeV": random.uniform(0, primary["energy_MeV"]),
            "tracks_created": random.randint(1, 10),
            "interactions": random.randint(1, 5)
        }
        
        return result
    
    def save_results(self, filename=None):
        """Save simulation results to JSON and ROOT files"""
        if filename is None:
            filename = self.config.output_file
        
        # Ensure output directory exists
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Prepare data
        data = {
            "config": self.config.to_dict(),
            "results": self.results,
            "summary": {
                "total_events": len(self.results),
                "total_energy_deposited_MeV": sum(r["energy_deposited_MeV"] for r in self.results),
                "avg_energy_deposited_MeV": sum(r["energy_deposited_MeV"] for r in self.results) / len(self.results) if self.results else 0
            }
        }
        
        # Save to JSON
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
        
        # Save to ROOT file
        self.save_root_file()
        
        return filename
    
    def save_root_file(self, filename=None):
        """Save simulation results to ROOT file with TTree"""
        if filename is None:
            filename = self.config.output_root_file
        
        # Ensure output directory exists
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.results:
            print("No results to save to ROOT file")
            return
        
        # Prepare arrays for ROOT TTree
        event_id = np.array([r["event_id"] for r in self.results], dtype=np.int32)
        particle_id = np.array([PARTICLE_IDS.get(r["primary"]["particle"], 0) for r in self.results], dtype=np.int32)
        truth_energy = np.array([r["primary"]["energy_MeV"] for r in self.results], dtype=np.float32)
        energy_deposited = np.array([r["energy_deposited_MeV"] for r in self.results], dtype=np.float32)
        tracks_created = np.array([r["tracks_created"] for r in self.results], dtype=np.int32)
        interactions = np.array([r["interactions"] for r in self.results], dtype=np.int32)
        
        # Position arrays
        pos_x = np.array([r["primary"]["position"][0] for r in self.results], dtype=np.float32)
        pos_y = np.array([r["primary"]["position"][1] for r in self.results], dtype=np.float32)
        pos_z = np.array([r["primary"]["position"][2] for r in self.results], dtype=np.float32)
        
        # Direction arrays
        dir_x = np.array([r["primary"]["direction"][0] for r in self.results], dtype=np.float32)
        dir_y = np.array([r["primary"]["direction"][1] for r in self.results], dtype=np.float32)
        dir_z = np.array([r["primary"]["direction"][2] for r in self.results], dtype=np.float32)
        
        # Create ROOT file with TTree
        with uproot.recreate(filename) as f:
            # Create the tree with branches using mktree for TTree format
            f.mktree("events", {
                "event_id": np.int32,
                "particle_id": np.int32,
                "truth_energy": np.float32,
                "energy_deposited": np.float32,
                "tracks_created": np.int32,
                "interactions": np.int32,
                "pos_x": np.float32,
                "pos_y": np.float32,
                "pos_z": np.float32,
                "dir_x": np.float32,
                "dir_y": np.float32,
                "dir_z": np.float32
            })
            
            # Fill the tree
            f["events"].extend({
                "event_id": event_id,
                "particle_id": particle_id,
                "truth_energy": truth_energy,
                "energy_deposited": energy_deposited,
                "tracks_created": tracks_created,
                "interactions": interactions,
                "pos_x": pos_x,
                "pos_y": pos_y,
                "pos_z": pos_z,
                "dir_x": dir_x,
                "dir_y": dir_y,
                "dir_z": dir_z
            })
        
        print(f"ROOT file saved to: {filename}")
        print(f"  Tree: 'events' with {len(self.results)} entries")
        print(f"  Branches: event_id, particle_id, truth_energy, energy_deposited, tracks_created, interactions, pos_x/y/z, dir_x/y/z")
        
        return filename
    
    def get_summary(self):
        """Get simulation summary"""
        if not self.results:
            return "No results available"
        
        total_energy = sum(r["energy_deposited_MeV"] for r in self.results)
        avg_energy = total_energy / len(self.results)
        
        summary = f"""
Simulation Summary:
  Total Events: {len(self.results)}
  Particle Type: {self.config.particle_type}
  Initial Energy: {self.config.particle_energy} MeV
  Total Energy Deposited: {total_energy:.4f} MeV
  Average Energy Deposited: {avg_energy:.4f} MeV
  Detector Material: {self.config.cube_material}
  Detector Size: {self.config.cube_size_x} x {self.config.cube_size_y} x {self.config.cube_size_z} cm³
"""
        return summary


def main():
    """Main entry point"""
    # Default configuration
    config = SimulationConfig()
    
    # Check for config file
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        with open(config_file, 'r') as f:
            config_data = json.load(f)
            config = SimulationConfig.from_dict(config_data)
    
    # Create and run simulation
    sim = Geant4Simulation(config)
    sim.initialize()
    sim.run()
    
    # Save and print results
    sim.save_results()
    print(sim.get_summary())


if __name__ == "__main__":
    main()
