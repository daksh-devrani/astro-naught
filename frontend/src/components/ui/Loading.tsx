"use client";

import { motion } from "framer-motion";

export function LoadingSpinner({ message = "Calculating Astrals..." }: { message?: string }) {
    return (
        <div className="flex flex-col items-center justify-center space-y-4 p-12">
            <div className="relative h-16 w-16">
                <motion.div
                    className="absolute inset-0 rounded-full border-b-2 border-r-2 border-amber-400"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                />
                <motion.div
                    className="absolute inset-2 rounded-full border-l-2 border-t-2 border-indigo-500"
                    animate={{ rotate: -360 }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                />
                <div className="absolute inset-0 flex items-center justify-center">
                    <div className="h-2 w-2 rounded-full bg-amber-200 animate-pulse" />
                </div>
            </div>
            <p className="text-sm font-medium tracking-widest text-indigo-300 animate-pulse">
                {message}
            </p>
        </div>
    );
}
