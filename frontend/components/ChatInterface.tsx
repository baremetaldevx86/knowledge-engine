"use client";

import { useState, useRef, useEffect } from "react";
import { Send, User, Bot, Loader2 } from "lucide-react";

interface Message {
    role: "user" | "assistant";
    content: string;
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([
        { role: "assistant", content: "Hello! I'm your Knowledge AI. Ask me anything about your notes." }
    ]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const sendMessage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput("");
        setMessages(prev => [...prev, { role: "user", content: userMessage }]);
        setIsLoading(true);

        try {
            const res = await fetch("http://localhost:8000/api/v1/chat/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: userMessage }),
            });

            if (!res.ok) {
                throw new Error("Failed to get response");
            }

            const data = await res.json();
            setMessages(prev => [...prev, { role: "assistant", content: data.answer }]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: "assistant", content: "Sorry, I encountered an error while processing your request." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[600px] w-full max-w-2xl mx-auto border border-border rounded-xl bg-card shadow-sm overflow-hidden">
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex items-start gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
                    >
                        <div className={`p-2 rounded-full shrink-0 ${msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"}`}>
                            {msg.role === "user" ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
                        </div>
                        <div
                            className={`p-3 rounded-lg max-w-[80%] text-sm leading-relaxed ${msg.role === "user"
                                ? "bg-primary text-primary-foreground rounded-tr-none"
                                : "bg-muted text-foreground rounded-tl-none whitespace-pre-wrap"
                                }`}
                        >
                            {msg.content}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex items-start gap-3">
                        <div className="p-2 rounded-full bg-muted shrink-0">
                            <Bot className="w-5 h-5" />
                        </div>
                        <div className="bg-muted p-3 rounded-lg rounded-tl-none flex items-center">
                            <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={sendMessage} className="p-4 border-t border-border bg-background flex gap-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question..."
                    className="flex-1 bg-secondary text-foreground px-4 py-2 rounded-lg focus:outline-none focus:ring-1 focus:ring-primary"
                />
                <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className="p-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
                >
                    <Send className="w-5 h-5" />
                </button>
            </form>
        </div>
    );
}
