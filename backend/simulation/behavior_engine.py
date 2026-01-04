"""
Behavior Engine Module

Handles AI-driven behaviors for characters and objects in the simulation.
"""
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import random
import numpy as np


class BehaviorState(Enum):
    """Possible behavior states"""
    IDLE = "idle"
    MOVING = "moving"
    INTERACTING = "interacting"
    AVOIDING = "avoiding"


class Agent:
    """Represents an autonomous agent with behaviors"""
    
    def __init__(
        self,
        agent_id: str,
        position: List[float],
        agent_type: str = "generic"
    ):
        self.id = agent_id
        self.position = np.array(position, dtype=float)
        self.velocity = np.zeros(3)
        self.target_position: Optional[np.ndarray] = None
        self.state = BehaviorState.IDLE
        self.agent_type = agent_type
        self.speed = 1.0
        self.perception_radius = 5.0
        self.behaviors: List[Callable] = []
        
    def set_target(self, target: List[float]):
        """Set a target position to move towards"""
        self.target_position = np.array(target, dtype=float)
        self.state = BehaviorState.MOVING
    
    def update(self, dt: float, environment: Dict[str, Any]) -> Dict[str, Any]:
        """Update agent behavior"""
        # Execute behaviors
        for behavior in self.behaviors:
            behavior(self, environment, dt)
        
        # State-based logic
        if self.state == BehaviorState.MOVING and self.target_position is not None:
            self._move_towards_target(dt)
        
        return {
            "position": self.position.tolist(),
            "velocity": self.velocity.tolist(),
            "state": self.state.value
        }
    
    def _move_towards_target(self, dt: float):
        """Move towards the target position"""
        if self.target_position is None:
            return
        
        direction = self.target_position - self.position
        distance = np.linalg.norm(direction)
        
        if distance < 0.1:
            # Reached target
            self.state = BehaviorState.IDLE
            self.velocity = np.zeros(3)
            return
        
        # Normalize and apply speed
        direction = direction / distance
        self.velocity = direction * self.speed
        
        # Update position
        self.position += self.velocity * dt


class BehaviorEngine:
    """
    Manages AI behaviors for all agents in the simulation
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.environment_data: Dict[str, Any] = {}
        
    def add_agent(
        self,
        agent_id: str,
        position: List[float],
        agent_type: str = "generic"
    ) -> Agent:
        """Add an agent to the simulation"""
        agent = Agent(agent_id, position, agent_type)
        
        # Assign default behaviors based on type
        self._assign_default_behaviors(agent)
        
        self.agents[agent_id] = agent
        return agent
    
    def remove_agent(self, agent_id: str):
        """Remove an agent from the simulation"""
        if agent_id in self.agents:
            del self.agents[agent_id]
    
    def _assign_default_behaviors(self, agent: Agent):
        """Assign default behaviors based on agent type"""
        if agent.agent_type == "wanderer":
            agent.behaviors.append(self._wander_behavior)
        elif agent.agent_type == "follower":
            agent.behaviors.append(self._follow_behavior)
        elif agent.agent_type == "avoider":
            agent.behaviors.append(self._avoid_obstacles_behavior)
    
    def _wander_behavior(self, agent: Agent, environment: Dict, dt: float):
        """Random wandering behavior"""
        if agent.state == BehaviorState.IDLE:
            # Occasionally pick a new random target
            if random.random() < 0.01:  # 1% chance per frame
                new_target = agent.position + np.random.randn(3) * 5
                new_target[1] = 0  # Keep on ground
                agent.set_target(new_target.tolist())
    
    def _follow_behavior(self, agent: Agent, environment: Dict, dt: float):
        """Follow a target behavior"""
        # Find nearest target (simplified)
        targets = environment.get("targets", [])
        if targets and agent.state == BehaviorState.IDLE:
            target = targets[0]
            agent.set_target(target)
    
    def _avoid_obstacles_behavior(self, agent: Agent, environment: Dict, dt: float):
        """Avoid obstacles behavior"""
        obstacles = environment.get("obstacles", [])
        
        for obstacle in obstacles:
            obstacle_pos = np.array(obstacle["position"])
            distance = np.linalg.norm(agent.position - obstacle_pos)
            
            if distance < agent.perception_radius:
                # Steer away
                avoid_direction = agent.position - obstacle_pos
                avoid_direction = avoid_direction / np.linalg.norm(avoid_direction)
                agent.velocity += avoid_direction * 0.5
    
    def command_agent(self, agent_id: str, command: str, params: Dict[str, Any]):
        """Send a command to an agent"""
        if agent_id not in self.agents:
            return {"error": "Agent not found"}
        
        agent = self.agents[agent_id]
        
        if command == "move_to":
            target = params.get("target")
            if target:
                agent.set_target(target)
                return {"status": "moving", "target": target}
        
        elif command == "stop":
            agent.state = BehaviorState.IDLE
            agent.velocity = np.zeros(3)
            return {"status": "stopped"}
        
        elif command == "set_speed":
            speed = params.get("speed", 1.0)
            agent.speed = speed
            return {"status": "speed_updated", "speed": speed}
        
        return {"error": "Unknown command"}
    
    def update_environment(self, environment_data: Dict[str, Any]):
        """Update environment data that agents can perceive"""
        self.environment_data = environment_data
    
    def step(self, dt: float) -> Dict[str, Any]:
        """Update all agents"""
        updates = {}
        
        for agent_id, agent in self.agents.items():
            updates[agent_id] = agent.update(dt, self.environment_data)
        
        return updates
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state of all agents"""
        return {
            agent_id: {
                "position": agent.position.tolist(),
                "velocity": agent.velocity.tolist(),
                "state": agent.state.value,
                "type": agent.agent_type
            }
            for agent_id, agent in self.agents.items()
        }
    
    def reset(self):
        """Reset all agents"""
        self.agents.clear()
        self.environment_data.clear()

