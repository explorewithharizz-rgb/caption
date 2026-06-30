"use client";
import { useEffect, useState } from "react";
import axios from "axios";

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/admin/stats`).then((r) => setStats(r.data));
  }, []);

  if (!stats) return <p className="p-10 text-white/50">Loading admin stats...</p>;

  return (
    <main className="max-w-5xl mx-auto px-6 py-16">
      <h1 className="text-2xl font-bold mb-8">Admin Dashboard</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {Object.entries(stats).map(([k, v]) => (
          <div key={k} className="glass-card p-5">
            <p className="text-2xl font-bold">{v as any}</p>
            <p className="text-xs text-white/40 capitalize">{k.replace(/_/g, " ")}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
