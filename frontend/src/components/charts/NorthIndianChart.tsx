"use client";

import React from "react";
import { motion } from "framer-motion";

interface PlanetInfo {
    name: string;
    degree?: number;
    isExalted?: boolean;
    isDebilitated?: boolean;
    isVargottama?: boolean;
    isPushkara?: boolean;
}

interface HouseData {
    houseNumber: number;
    rashiNumber: number; // 1-12
    planets: PlanetInfo[];
}

interface NorthIndianChartProps {
    houses: HouseData[]; // Must be an array of exactly 12 houses
    className?: string;
    title?: string;
}

export default function NorthIndianChart({ houses, className, title }: NorthIndianChartProps) {
    // SVG grid dimensions
    const s = 400; // side length of the square
    const cx = s / 2;
    const cy = s / 2;

    // Diamond / North Indian Chart specific lines
    // The outer box is (0,0) to (s,s)
    // Cross forming 4 inner diamonds
    const lines = [
        // Outer Border
        { x1: 0, y1: 0, x2: s, y2: 0 },
        { x1: s, y1: 0, x2: s, y2: s },
        { x1: s, y1: s, x2: 0, y2: s },
        { x1: 0, y1: s, x2: 0, y2: 0 },
        // Diagonals (Corner to Corner)
        { x1: 0, y1: 0, x2: s, y2: s },
        { x1: s, y1: 0, x2: 0, y2: s },
        // Inner diamond (Midpoint to Midpoint)
        { x1: cx, y1: 0, x2: s, y2: cy },
        { x1: s, y1: cy, x2: cx, y2: s },
        { x1: cx, y1: s, x2: 0, y2: cy },
        { x1: 0, y1: cy, x2: cx, y2: 0 },
    ];

    // Coordinates for the center of each of the 12 houses
    // In North Indian style, House 1 is always the top central diamond.
    // Then they go counter-clockwise.
    const housePositions = {
        1: { cx: 200, cy: 100 },
        2: { cx: 100, cy: 50 },
        3: { cx: 50, cy: 100 },
        4: { cx: 100, cy: 200 },
        5: { cx: 50, cy: 300 },
        6: { cx: 100, cy: 350 },
        7: { cx: 200, cy: 300 },
        8: { cx: 300, cy: 350 },
        9: { cx: 350, cy: 300 },
        10: { cx: 300, cy: 200 },
        11: { cx: 350, cy: 100 },
        12: { cx: 300, cy: 50 },
    };

    // Coordinates for the tiny Rashi numbers (placed in corners / edges of each house)
    const rashiNumberPositions = {
        1: { x: 200, y: 20 },
        2: { x: 100, y: 20 },
        3: { x: 20, y: 100 },
        4: { x: 30, y: 200 },
        5: { x: 20, y: 300 },
        6: { x: 100, y: 380 },
        7: { x: 200, y: 380 },
        8: { x: 300, y: 380 },
        9: { x: 380, y: 300 },
        10: { x: 370, y: 200 },
        11: { x: 380, y: 100 },
        12: { x: 300, y: 20 },
    };

    return (
        <div className={`relative flex flex-col items-center ${className}`}>
            {title && <h3 className="mb-4 text-xl font-medium tracking-widest text-amber-200/80">{title}</h3>}

            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, ease: "easeOut" }}
                className="relative shadow-2xl shadow-indigo-500/10 rounded-sm overflow-hidden"
            >
                <svg 
                    viewBox={`0 0 ${s} ${s}`} 
                    className="w-full h-auto aspect-square max-w-[400px] bg-slate-900/40 backdrop-blur-md"
                >
                    {/* Draw Grid Lines */}
                    {lines.map((line, idx) => (
                        <line
                            key={idx}
                            x1={line.x1}
                            y1={line.y1}
                            x2={line.x2}
                            y2={line.y2}
                            stroke="rgba(251, 191, 36, 0.4)" // Amber-400 with 40% opacity
                            strokeWidth="2"
                        />
                    ))}

                    {/* Render House Contents */}
                    {houses.map((house) => {
                        const pos = housePositions[house.houseNumber as keyof typeof housePositions];
                        const rashiPos = rashiNumberPositions[house.houseNumber as keyof typeof rashiNumberPositions];

                        if (!pos || !rashiPos) return null;

                        return (
                            <g key={`house-${house.houseNumber}`}>
                                {/* Rashi Number */}
                                <text
                                    x={rashiPos.x}
                                    y={rashiPos.y}
                                    textAnchor="middle"
                                    dominantBaseline="middle"
                                    className="fill-slate-500 text-xs font-semibold select-none"
                                >
                                    {house.rashiNumber}
                                </text>

                                {/* Planets */}
                                {house.planets.length > 0 && (
                                    <g>
                                        {house.planets.map((p, idx) => {
                                            // Vertically stack the planets around the center coordinate
                                            const yOffset = (idx - (house.planets.length - 1) / 2) * 14;
                                            const degStr = p.degree !== undefined ? `${Math.floor(p.degree)}°` : "";

                                            return (
                                                <text
                                                    key={p.name}
                                                    x={pos.cx}
                                                    y={pos.cy + yOffset}
                                                    textAnchor="middle"
                                                    dominantBaseline="middle"
                                                    className="fill-amber-100 text-xs font-medium tracking-wide drop-shadow-md"
                                                >
                                                    {p.name.substring(0, 2)} {degStr}
                                                    {p.isExalted && <tspan fill="#4ade80">↑</tspan>}
                                                    {p.isDebilitated && <tspan fill="#f87171">↓</tspan>}
                                                    {p.isVargottama && <tspan fill="#fcd34d">⭐</tspan>}
                                                    {p.isPushkara && <tspan fill="#f9a8d4">🌸</tspan>}
                                                </text>
                                            );
                                        })}
                                    </g>
                                )}
                            </g>
                        );
                    })}
                </svg>
            </motion.div>
        </div>
    );
}
