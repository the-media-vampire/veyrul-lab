// Original study by Iris (Veyrul). MIT. Not executed or visually inspected.
import React, { useState } from 'react'
import { Canvas } from '@react-three/fiber'

const rest = '#65717c'
const accent = '#ffb14a'

export default function HoverStudy() {
  const [mode, setMode] = useState('local')
  const [active, setActive] = useState(null)
  const [preview, setPreview] = useState(false)
  const selected = preview ? 1 : active
  return (
    <main style={{ background: '#10151b', color: '#fff', padding: 24 }}>
      <h1>Which cube is responding?</h1>
      <label>Response scope: <select value={mode} onChange={e => setMode(e.target.value)}>
        <option value="local">A: local</option>
        <option value="global">B: global</option>
      </select></label>{' '}
      <label><input type="checkbox" checked={preview} onChange={e => setPreview(e.target.checked)} /> Preview middle hover</label>
      <div style={{ width: '100%', height: 420 }}>
        <Canvas camera={{ position: [0, 0, 9], fov: 40 }} dpr={1}>
          <color attach="background" args={['#10151b']} />
          <ambientLight intensity={0.8} />
          <directionalLight position={[3, 4, 5]} intensity={2} />
          {[-2, 0, 2].map((x, i) => (
            <mesh key={i} position={[x, 0, 0]} rotation={[0.25, 0.35, 0]}
              onPointerOver={e => { e.stopPropagation(); setActive(i) }}
              onPointerOut={() => setActive(null)}>
              <boxGeometry args={[1.2, 1.2, 1.2]} />
              <meshStandardMaterial roughness={0.8}
                color={selected !== null && (mode === 'global' || selected === i) ? accent : rest} />
            </mesh>
          ))}
        </Canvas>
      </div>
      <p>Hover a cube, or enable the middle-hover preview for matched stills.</p>
    </main>
  )
}