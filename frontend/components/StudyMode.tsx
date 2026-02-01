"use client";

import { useState } from "react";
import { Brain, RefreshCw, ChevronLeft, ChevronRight, Loader2 } from "lucide-react";

interface Flashcard {
    front: string;
    back: string;
}

export default function StudyMode() {
    const [cards, setCards] = useState<Flashcard[]>([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isFlipped, setIsFlipped] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [noteId, setNoteId] = useState(""); // TODO: Allow selecting a note specifically
    // For prototype, we might just pick the first available note or ask user for ID?
    // Let's list recent notes to pick from?
    // Or simpler: Just a "Generate from random note" button for now?
    // Let's assume we pass in a noteId or have a selector.
    // For this MVP, let's just input a Note ID manually or fetch recent notes.

    const [notes, setNotes] = useState<{ id: string, title: string }[]>([]);

    // Load notes on mount
    const loadNotes = async () => {
        try {
            const res = await fetch("http://localhost:8000/api/v1/notes/");
            const data = await res.json();
            setNotes(data);
            if (data.length > 0 && !noteId) setNoteId(data[0].id);
        } catch (e) { console.error(e) }
    };

    const generateCards = async () => {
        if (!noteId) return;
        setIsLoading(true);
        setCards([]);
        setCurrentIndex(0);
        setIsFlipped(false);

        try {
            const res = await fetch("http://localhost:8000/api/v1/study/flashcards", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ note_id: noteId, amount: 5 })
            });
            const data = await res.json();
            setCards(data.cards);
        } catch (error) {
            console.error("Failed to generate flashcards", error);
        } finally {
            setIsLoading(false);
        }
    };

    const nextCard = () => {
        setIsFlipped(false);
        setCurrentIndex((prev) => (prev + 1) % cards.length);
    };

    const prevCard = () => {
        setIsFlipped(false);
        setCurrentIndex((prev) => (prev - 1 + cards.length) % cards.length);
    };

    return (
        <div className="w-full max-w-2xl mx-auto space-y-8 flex flex-col items-center">
            {/* Controls */}
            <div className="flex gap-4 items-center w-full">
                <select
                    className="flex-1 p-3 rounded-lg border-2 border-black bg-black text-white focus:ring-4 focus:ring-black/20 focus:border-black outline-none font-bold"
                    value={noteId}
                    onClick={loadNotes}
                    onChange={(e) => setNoteId(e.target.value)}
                >
                    <option value="" disabled>Select a note to study</option>
                    {notes.map(n => <option key={n.id} value={n.id}>{n.title}</option>)}
                </select>

                <button
                    onClick={generateCards}
                    disabled={isLoading || !noteId}
                    className="px-6 py-3 bg-black text-primary rounded-lg font-black hover:scale-105 active:scale-95 disabled:opacity-50 disabled:pointer-events-none transition-all flex items-center gap-2 border-2 border-transparent hover:border-black/10 shadow-xl"
                >
                    {isLoading ? <Loader2 className="animate-spin" /> : <Brain />}
                    Generate Flashcards
                </button>
            </div>

            {/* Flashcard Area */}
            {cards.length > 0 && (
                <div className="w-full aspect-[3/2]" style={{ perspective: "1000px" }}>
                    <div
                        className={`relative w-full h-full duration-500 cursor-pointer transition-transform ${isFlipped ? "" : ""}`}
                        style={{
                            transformStyle: "preserve-3d",
                            transform: isFlipped ? "rotateY(180deg)" : "rotateY(0deg)"
                        }}
                        onClick={() => setIsFlipped(!isFlipped)}
                    >
                        {/* Front */}
                        <div
                            className="absolute inset-0 bg-black border-4 border-black/20 rounded-3xl flex items-center justify-center p-8 text-center shadow-2xl hover:border-black/40 transition-colors"
                            style={{ backfaceVisibility: "hidden" }}
                        >
                            <div>
                                <span className="text-xs uppercase tracking-widest text-zinc-500 mb-6 block font-bold">Question</span>
                                <h3 className="text-3xl font-black text-white mb-8 leading-tight">{cards[currentIndex].front}</h3>
                                <div className="absolute bottom-8 left-0 w-full text-center text-sm text-zinc-600 font-bold uppercase tracking-widest animate-pulse">
                                    Click to flip
                                </div>
                            </div>
                        </div>

                        {/* Back */}
                        <div
                            className="absolute inset-0 bg-white border-4 border-black rounded-3xl flex items-center justify-center p-8 text-center shadow-2xl"
                            style={{
                                backfaceVisibility: "hidden",
                                transform: "rotateY(180deg)"
                            }}
                        >
                            <div>
                                <span className="text-xs uppercase tracking-widest text-zinc-400 mb-6 block font-bold">Answer</span>
                                <p className="text-2xl font-bold text-black leading-relaxed">{cards[currentIndex].back}</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {cards.length > 0 && (
                <div className="flex items-center gap-8 text-black">
                    <button onClick={prevCard} className="p-4 bg-black/10 hover:bg-black/20 rounded-full transition-colors">
                        <ChevronLeft className="w-6 h-6" />
                    </button>
                    <span className="text-lg font-black tracking-widest">
                        {currentIndex + 1} / {cards.length}
                    </span>
                    <button onClick={nextCard} className="p-4 bg-black/10 hover:bg-black/20 rounded-full transition-colors">
                        <ChevronRight className="w-6 h-6" />
                    </button>
                </div>
            )}
        </div>
    );
}
