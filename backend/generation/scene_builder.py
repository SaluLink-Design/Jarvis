"""
Scene Builder Module

Constructs complete 3D environments and manages scene composition.
"""
from typing import Dict, Any, List
import random


class SceneBuilder:
    """
    Builds complete 3D scenes with environments, lighting, and composition
    """
    
    def __init__(self):
        self.environment_templates = {
            "basic": self._create_basic_environment,
            "forest": self._create_forest_environment,
            "city": self._create_city_environment,
            "interior": self._create_interior_environment,
            "studio": self._create_studio_environment
        }
    
    async def create_environment(self, env_type: str) -> Dict[str, Any]:
        """
        Create a complete environment
        
        Args:
            env_type: Type of environment (forest, city, interior, etc.)
            
        Returns:
            Environment configuration
        """
        if env_type in self.environment_templates:
            return self.environment_templates[env_type]()
        else:
            return self._create_basic_environment()
    
    def _create_basic_environment(self) -> Dict[str, Any]:
        """Create a basic empty environment with ground and sky"""
        return {
            "type": "basic",
            "ground": {
                "type": "plane",
                "size": 100,
                "color": "#808080",
                "texture": "grid"
            },
            "sky": {
                "type": "skybox",
                "color": "#87CEEB"
            },
            "lighting": self._create_lighting("studio"),
            "fog": None
        }
    
    def _create_forest_environment(self) -> Dict[str, Any]:
        """Create a forest environment"""
        return {
            "type": "forest",
            "ground": {
                "type": "terrain",
                "size": 200,
                "color": "#228B22",
                "texture": "grass",
                "height_variation": 5
            },
            "sky": {
                "type": "skybox",
                "color": "#87CEEB",
                "clouds": True
            },
            "lighting": self._create_lighting("morning"),
            "fog": {
                "color": "#e8f4f8",
                "near": 50,
                "far": 200
            },
            "vegetation": {
                "trees": self._generate_tree_positions(50),
                "grass": True,
                "rocks": True
            }
        }
    
    def _create_city_environment(self) -> Dict[str, Any]:
        """Create an urban environment"""
        return {
            "type": "city",
            "ground": {
                "type": "plane",
                "size": 500,
                "color": "#404040",
                "texture": "asphalt"
            },
            "sky": {
                "type": "skybox",
                "color": "#4a5f7f"
            },
            "lighting": self._create_lighting("noon"),
            "buildings": self._generate_building_grid(10, 10),
            "roads": True
        }
    
    def _create_interior_environment(self) -> Dict[str, Any]:
        """Create an interior room environment"""
        return {
            "type": "interior",
            "room": {
                "width": 10,
                "length": 10,
                "height": 3,
                "walls": {
                    "color": "#f5f5dc",
                    "texture": "paint"
                },
                "floor": {
                    "color": "#8B7355",
                    "texture": "wood"
                },
                "ceiling": {
                    "color": "#ffffff"
                }
            },
            "lighting": self._create_lighting("interior"),
            "windows": [
                {"position": [5, 1.5, -5], "size": [2, 1.5]}
            ]
        }
    
    def _create_studio_environment(self) -> Dict[str, Any]:
        """Create a studio lighting environment"""
        return {
            "type": "studio",
            "ground": {
                "type": "plane",
                "size": 50,
                "color": "#ffffff",
                "texture": "none"
            },
            "sky": {
                "type": "solid",
                "color": "#f0f0f0"
            },
            "lighting": self._create_lighting("studio"),
            "backdrop": {
                "type": "cyclorama",
                "color": "#ffffff"
            }
        }
    
    def _create_lighting(self, preset: str) -> Dict[str, Any]:
        """Create lighting configuration"""
        lighting_presets = {
            "studio": {
                "ambient": {
                    "color": "#ffffff",
                    "intensity": 0.5
                },
                "directional": [
                    {
                        "color": "#ffffff",
                        "intensity": 0.8,
                        "position": [10, 10, 10]
                    }
                ],
                "point": [
                    {
                        "color": "#ffffff",
                        "intensity": 0.5,
                        "position": [-10, 5, 5]
                    }
                ]
            },
            "morning": {
                "ambient": {
                    "color": "#ffd89b",
                    "intensity": 0.3
                },
                "directional": [
                    {
                        "color": "#ffe5b4",
                        "intensity": 0.7,
                        "position": [20, 10, 10]
                    }
                ]
            },
            "noon": {
                "ambient": {
                    "color": "#ffffff",
                    "intensity": 0.6
                },
                "directional": [
                    {
                        "color": "#ffffff",
                        "intensity": 1.0,
                        "position": [0, 50, 0]
                    }
                ]
            },
            "sunset": {
                "ambient": {
                    "color": "#ff7f50",
                    "intensity": 0.4
                },
                "directional": [
                    {
                        "color": "#ff6347",
                        "intensity": 0.8,
                        "position": [50, 5, 0]
                    }
                ]
            },
            "night": {
                "ambient": {
                    "color": "#1a1a2e",
                    "intensity": 0.1
                },
                "point": [
                    {
                        "color": "#fff5e1",
                        "intensity": 0.5,
                        "position": [0, 10, 0]
                    }
                ]
            },
            "interior": {
                "ambient": {
                    "color": "#fffaf0",
                    "intensity": 0.4
                },
                "point": [
                    {
                        "color": "#fffaf0",
                        "intensity": 0.8,
                        "position": [0, 2.5, 0]
                    }
                ]
            }
        }
        
        return lighting_presets.get(preset, lighting_presets["studio"])
    
    def _generate_tree_positions(self, count: int) -> List[Dict[str, Any]]:
        """Generate random tree positions for forest"""
        trees = []
        for _ in range(count):
            trees.append({
                "position": [
                    random.uniform(-90, 90),
                    0,
                    random.uniform(-90, 90)
                ],
                "scale": random.uniform(0.8, 1.5),
                "rotation": random.uniform(0, 360)
            })
        return trees
    
    def _generate_building_grid(self, rows: int, cols: int) -> List[Dict[str, Any]]:
        """Generate grid of buildings"""
        buildings = []
        spacing = 30
        
        for i in range(rows):
            for j in range(cols):
                height = random.uniform(10, 50)
                buildings.append({
                    "position": [
                        i * spacing - (rows * spacing / 2),
                        height / 2,
                        j * spacing - (cols * spacing / 2)
                    ],
                    "dimensions": {
                        "width": random.uniform(10, 20),
                        "height": height,
                        "depth": random.uniform(10, 20)
                    },
                    "color": f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
                })
        
        return buildings

