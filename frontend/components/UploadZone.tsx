"use client";

import { useState, useCallback } from "react";
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

export default function UploadZone() {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback(async (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const files = Array.from(e.dataTransfer.files);
        if (files.length === 0) return;

        await uploadFiles(files);
    }, []);

    const handleFileSelect = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            const files = Array.from(e.target.files);
            await uploadFiles(files);
        }
    }, []);

    const uploadFiles = async (files: File[]) => {
        setIsUploading(true);
        setStatus("idle");

        try {
            console.log("Uploading files:", files);

            for (const file of files) {
                const formData = new FormData();
                formData.append("file", file);

                await fetch("http://localhost:8000/api/v1/notes/upload/", {
                    method: "POST",
                    body: formData,
                });
            }

            setStatus("success");
        } catch (error) {
            console.error("Upload failed", error);
            setStatus("error");
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div
            className={`relative flex flex-col items-center justify-center w-full max-w-2xl p-12 transition-all border-2 border-dashed rounded-xl cursor-pointer
        ${isDragging ? "border-primary bg-primary/5 scale-[1.02]" : "border-border hover:border-primary/50 hover:bg-secondary/50"}
        ${isUploading ? "opacity-50 pointer-events-none" : ""}
      `}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById("file-upload")?.click()}
        >
            <input
                id="file-upload"
                type="file"
                multiple
                className="hidden"
                onChange={handleFileSelect}
                accept=".md,.txt,.pdf"
            />

            <div className="flex flex-col items-center gap-4 text-center">
                <div className={`p-4 rounded-full transition-colors ${status === 'success' ? 'bg-green-100 dark:bg-green-900/30' : 'bg-secondary'}`}>
                    {status === 'success' ? (
                        <CheckCircle className="w-8 h-8 text-green-600 dark:text-green-400" />
                    ) : status === 'error' ? (
                        <AlertCircle className="w-8 h-8 text-red-600 dark:text-red-400" />
                    ) : isUploading ? (
                        <Loader2 className="w-8 h-8 animate-spin text-primary" />
                    ) : (
                        <Upload className="w-8 h-8 text-muted-foreground" />
                    )}
                </div>

                <div className="space-y-1">
                    <h3 className="text-lg font-semibold tracking-tight">
                        {isUploading ? "Uploading notes..." : "Upload your notes"}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                        Drag & drop Markdown, Text, or PDF files here
                    </p>
                </div>
            </div>
        </div>
    );
}
