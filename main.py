import Link from "next/link";
import { Sparkles, Upload, Wand2, Download, Star } from "lucide-react";

const FEATURES = [
  { icon: Upload, title: "Drag & Drop Upload", desc: "MP4, MOV, AVI, MKV up to 500MB — instant progress tracking." },
  { icon: Wand2, title: "AI Tamil → Tanglish", desc: "Whisper-powered transcription with natural, creator-style Tanglish conversion." },
  { icon: Sparkles, title: "Smart Caption Editor", desc: "Edit, merge, split, and style captions with real-time mobile preview." },
  { icon: Download, title: "Export Anywhere", desc: "SRT, VTT, TXT, or burn captions directly into your final MP4." },
];

const TESTIMONIALS = [
  { name: "Karthik R.", handle: "@karthikvlogs", quote: "Cut my captioning time from 2 hours to 5 minutes per Reel." },
  { name: "Priya S.", handle: "@priyacooks_ta", quote: "The Tanglish actually sounds like how I talk. No more robotic captions." },
  { name: "Arun M.", handle: "@arunshorts", quote: "Burned-in captions look so clean on Shorts. Engagement went up noticeably." },
];

export default function LandingPage() {
  return (
    <main className="overflow-hidden">
      {/* Nav */}
      <nav className="flex items-center justify-between px-6 md:px-12 py-5 max-w-7xl mx-auto">
        <div className="flex items-center gap-2 font-bold text-xl">
          <Sparkles className="text-primary-light" size={22} />
          <span>Tanglish Caption AI</span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm text-white/70">
          <Link href="/pricing" className="hover:text-white transition">Pricing</Link>
          <Link href="/contact" className="hover:text-white transition">Contact</Link>
          <Link href="/dashboard" className="hover:text-white transition">Dashboard</Link>
        </div>
        <Link href="/dashboard" className="btn-primary text-sm py-2.5 px-5">Get Started Free</Link>
      </nav>

      {/* Hero */}
      <section className="px-6 md:px-12 max-w-5xl mx-auto text-center pt-16 pb-24 animate-fade-in">
        <div className="inline-flex items-center gap-2 glass-card px-4 py-1.5 text-xs text-white/70 mb-6">
          <Sparkles size={14} className="text-accent" /> AI-Powered Tamil Caption Generator
        </div>
        <h1 className="text-4xl md:text-6xl font-extrabold leading-tight mb-6">
          Turn Tamil Speech into{" "}
          <span className="gradient-text">Tanglish Captions</span> in Minutes
        </h1>
        <p className="text-white/60 text-lg max-w-2xl mx-auto mb-10">
          Built for Instagram Reels, YouTube Shorts, and TikTok creators. Upload your video,
          get accurate Whisper-powered Tamil transcription, and natural, engagement-ready
          Tanglish captions — editable, styleable, and exportable instantly.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link href="/dashboard" className="btn-primary animate-glow">Upload Your First Video</Link>
          <Link href="/pricing" className="btn-ghost">See Pricing</Link>
        </div>
      </section>

      {/* Features */}
      <section className="px-6 md:px-12 max-w-7xl mx-auto pb-24">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {FEATURES.map((f) => (
            <div key={f.title} className="glass-card p-6 animate-slide-up hover:border-primary-light/40 transition">
              <f.icon className="text-primary-light mb-4" size={28} />
              <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
              <p className="text-white/60 text-sm">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Example conversion */}
      <section className="px-6 md:px-12 max-w-4xl mx-auto pb-24">
        <div className="glass-card p-8 md:p-10">
          <h2 className="text-2xl font-bold mb-6 text-center">See It In Action</h2>
          <div className="space-y-4">
            {[
              ["வணக்கம் நண்பர்களே", "Vanakkam Nanbargale"],
              ["எப்படி இருக்கீங்க", "Epdi Irukeenga"],
              ["இன்று ஒரு புதிய வீடியோ", "Inniku Oru Pudhiya Video"],
            ].map(([ta, tg]) => (
              <div key={ta} className="flex items-center justify-between bg-white/5 rounded-xl px-5 py-4">
                <span className="text-white/50">{ta}</span>
                <span className="text-accent font-medium">{tg}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="px-6 md:px-12 max-w-7xl mx-auto pb-24">
        <h2 className="text-2xl font-bold text-center mb-10">Loved by Tamil Creators</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {TESTIMONIALS.map((t) => (
            <div key={t.handle} className="glass-card p-6">
              <div className="flex gap-1 mb-3 text-accent">
                {Array.from({ length: 5 }).map((_, i) => <Star key={i} size={14} fill="currentColor" />)}
              </div>
              <p className="text-white/80 mb-4">"{t.quote}"</p>
              <p className="text-sm text-white/50">{t.name} · {t.handle}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="px-6 md:px-12 max-w-4xl mx-auto pb-24 text-center">
        <div className="glass-card p-12">
          <h2 className="text-3xl font-bold mb-4">Ready to caption your next video?</h2>
          <p className="text-white/60 mb-8">No credit card required for your first 3 videos.</p>
          <Link href="/dashboard" className="btn-primary">Start Captioning Free</Link>
        </div>
      </section>

      <footer className="px-6 md:px-12 py-8 text-center text-white/40 text-sm border-t border-white/5">
        © 2026 Tanglish Caption AI. All rights reserved.
      </footer>
    </main>
  );
}
