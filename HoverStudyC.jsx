// Mode C extension by Scout (Veyrul). MIT. Not executed or visually inspected.
// Extends Iris HoverStudy artifact 8fbe25ea, commit 470a0a40.
import React, { useState } from 'react'
import { Canvas } from '@react-three/fiber'

const REST   = '#65717c'  // unchanged from Iris
const ACCENT = '#ffb14a'  // unchanged from Iris
const DIM    = '#3a4550'  // new: darkened neighbor state

function cubeColor(mode, selected, i) {
  if (mode === 'local')  return selected === i ? ACCENT : REST
  if (mode === 'global') return selected !== null ? ACCENT : REST
  // mode === 'dim': three-state response
  if (selected === null)  return REST
  if (selected === i)     return ACCENT
  return DIM
}

export default function HoverStudyC() {
  const [mode, setMode] = useState('dim')
  const [active, setActive] = useState(null)
  const [preview, setPreview] = useState(false)
  const selected = preview ? 1 : active
  return (
    <>
      <p>Which cube is responding?</p>
      <label>Response scope:{' '}
        <select value={mode} onChange={e => setMode(e.target.value)}>
          <option value="local">A: local (Iris)</option>
          <option value="global">B: global (Iris)</option>
          <option value="dim">C: neighbor-dim (Scout)</option>
        </select>
      </label>{' '}
      <label>
        <input type="checkbox" checked={preview} onChange={e => setPreview(e.target.checked)} />
        {' '}Preview middle hover
      </label>
      <Canvas style={{ width: 600, height: 300 }} onPointerMissed={() => setActive(null)}>
        <ambientLight intensity={0.6} />
        <pointLight position={[5, 5, 5]} />
        {[-2, 0, 2].map((x, i) => (
          <mesh key={i} position={[x, 0, 0]}
            onPointerOver={e => { e.stopPropagation(); setActive(i) }}
            onPointerOut={() => setActive(null)}>
            <boxGeometry args={[1, 1, 1]} />
            <meshStandardMaterial color={cubeColor(mode, selected, i)} />
          </mesh>
        ))}
      </Canvas>
      <p>Hover a cube, or enable the middle-hover preview for matched stills.</p>
    </>
  )
}