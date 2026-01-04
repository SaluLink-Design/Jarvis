"""
Physics Engine Module

Handles physics simulation for interactive 3D environments.
"""
from typing import Dict, Any, List, Optional
import numpy as np
from dataclasses import dataclass


@dataclass
class PhysicsBody:
    """Represents a physics body in the simulation"""
    id: str
    position: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray
    mass: float
    is_static: bool = False
    friction: float = 0.5
    restitution: float = 0.3  # bounciness
    

class PhysicsEngine:
    """
    Simple physics engine for 3D simulations
    
    Note: This is a simplified implementation. For production,
    integrate with Bullet, PhysX, or similar physics libraries.
    """
    
    def __init__(self, gravity: float = -9.81):
        self.gravity = np.array([0, gravity, 0])
        self.bodies: Dict[str, PhysicsBody] = {}
        self.time_step = 1.0 / 60.0  # 60 FPS
        self.damping = 0.98  # velocity damping
        
    def add_body(
        self,
        object_id: str,
        position: List[float],
        mass: float = 1.0,
        is_static: bool = False
    ) -> PhysicsBody:
        """Add a physics body to the simulation"""
        body = PhysicsBody(
            id=object_id,
            position=np.array(position, dtype=float),
            velocity=np.zeros(3),
            acceleration=np.zeros(3),
            mass=mass,
            is_static=is_static
        )
        self.bodies[object_id] = body
        return body
    
    def remove_body(self, object_id: str):
        """Remove a physics body from the simulation"""
        if object_id in self.bodies:
            del self.bodies[object_id]
    
    def apply_force(self, object_id: str, force: np.ndarray):
        """Apply a force to a body"""
        if object_id in self.bodies:
            body = self.bodies[object_id]
            if not body.is_static:
                body.acceleration += force / body.mass
    
    def apply_impulse(self, object_id: str, impulse: np.ndarray):
        """Apply an impulse (instant force) to a body"""
        if object_id in self.bodies:
            body = self.bodies[object_id]
            if not body.is_static:
                body.velocity += impulse / body.mass
    
    def step(self, dt: Optional[float] = None) -> Dict[str, Any]:
        """
        Advance the physics simulation by one time step
        
        Returns:
            Dictionary of updated positions and velocities
        """
        if dt is None:
            dt = self.time_step
        
        updates = {}
        
        for body_id, body in self.bodies.items():
            if body.is_static:
                continue
            
            # Apply gravity
            body.acceleration += self.gravity
            
            # Update velocity
            body.velocity += body.acceleration * dt
            
            # Apply damping
            body.velocity *= self.damping
            
            # Update position
            body.position += body.velocity * dt
            
            # Ground collision (simple)
            if body.position[1] < 0:
                body.position[1] = 0
                body.velocity[1] = -body.velocity[1] * body.restitution
                
                # Apply friction
                body.velocity[0] *= (1 - body.friction * dt)
                body.velocity[2] *= (1 - body.friction * dt)
            
            # Reset acceleration
            body.acceleration = np.zeros(3)
            
            # Store update
            updates[body_id] = {
                "position": body.position.tolist(),
                "velocity": body.velocity.tolist()
            }
        
        return updates
    
    def detect_collisions(self) -> List[Dict[str, Any]]:
        """
        Simple sphere-sphere collision detection
        
        Returns:
            List of collision events
        """
        collisions = []
        body_list = list(self.bodies.values())
        
        for i, body1 in enumerate(body_list):
            for body2 in body_list[i+1:]:
                # Simple distance-based collision
                distance = np.linalg.norm(body1.position - body2.position)
                collision_threshold = 2.0  # simplified radius
                
                if distance < collision_threshold:
                    collisions.append({
                        "body1": body1.id,
                        "body2": body2.id,
                        "point": ((body1.position + body2.position) / 2).tolist(),
                        "distance": float(distance)
                    })
        
        return collisions
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state of all physics bodies"""
        return {
            body_id: {
                "position": body.position.tolist(),
                "velocity": body.velocity.tolist(),
                "mass": body.mass,
                "is_static": body.is_static
            }
            for body_id, body in self.bodies.items()
        }
    
    def reset(self):
        """Reset the physics simulation"""
        self.bodies.clear()

