"use client";

import { useState } from "react";
import { Search, Loader2, FileText } from "lucide-react";

interface SearchResult {
    chunk_id: string;
    note_id: string;
    note_title: string;
    content: string;
    score: number;
}

export default function SearchBar() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<SearchResult[]>([]);
    const [hasSearched, setHasSearched] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!query.trim()) return;

        setIsLoading(true);
        setHasSearched(true);
        try {
            const res = await fetch(`http://localhost:8000/api/v1/search/?q=${encodeURIComponent(query)}&limit=5`);
            const data = await res.json();
            setResults(data);
        } catch (error) {
            console.error("Search failed", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="w-full max-w-2xl mx-auto space-y-8">
            <form onSubmit={handleSearch} className="relative group">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    {isLoading ? (
                        <Loader2 className="h-5 w-5 text-muted-foreground animate-spin" />
                    ) : (
                        <Search className="h-5 w-5 text-muted-foreground group-focus-within:text-primary transition-colors" />
                    )}
                </div>
                <input
                    type="text"
                    className="block w-full pl-10 pr-3 py-4 border-2 border-border rounded-xl bg-background focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all shadow-sm"
                    placeholder="Ask your notes anything..."
                    value={query}
                    onChange={(e) => {
                        setQuery(e.target.value);
                        if (e.target.value === "") {
                            setHasSearched(false);
                            setResults([]);
                        }
                    }}
                />
            </form>

            <div className="space-y-4">
                {results.map((result) => (
                    <div key={result.chunk_id} className="p-6 rounded-xl border border-border bg-card hover:bg-secondary/20 transition-colors shadow-sm">
                        <div className="flex items-center gap-2 mb-2">
                            <FileText className="h-4 w-4 text-primary" />
                            <h3 className="font-semibold text-sm text-primary">{result.note_title}</h3>
                        </div>
                        <p className="text-muted-foreground text-sm leading-relaxed line-clamp-3">
                            {result.content}
                        </p>
                    </div>
                ))}

                {results.length === 0 && !isLoading && hasSearched && (
                    <div className="text-center text-muted-foreground py-8">
                        No related notes found.
                    </div>
                )}
            </div>
        </div>
    );
}
