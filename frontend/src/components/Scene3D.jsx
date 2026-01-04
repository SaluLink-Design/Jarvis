import React, { Suspense, useRef } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, Sky, PerspectiveCamera } from '@react-three/drei';
import { useJarvisStore } from '../store/jarvisStore';
import SceneObject from './SceneObject';

const Scene3D = () => {
  const { sceneData } = useJarvisStore();
  const controlsRef = useRef();

  return (
    <Canvas
      shadows
      gl={{ antialias: true }}
      className="w-full h-full"
    >
      {/* Camera */}
      <PerspectiveCamera makeDefault position={[10, 10, 10]} fov={60} />

      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <directionalLight
        position={[10, 10, 5]}
        intensity={1}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      <pointLight position={[-10, 5, -10]} intensity={0.5} />

      {/* Environment */}
      <Sky
        distance={450000}
        sunPosition={[0, 1, 0]}
        inclination={0.5}
        azimuth={0.25}
      />

      {/* Grid */}
      <Grid
        args={[100, 100]}
        cellSize={1}
        cellThickness={0.5}
        cellColor="#6b7280"
        sectionSize={10}
        sectionThickness={1}
        sectionColor="#4b5563"
        fadeDistance={50}
        fadeStrength={1}
        followCamera={false}
        infiniteGrid={true}
      />

      {/* Scene Objects */}
      <Suspense fallback={null}>
        {sceneData?.objects?.map((obj, index) => (
          <SceneObject key={obj.id || index} data={obj} />
        ))}
      </Suspense>

      {/* Controls */}
      <OrbitControls
        ref={controlsRef}
        enableDamping
        dampingFactor={0.05}
        minDistance={2}
        maxDistance={100}
        maxPolarAngle={Math.PI / 2}
      />
    </Canvas>
  );
};

export default Scene3D;

