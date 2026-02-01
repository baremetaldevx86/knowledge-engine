"use client";

import { useState } from "react";
import UploadZone from "@/components/UploadZone";
import SearchBar from "@/components/SearchBar";
import ChatInterface from "@/components/ChatInterface";
import KnowledgeGraph from "@/components/KnowledgeGraph";
import StudyMode from "@/components/StudyMode";
import { Upload, Search, MessageSquare, Share2, Brain } from "lucide-react";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"upload" | "search" | "chat" | "graph" | "study">("upload");

  return (
    <main className="flex min-h-screen flex-col items-center p-4 md:p-8 bg-black text-white selection:bg-primary selection:text-black font-sans">
      <div className="w-full max-w-7xl mx-auto space-y-8">

        {/* Header */}
        <header className="flex items-center justify-between py-4 border-b border-white/10">
          <div className="text-primary font-black text-3xl tracking-tighter select-none">
            $ KNOWLEDGE ENGINE
          </div>
          <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center animate-pulse">
            <div className="w-4 h-4 rounded-full bg-black" />
          </div>
        </header>

        {/* Hero / State Indicator */}
        <div className="py-8 text-center space-y-4">
          <h1 className="text-5xl md:text-7xl font-black tracking-tighter uppercase">
            {activeTab === 'upload' && "Inject Data"}
            {activeTab === 'search' && "Deep Search"}
            {activeTab === 'chat' && "Neural Chat"}
            {activeTab === 'graph' && "Network View"}
            {activeTab === 'study' && "Mastery Mode"}
          </h1>
          <p className="text-zinc-500 font-bold tracking-widest uppercase text-sm">
            System Status: <span className="text-primary">Online</span>
          </p>
        </div>

        {/* Tab Navigation */}
        <nav className="flex flex-wrap justify-center gap-2 md:gap-4 sticky top-4 z-50">
          {[
            { id: "upload", label: "Upload", icon: Upload },
            { id: "search", label: "Search", icon: Search },
            { id: "chat", label: "Chat", icon: MessageSquare },
            { id: "graph", label: "Graph", icon: Share2 },
            { id: "study", label: "Study", icon: Brain },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`
                px-6 py-3 rounded-full font-bold uppercase tracking-wider flex items-center gap-2 transition-all duration-300 border-2
                ${activeTab === tab.id
                  ? "bg-primary text-black border-primary shadow-[0_0_20px_rgba(0,214,50,0.5)] scale-105"
                  : "bg-balck text-zinc-500 border-zinc-800 hover:border-zinc-600 hover:text-white"
                }
              `}
            >
              <tab.icon className="w-4 h-4" />
              <span className="hidden md:inline">{tab.label}</span>
            </button>
          ))}
        </nav>

        {/* Main Content Area */}
        <div className="min-h-[600px] w-full bg-zinc-900/30 border border-white/5 rounded-3xl p-6 md:p-12 relative overflow-hidden ring-1 ring-white/5 shadow-2xl">

          {/* Background Decor */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-primary/5 rounded-full blur-[100px] -z-10" />
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-primary/5 rounded-full blur-[100px] -z-10" />

          {/* Views */}
          <div className="animate-in fade-in zoom-in-95 duration-300">
            {/* Upload Tab */}
            <div className={`${activeTab === 'upload' ? 'block' : 'hidden'} flex flex-col items-center justify-center h-full space-y-8`}>
              <div className="text-center max-w-lg mx-auto mb-8">
                <h2 className="text-2xl font-bold mb-2">Upload Knowledge</h2>
                <p className="text-zinc-400">Drag & drop your PDFs, Markdown, or Text files to instantly index them into the neural network.</p>
              </div>
              <UploadZone />
            </div>

            {/* Search Tab */}
            <div className={`${activeTab === 'search' ? 'block' : 'hidden'} max-w-3xl mx-auto space-y-8`}>
              <div className="text-center">
                <h2 className="text-3xl font-black mb-6 text-primary tracking-tight">SEMANTIC SEARCH</h2>
              </div>
              <SearchBar />
            </div>

            {/* Chat Tab */}
            <div className={`${activeTab === 'chat' ? 'block' : 'hidden'} h-[600px] flex flex-col`}>
              <div className="flex-1">
                <ChatInterface />
              </div>
            </div>

            {/* Graph Tab */}
            <div className={`${activeTab === 'graph' ? 'block' : 'hidden'} h-[600px] w-full bg-black rounded-xl overflow-hidden border border-white/10`}>
              <KnowledgeGraph />
            </div>

            {/* Study Tab */}
            <div className={`${activeTab === 'study' ? 'block' : 'hidden'} w-full`}>
              <StudyMode />
            </div>
          </div>

        </div>

      </div>
    </main>
  );
}
