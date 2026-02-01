"use client";

import { useEffect, useState, useRef } from "react";
import dynamic from "next/dynamic";
import { Loader2 } from "lucide-react";

// Dynamically import ForceGraph2D as it relies on window/canvas
const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), {
    ssr: false,
});

export default function KnowledgeGraph() {
    const [data, setData] = useState({ nodes: [], links: [] });
    const [isLoading, setIsLoading] = useState(true);
    const graphRef = useRef<any>(null);

    useEffect(() => {
        // Determine color based on system preference (simple check)
        // For now assume light mode or dark mode handling in graph config

        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        fetch(`${apiUrl}/api/v1/graph/`)
            .then((res) => res.json())
            .then((graphData) => {
                // Transform backend data to format expected by react-force-graph
                // Backend returns {nodes: [], edges: []}
                // react-force-graph expects {nodes: [], links: []}
                setData({
                    nodes: graphData.nodes,
                    links: graphData.edges
                });
            })
            .catch((err) => console.error("Failed to fetch graph", err))
            .finally(() => setIsLoading(false));
    }, []);

    return (
        <div className="w-full h-[500px] border border-border rounded-xl bg-card overflow-hidden relative">
            {isLoading && (
                <div className="absolute inset-0 flex items-center justify-center bg-card/80 z-10">
                    <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
            )}

            {!isLoading && data.nodes.length === 0 && (
                <div className="absolute inset-0 flex items-center justify-center text-muted-foreground z-10">
                    Not enough notes to link yet.
                </div>
            )}

            {/* Render graph only client-side */}
            <div className="w-full h-full">
                <ForceGraph2D
                    ref={graphRef}
                    graphData={data}
                    nodeLabel="label"
                    nodeColor={() => "#3b82f6"} // primary color (blue-500)
                    linkColor={() => "#94a3b8"} // slate-400
                    backgroundColor="rgba(0,0,0,0)" // Transparent to pick up card bg
                    width={700} // Approximate, ideally responsive wrapper
                    height={500}
                />
            </div>
        </div>
    );
}
