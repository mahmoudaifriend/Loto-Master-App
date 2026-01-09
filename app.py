// =====================================================
// TOTOLOTO ALGORITMIA – Lotofácil Engine (PRO+)
// Hot/Cold Logic + Copy Caixa + Circular Engine (25 balls)
// =====================================================

import React, { useEffect, useState } from "react";

// =====================================================
// CONFIG – LOTOFÁCIL
// =====================================================
const NUMBERS = Array.from({ length: 25 }, (_, i) => i + 1);
const DRAW_DAYS = [2, 4, 6]; // Terça, Quinta, Sábado

// =====================================================
// API – Último sorteio oficial (Caixa)
// =====================================================
async function fetchLastDraw() {
  try {
    const res = await fetch("https://loteriascaixa-api.herokuapp.com/api/lotofacil/latest");
    const data = await res.json();
    return data.dezenas.map(n => parseInt(n, 10));
  } catch {
    return null;
  }
}

// =====================================================
// UTILS
// =====================================================
function getNextDrawCountdown() {
  const now = new Date();
  if ([0, 1].includes(now.getDay())) return null;
  let next = new Date(now);
  while (!DRAW_DAYS.includes(next.getDay())) next.setDate(next.getDate() + 1);
  next.setHours(20, 0, 0, 0);
  const diff = next.getTime() - now.getTime();
  return diff > 0 ? diff : null;
}

function formatTime(ms) {
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  const s = Math.floor((ms % 60000) / 1000);
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

function shuffle(arr) {
  return [...arr].sort(() => Math.random() - 0.5);
}

function countHits(bet, draw) {
  return bet.filter(n => n !== -1 && draw.includes(n)).length;
}

// =====================================================
// HOT / COLD ENGINE (sem revelar o truque)
// =====================================================
function buildWeights(lastDraw) {
  const weights = {};
  NUMBERS.forEach(n => {
    let w = 1;
    if (lastDraw?.includes(n)) w += 0.6; // quente
    if (n % 2 === 0) w += 0.1; // equilíbrio par/impar
    if ([1, 5, 10, 15, 20, 25].includes(n)) w += 0.1; // distribuição visual
    weights[n] = w;
  });
  return weights;
}

function weightedPick(count, weights) {
  const pool = [];
  Object.entries(weights).forEach(([n, w]) => {
    for (let i = 0; i < Math.floor(w * 10); i++) pool.push(Number(n));
  });
  return shuffle(pool).filter((v, i, a) => a.indexOf(v) === i).slice(0, count);
}

// =====================================================
// COMPONENTS
// =====================================================

function Countdown() {
  const [time, setTime] = useState(null);
  useEffect(() => {
    const t = setInterval(() => setTime(getNextDrawCountdown()), 1000);
    return () => clearInterval(t);
  }, []);
  return <div className="text-center text-yellow-400 mb-2">{time ? formatTime(time) : "Aguardando próximo ciclo"}</div>;
}

function CircularEngine({ active }) {
  return (
    <div className="relative w-72 h-72 mx-auto my-6">
      <div className={`absolute inset-0 rounded-full border-4 border-purple-600 ${active ? "animate-spin" : "animate-spin-slow"}`} />
      {NUMBERS.map((n, i) => {
        const angle = (i / 25) * 2 * Math.PI;
        const x = 120 + 100 * Math.cos(angle);
        const y = 120 + 100 * Math.sin(angle);
        return (
          <div
            key={n}
            style={{ left: x, top: y }}
            className="absolute w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold"
          >
            <span className="bg-gradient-to-br from-purple-500 to-yellow-400 text-black w-full h-full rounded-full flex items-center justify-center">
              {String(n).padStart(2, "0")}
            </span>
          </div>
        );
      })}
    </div>
  );
}

function ModeSelector({ mode, setMode }) {
  return (
    <div className="grid grid-cols-2 gap-4">
      <button onClick={() => setMode("individual")} className={`p-3 rounded-xl ${mode === "individual" ? "bg-purple-700" : "bg-gray-800"}`}>Individual</button>
      <button onClick={() => setMode("bolao")} className={`p-3 rounded-xl ${mode === "bolao" ? "bg-purple-700" : "bg-gray-800"}`}>Bolão</button>
    </div>
  );
}

function Results({ bets }) {
  return (
    <div className="space-y-2">
      {bets.map((bet, i) => (
        <div key={i} className="flex flex-wrap gap-1">
          {bet.map((n, idx) => (
            <span key={idx} className="w-7 h-7 rounded-full bg-purple-800 flex items-center justify-center text-xs">
              {n === -1 ? "X" : String(n).padStart(2, "0")}
            </span>
          ))}
        </div>
      ))}
    </div>
  );
}

function SocialProof({ bets, lastDraw }) {
  if (!lastDraw) return null;
  const stats = { 11: 0, 12: 0, 13: 0, 14: 0 };
  bets.forEach(b => {
    const h = countHits(b, lastDraw);
    if (stats[h] !== undefined) stats[h]++;
  });

  return (
    <div className="mt-6 p-4 rounded-2xl bg-black/50 border border-purple-700">
      <h3 className="text-yellow-400 mb-3">Comparação com último sorteio</h3>
      {stats[14] > 0 && <div className="p-3 bg-yellow-400 text-black rounded-xl font-bold animate-pulse">🔥 {stats[14]} apostas fariam 14 pontos</div>}
      {stats[13] > 0 && <div className="p-3 mt-2 bg-purple-600 rounded-xl font-semibold">⭐ {stats[13]} apostas fariam 13 pontos</div>}
      {[11, 12].map(k => stats[k] > 0 && <div key={k} className="text-sm opacity-80 mt-1">{stats[k]} apostas fariam {k} pontos</div>)}
    </div>
  );
}

function CopyCaixa({ bets }) {
  function copy() {
    const text = bets
      .map(b => b.filter(n => n !== -1).map(n => String(n).padStart(2, "0")).join(" "))
      .join("\n");
    navigator.clipboard.writeText(text);
    alert("Apostas copiadas para envio na Caixa");
  }

  return (
    <button onClick={copy} className="w-full mt-4 p-3 bg-green-500 text-black rounded-xl font-bold">
      Copiar para Caixa
    </button>
  );
}

// =====================================================
// MAIN APP
// =====================================================
export default function App() {
  const [mode, setMode] = useState(null);
  const [volume, setVolume] = useState(100);
  const [closure, setClosure] = useState(15);
  const [bets, setBets] = useState([]);
  const [lastDraw, setLastDraw] = useState(null);
  const [filter, setFilter] = useState(20);
  const [simulating, setSimulating] = useState(false);

  useEffect(() => {
    fetchLastDraw().then(setLastDraw);
  }, []);

  function simulate() {
    const weights = buildWeights(lastDraw);
    setSimulating(true);
    const gen = [];

    for (let i = 0; i < volume; i++) {
      if (mode === "individual") {
        gen.push([...weightedPick(14, weights), -1]);
      } else {
        gen.push(weightedPick(closure, weights));
      }
    }

    setTimeout(() => {
      setBets(gen);
      setSimulating(false);
    }, 2000);
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-900 to-black text-white p-4">
      <Countdown />
      <CircularEngine active={simulating} />
      <ModeSelector mode={mode} setMode={setMode} />

      <div className="mt-4">
        <label>Fechamento: {closure}</label>
        <input type="range" min={15} max={20} value={closure} onChange={e => setClosure(+e.target.value)} className="w-full" />
      </div>

      <div className="mt-4">
        <label>Volume</label>
        <select value={volume} onChange={e => setVolume(+e.target.value)} className="w-full bg-black border p-2">
          <option value={50}>1–100</option>
          <option value={500}>100–1000</option>
          <option value={2000}>1000–10000</option>
        </select>
      </div>

      <button onClick={simulate} className="w-full mt-6 p-4 bg-yellow-500 text-black rounded-xl font-bold">SIMULAR</button>

      {bets.length > 0 && (
        <div className="mt-6">
          <Results bets={bets.slice(0, filter)} />
          <div className="mt-3">
            <label>Filtrar apostas quentes: {filter}</label>
            <input type="range" min={1} max={100} value={filter} onChange={e => setFilter(+e.target.value)} className="w-full" />
          </div>
          <CopyCaixa bets={bets.slice(0, filter)} />
          <SocialProof bets={bets} lastDraw={lastDraw} />
        </div>
      )}
    </div>
  );
}

// =====================================================
// Tailwind extra:
// .animate-spin-slow { animation: spin 14s linear infinite }
// =====================================================
