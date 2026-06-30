"use client";

import { useEffect, useState, use } from "react";
import axios from "axios";
import { Search, Scissors, Combine, Download, Flame, Type, AlignCenter } from "lucide-react";

interface Segment {
  id: string;
  start: number;
  end: number;
  tamil_text: string;
  tanglish_text: string;
  edited: boolean;
}

interface StyleConfig {
  fontFamily: string;
  fontSize: number;
  position: "top" | "center" | "bottom";
  bgOpacity: number;
  strokeWidth: number;
  animation: "fade" | "pop" | "slide" | "none";
}

const FONTS = ["Poppins", "Montserrat", "Anton", "Inter", "Bebas Neue"];
const ANIMATIONS = ["fade", "pop", "slide", "none"] as const;

function fmtTime(t: number) {
  const m = Math.floor(t / 60);
  const s = (t % 60).toFixed(1);
  return `${m}:${s.padStart(4, "0")}`;
}

export default function CaptionEditorPage({ params }: { params: Promise<{ projectId: string }> }) {
  const { projectId } = use(params);
  const [segments, setSegments] = useState<Segment[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [search, setSearch] = useState("");
  const [replace, setReplace] = useState("");
  const [style, setStyle] = useState<StyleConfig>({
    fontFamily: "Poppins", fontSize: 24, position: "bottom",
    bgOpacity: 0.6, strokeWidth: 2, animation: "fade",
  });

  useEffect(() => {
    axios
      .get(`${process.env.NEXT_PUBLIC_API_URL}/api/transcribe/segments/${projectId}`)
      .then((res) => setSegments(res.data))
      .catch(console.error);
  }, [projectId]);

  const updateSegment = async (id: string, text: string) => {
    setSegments((prev) => prev.map((s) => (s.id === id ? { ...s, tanglish_text: text, edited: true } : s)));
    await axios.patch(`${process.env.NEXT_PUBLIC_API_URL}/api/captions/segment/${id}`, { tanglish_text: text });
  };

  const toggleSelect = (id: string) =>
    setSelected((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));

  const mergeSelected = async () => {
    if (selected.length < 2) return;
    const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/captions/merge`, { segment_ids: selected });
    setSegments((prev) => {
      const kept = prev.filter((s) => !selected.includes(s.id) || s.id === res.data.id);
      return kept.map((s) => (s.id === res.data.id ? { ...s, tanglish_text: res.data.tanglish_text, end: res.data.end } : s));
    });
    setSelected([]);
  };

  const splitSegment = async (seg: Segment) => {
    const mid = Math.floor(seg.tanglish_text.length / 2);
    const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/captions/split`, {
      segment_id: seg.id, split_at_char: mid,
    });
    setSegments((prev) => {
      const idx = prev.findIndex((s) => s.id === seg.id);
      const updated = [...prev];
      updated[idx] = { ...seg, tanglish_text: res.data.first.text };
      updated.splice(idx + 1, 0, {
        id: res.data.second.id, start: seg.start, end: seg.end,
        tamil_text: "", tanglish_text: res.data.second.text, edited: true,
      });
      return updated;
    });
  };

  const runSearchReplace = async () => {
    if (!search) return;
    await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/captions/search-replace`, {
      project_id: projectId, search, replace,
    });
    setSegments((prev) => prev.map((s) => ({ ...s, tanglish_text: s.tanglish_text.split(search).join(replace) })));
  };

  const exportFile = (fmt: "srt" | "vtt" | "txt") => {
    window.open(`${process.env.NEXT_PUBLIC_API_URL}/api/export/${projectId}/${fmt}`, "_blank");
  };

  const burnCaptions = async () => {
    const res = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/api/export/${projectId}/burn`, { style });
    window.open(res.data.exported_video_url, "_blank");
  };

  return (
    <main className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Caption list */}
      <section className="lg:col-span-2">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-xl font-bold">Caption Editor</h1>
          <div className="flex gap-2">
            <button onClick={mergeSelected} disabled={selected.length < 2} className="btn-ghost text-xs py-2 px-3 flex items-center gap-1 disabled:opacity-30">
              <Combine size={14} /> Merge
            </button>
          </div>
        </div>

        {/* Search & replace */}
        <div className="glass-card p-4 mb-4 flex items-center gap-2">
          <Search size={16} className="text-white/40" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search Tanglish text..."
            className="bg-transparent flex-1 outline-none text-sm"
          />
          <input
            value={replace}
            onChange={(e) => setReplace(e.target.value)}
            placeholder="Replace with..."
            className="bg-transparent flex-1 outline-none text-sm border-l border-white/10 pl-3"
          />
          <button onClick={runSearchReplace} className="btn-ghost text-xs py-1.5 px-3">Replace All</button>
        </div>

        <div className="space-y-2 max-h-[65vh] overflow-y-auto pr-1">
          {segments.map((seg) => (
            <div
              key={seg.id}
              className={`glass-card p-4 flex gap-3 items-start transition ${selected.includes(seg.id) ? "border-primary-light" : ""}`}
            >
              <input
                type="checkbox"
                checked={selected.includes(seg.id)}
                onChange={() => toggleSelect(seg.id)}
                className="mt-1.5"
              />
              <div className="flex-1">
                <p className="text-xs text-white/40 mb-1">{fmtTime(seg.start)} → {fmtTime(seg.end)}</p>
                <textarea
                  value={seg.tanglish_text}
                  onChange={(e) => updateSegment(seg.id, e.target.value)}
                  rows={1}
                  className="bg-transparent w-full outline-none text-sm resize-none focus:bg-white/5 rounded px-2 py-1 -ml-2"
                />
                {seg.tamil_text && <p className="text-xs text-white/30 mt-1">{seg.tamil_text}</p>}
              </div>
              <button onClick={() => splitSegment(seg)} className="text-white/40 hover:text-white" title="Split">
                <Scissors size={14} />
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* Style + preview panel */}
      <aside className="space-y-6">
        <div className="glass-card p-5">
          <h2 className="font-semibold mb-4 flex items-center gap-2"><Type size={16}/> Subtitle Styling</h2>

          <label className="text-xs text-white/50">Font Family</label>
          <select
            value={style.fontFamily}
            onChange={(e) => setStyle({ ...style, fontFamily: e.target.value })}
            className="w-full bg-white/5 rounded-lg px-3 py-2 mt-1 mb-3 text-sm"
          >
            {FONTS.map((f) => <option key={f} value={f}>{f}</option>)}
          </select>

          <label className="text-xs text-white/50">Font Size: {style.fontSize}px</label>
          <input
            type="range" min={14} max={48} value={style.fontSize}
            onChange={(e) => setStyle({ ...style, fontSize: Number(e.target.value) })}
            className="w-full mb-3"
          />

          <label className="text-xs text-white/50 flex items-center gap-1"><AlignCenter size={12}/> Position</label>
          <div className="flex gap-2 mt-1 mb-3">
            {(["top", "center", "bottom"] as const).map((p) => (
              <button
                key={p}
                onClick={() => setStyle({ ...style, position: p })}
                className={`flex-1 py-1.5 rounded-lg text-xs capitalize ${style.position === p ? "bg-primary text-white" : "bg-white/5 text-white/60"}`}
              >
                {p}
              </button>
            ))}
          </div>

          <label className="text-xs text-white/50">Background Opacity: {Math.round(style.bgOpacity * 100)}%</label>
          <input
            type="range" min={0} max={1} step={0.05} value={style.bgOpacity}
            onChange={(e) => setStyle({ ...style, bgOpacity: Number(e.target.value) })}
            className="w-full mb-3"
          />

          <label className="text-xs text-white/50">Stroke Width: {style.strokeWidth}px</label>
          <input
            type="range" min={0} max={6} value={style.strokeWidth}
            onChange={(e) => setStyle({ ...style, strokeWidth: Number(e.target.value) })}
            className="w-full mb-3"
          />

          <label className="text-xs text-white/50">Animation Preset</label>
          <div className="flex gap-2 mt-1 flex-wrap">
            {ANIMATIONS.map((a) => (
              <button
                key={a}
                onClick={() => setStyle({ ...style, animation: a })}
                className={`px-3 py-1.5 rounded-lg text-xs capitalize ${style.animation === a ? "bg-primary text-white" : "bg-white/5 text-white/60"}`}
              >
                {a}
              </button>
            ))}
          </div>
        </div>

        {/* Mobile-first preview */}
        <div className="glass-card p-5">
          <h2 className="font-semibold mb-4">Mobile Preview</h2>
          <div className="relative mx-auto bg-black rounded-2xl overflow-hidden" style={{ width: 220, height: 390 }}>
            <div className="absolute inset-0 bg-gradient-to-br from-primary/30 to-accent/20" />
            <div
              className={`absolute left-0 right-0 px-3 flex justify-center ${
                style.position === "top" ? "top-6" : style.position === "center" ? "top-1/2 -translate-y-1/2" : "bottom-8"
              }`}
            >
              <span
                className="px-2 py-1 rounded text-white text-center animate-fade-in"
                style={{
                  fontFamily: style.fontFamily,
                  fontSize: style.fontSize * 0.55,
                  backgroundColor: `rgba(0,0,0,${style.bgOpacity})`,
                  WebkitTextStroke: `${style.strokeWidth * 0.5}px black`,
                }}
              >
                {segments[0]?.tanglish_text || "Vanakkam Nanbargale"}
              </span>
            </div>
          </div>
        </div>

        {/* Export */}
        <div className="glass-card p-5 space-y-2">
          <h2 className="font-semibold mb-2 flex items-center gap-2"><Download size={16}/> Export</h2>
          <button onClick={() => exportFile("srt")} className="btn-ghost w-full text-sm py-2">Download .SRT</button>
          <button onClick={() => exportFile("vtt")} className="btn-ghost w-full text-sm py-2">Download .VTT</button>
          <button onClick={() => exportFile("txt")} className="btn-ghost w-full text-sm py-2">Download .TXT</button>
          <button onClick={burnCaptions} className="btn-primary w-full text-sm py-2.5 flex items-center justify-center gap-2">
            <Flame size={16} /> Burn Captions into MP4
          </button>
        </div>
      </aside>
    </main>
  );
}
