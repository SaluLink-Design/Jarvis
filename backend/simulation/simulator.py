"""
Main Simulator Module

Coordinates physics and behavioral simulations.
"""
from typing import Dict, Any, Optional
from .physics_engine import PhysicsEngine
from .behavior_engine import BehaviorEngine


class Simulator:
    """
    Main simulation coordinator that combines physics and behaviors
    """
    
    def __init__(self):
        self.physics_engine = PhysicsEngine()
        self.behavior_engine = BehaviorEngine()
        self.is_running = False
        self.simulation_time = 0.0
        
    def initialize(self, scene_data: Dict[str, Any]):
        """Initialize simulation from scene data"""
        # Add physics bodies for objects
        for obj in scene_data.get("objects", []):
            obj_id = obj.get("id")
            position = obj.get("position", [0, 0, 0])
            is_static = obj.get("is_static", False)
            mass = obj.get("mass", 1.0)
            
            self.physics_engine.add_body(
                obj_id,
                position,
                mass=mass,
                is_static=is_static
            )
        
        # Add agents for dynamic entities
        for agent_data in scene_data.get("agents", []):
            agent_id = agent_data.get("id")
            position = agent_data.get("position", [0, 0, 0])
            agent_type = agent_data.get("type", "generic")
            
            self.behavior_engine.add_agent(agent_id, position, agent_type)
    
    def start(self):
        """Start the simulation"""
        self.is_running = True
        
    def stop(self):
        """Stop the simulation"""
        self.is_running = False
    
    def step(self, dt: Optional[float] = None) -> Dict[str, Any]:
        """
        Advance simulation by one time step
        
        Returns:
            Updated simulation state
        """
        if not self.is_running:
            return self.get_state()
        
        if dt is None:
            dt = 1.0 / 60.0
        
        # Update physics
        physics_updates = self.physics_engine.step(dt)
        
        # Update behaviors
        behavior_updates = self.behavior_engine.step(dt)
        
        # Detect collisions
        collisions = self.physics_engine.detect_collisions()
        
        self.simulation_time += dt
        
        return {
            "time": self.simulation_time,
            "physics_updates": physics_updates,
            "behavior_updates": behavior_updates,
            "collisions": collisions
        }
    
    def apply_force(self, object_id: str, force: list):
        """Apply a force to an object"""
        import numpy as np
        self.physics_engine.apply_force(object_id, np.array(force))
    
    def command_agent(self, agent_id: str, command: str, params: Dict[str, Any]):
        """Send a command to an agent"""
        return self.behavior_engine.command_agent(agent_id, command, params)
    
    def add_object(self, object_data: Dict[str, Any]):
        """Add an object to the simulation"""
        obj_id = object_data.get("id")
        position = object_data.get("position", [0, 0, 0])
        is_static = object_data.get("is_static", False)
        mass = object_data.get("mass", 1.0)
        
        self.physics_engine.add_body(obj_id, position, mass=mass, is_static=is_static)
    
    def remove_object(self, object_id: str):
        """Remove an object from the simulation"""
        self.physics_engine.remove_body(object_id)
    
    def add_agent(self, agent_data: Dict[str, Any]):
        """Add an agent to the simulation"""
        agent_id = agent_data.get("id")
        position = agent_data.get("position", [0, 0, 0])
        agent_type = agent_data.get("type", "generic")
        
        self.behavior_engine.add_agent(agent_id, position, agent_type)
    
    def remove_agent(self, agent_id: str):
        """Remove an agent from the simulation"""
        self.behavior_engine.remove_agent(agent_id)
    
    def get_state(self) -> Dict[str, Any]:
        """Get current simulation state"""
        return {
            "time": self.simulation_time,
            "is_running": self.is_running,
            "physics": self.physics_engine.get_state(),
            "agents": self.behavior_engine.get_state()
        }
    
    def reset(self):
        """Reset the simulation"""
        self.physics_engine.reset()
        self.behavior_engine.reset()
        self.simulation_time = 0.0
        self.is_running = False

