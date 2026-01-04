import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';

const SceneObject = ({ data }) => {
  const meshRef = useRef();

  // Subtle animation (optional)
  useFrame((state) => {
    if (meshRef.current && data.animate) {
      meshRef.current.rotation.y += 0.01;
    }
  });

  if (!data || !data.geometry) {
    return null;
  }

  const { geometry, material, position = [0, 0, 0], rotation = [0, 0, 0] } = data;

  // Parse geometry type
  const renderGeometry = () => {
    switch (geometry.type) {
      case 'BoxGeometry':
        return (
          <boxGeometry
            args={[
              geometry.parameters.width,
              geometry.parameters.height,
              geometry.parameters.depth
            ]}
          />
        );
      
      case 'SphereGeometry':
        return (
          <sphereGeometry
            args={[
              geometry.parameters.radius,
              geometry.parameters.widthSegments,
              geometry.parameters.heightSegments
            ]}
          />
        );
      
      case 'CylinderGeometry':
        return (
          <cylinderGeometry
            args={[
              geometry.parameters.radiusTop,
              geometry.parameters.radiusBottom,
              geometry.parameters.height,
              geometry.parameters.radialSegments
            ]}
          />
        );
      
      case 'ConeGeometry':
        return (
          <coneGeometry
            args={[
              geometry.parameters.radius,
              geometry.parameters.height,
              geometry.parameters.radialSegments
            ]}
          />
        );
      
      case 'PlaneGeometry':
        return (
          <planeGeometry
            args={[
              geometry.parameters.width,
              geometry.parameters.height
            ]}
          />
        );
      
      default:
        return <boxGeometry args={[1, 1, 1]} />;
    }
  };

  return (
    <mesh
      ref={meshRef}
      position={position}
      rotation={rotation}
      castShadow
      receiveShadow
    >
      {renderGeometry()}
      <meshStandardMaterial
        color={material?.color || '#808080'}
        metalness={material?.metalness || 0.3}
        roughness={material?.roughness || 0.7}
      />
    </mesh>
  );
};

export default SceneObject;

