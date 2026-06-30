import { Check } from "lucide-react";

const PLANS = [
  { name: "Free", price: "$0", period: "/mo", features: ["3 videos / month", "Up to 5 min per video", "Tanglish captions", "SRT/VTT/TXT export"], cta: "Start Free" },
  { name: "Creator", price: "$15", period: "/mo", features: ["30 videos / month", "Up to 20 min per video", "AI punctuation & emoji", "Burned-in MP4 export", "Priority queue"], cta: "Go Creator", highlight: true },
  { name: "Pro", price: "$39", period: "/mo", features: ["Unlimited videos", "Up to 60 min per video", "Bulk export", "Team seats (3)", "API access"], cta: "Go Pro" },
];

export default function PricingPage() {
  return (
    <main className="max-w-6xl mx-auto px-6 py-16">
      <h1 className="text-3xl font-bold text-center mb-2">Simple, Creator-Friendly Pricing</h1>
      <p className="text-white/50 text-center mb-12">Cancel anytime. No hidden fees.</p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {PLANS.map((p) => (
          <div key={p.name} className={`glass-card p-8 ${p.highlight ? "border-primary-light ring-1 ring-primary/40" : ""}`}>
            <h2 className="font-semibold text-lg mb-1">{p.name}</h2>
            <p className="mb-6"><span className="text-3xl font-bold">{p.price}</span><span className="text-white/40">{p.period}</span></p>
            <ul className="space-y-3 mb-8">
              {p.features.map((f) => (
                <li key={f} className="flex items-center gap-2 text-sm text-white/70">
                  <Check size={16} className="text-accent" /> {f}
                </li>
              ))}
            </ul>
            <button className={p.highlight ? "btn-primary w-full" : "btn-ghost w-full"}>{p.cta}</button>
          </div>
        ))}
      </div>
    </main>
  );
}
