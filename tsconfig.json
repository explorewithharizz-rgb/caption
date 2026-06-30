"use client";
import { useState } from "react";

export default function ContactPage() {
  const [sent, setSent] = useState(false);
  return (
    <main className="max-w-xl mx-auto px-6 py-16">
      <h1 className="text-3xl font-bold mb-2">Contact Us</h1>
      <p className="text-white/50 mb-8">Questions, feedback, or partnership ideas — we'd love to hear from you.</p>
      {sent ? (
        <div className="glass-card p-8 text-center text-accent">Thanks! We'll get back to you within 24 hours.</div>
      ) : (
        <form onSubmit={(e) => { e.preventDefault(); setSent(true); }} className="glass-card p-8 space-y-4">
          <input required placeholder="Your name" className="w-full bg-white/5 rounded-lg px-4 py-3 text-sm outline-none" />
          <input required type="email" placeholder="Email" className="w-full bg-white/5 rounded-lg px-4 py-3 text-sm outline-none" />
          <textarea required placeholder="Message" rows={5} className="w-full bg-white/5 rounded-lg px-4 py-3 text-sm outline-none" />
          <button className="btn-primary w-full">Send Message</button>
        </form>
      )}
    </main>
  );
}
