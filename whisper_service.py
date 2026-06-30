"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import VideoUploader from "@/components/VideoUploader";
import { Clock, FileVideo, BarChart3, CreditCard } from "lucide-react";

interface ProjectRow {
  id: string;
  title: string;
  status: "queued" | "processing" | "completed" | "failed";
  video_url: string | null;
  created_at: string;
}

const STATUS_COLOR: Record<string, string> = {
  queued: "text-yellow-400 bg-yellow-400/10",
  processing: "text-accent bg-accent/10",
  completed: "text-green-400 bg-green-400/10",
  failed: "text-red-400 bg-red-400/10",
};

export default function DashboardPage() {
  const router = useRouter();
  const [projects, setProjects] = useState<ProjectRow[]>([]);
  const [usage, setUsage] = useState({ minutes_processed: 0, videos_processed: 0 });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [projRes, usageRes] = await Promise.all([
          axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/projects`),
          axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/projects/usage`),
        ]);
        setProjects(projRes.data);
        setUsage(usageRes.data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchData();
  }, []);

  return (
    <main className="max-w-6xl mx-auto px-6 py-10">
      <header className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <div className="flex gap-3 text-sm text-white/60">
          <a href="/profile" className="btn-ghost py-2 px-4">Profile</a>
          <a href="/pricing" className="btn-ghost py-2 px-4 flex items-center gap-1"><CreditCard size={16}/> Plan</a>
        </div>
      </header>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10">
        <div className="glass-card p-5 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-primary/15"><FileVideo className="text-primary-light" /></div>
          <div>
            <p className="text-2xl font-bold">{usage.videos_processed}</p>
            <p className="text-sm text-white/50">Videos processed</p>
          </div>
        </div>
        <div className="glass-card p-5 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-accent/15"><Clock className="text-accent" /></div>
          <div>
            <p className="text-2xl font-bold">{usage.minutes_processed.toFixed(1)}</p>
            <p className="text-sm text-white/50">Minutes transcribed this month</p>
          </div>
        </div>
        <div className="glass-card p-5 flex items-center gap-4">
          <div className="p-3 rounded-xl bg-pink-400/15"><BarChart3 className="text-accent-pink" /></div>
          <div>
            <p className="text-2xl font-bold">{projects.length}</p>
            <p className="text-sm text-white/50">Total projects</p>
          </div>
        </div>
      </div>

      {/* Upload */}
      <section className="mb-12">
        <h2 className="text-lg font-semibold mb-4">Upload a New Video</h2>
        <VideoUploader onUploaded={(id) => router.push(`/editor/${id}`)} />
      </section>

      {/* Project history */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Recent Uploads</h2>
        <div className="glass-card divide-y divide-white/5">
          {projects.length === 0 && (
            <p className="p-6 text-white/40 text-sm">No projects yet. Upload your first video above.</p>
          )}
          {projects.map((p) => (
            <button
              key={p.id}
              onClick={() => router.push(`/editor/${p.id}`)}
              className="w-full flex items-center justify-between p-5 hover:bg-white/5 transition text-left"
            >
              <div>
                <p className="font-medium">{p.title}</p>
                <p className="text-xs text-white/40">{new Date(p.created_at).toLocaleString()}</p>
              </div>
              <span className={`text-xs px-3 py-1 rounded-full font-medium ${STATUS_COLOR[p.status]}`}>
                {p.status}
              </span>
            </button>
          ))}
        </div>
      </section>
    </main>
  );
}
