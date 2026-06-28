/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, MapPin, Calendar, Compass, Loader2 } from "lucide-react";

interface UserFormProps {
    onSubmit: (data: any) => void;
    isLoading: boolean;
}

export default function UserInputForm({ onSubmit, isLoading }: UserFormProps) {
    const [formData, setFormData] = useState({
        name: "",
        gender: "Male",
        date: "",
        time: "",
        latitude: "",
        longitude: "",
        ayanamsa_type: "lahiri"
    });

    const [locationSearch, setLocationSearch] = useState("");
    const [suggestions, setSuggestions] = useState<any[]>([]);
    const [isSearchingLocation, setIsSearchingLocation] = useState(false);
    const [locationError, setLocationError] = useState("");
    const [showSuggestions, setShowSuggestions] = useState(false);

    // Debounced location search
    useEffect(() => {
        const fetchLocations = async () => {
            if (locationSearch.trim().length < 3) {
                setSuggestions([]);
                return;
            }

            // If we already have coordinates and the search bar matches our selected location, do not search again
            if (formData.latitude && formData.longitude) {
                return;
            }

            setIsSearchingLocation(true);
            setLocationError("");

            try {
                const query = encodeURIComponent(locationSearch.trim());
                const res = await fetch(`https://nominatim.openstreetmap.org/search?city=${query}&format=json&addressdetails=1&limit=5&countrycodes=in`);

                if (!res.ok) throw new Error("Location API Error");

                const data = await res.json();
                setSuggestions(data);
                setShowSuggestions(true);

                if (data.length === 0) {
                    setLocationError("No locations found. Try being more specific.");
                }
            } catch (err) {
                setLocationError("Error connecting to Geocoding service.");
            } finally {
                setIsSearchingLocation(false);
            }
        };

        const timeoutId = setTimeout(() => {
            fetchLocations();
        }, 600); // 600ms debounce

        return () => clearTimeout(timeoutId);
    }, [locationSearch, formData.latitude, formData.longitude]);

    const handleSelectLocation = (place: any) => {
        setFormData(prev => ({
            ...prev,
            latitude: place.lat,
            longitude: place.lon
        }));
        // Format a slightly cleaner display name if possible
        const address = place.address || {};
        const city = address.city || address.town || address.village || address.county || "";
        const state = address.state || "";
        const postcode = address.postcode || "";
        const country = address.country || "";

        const cleanName = [city, state, postcode, country].filter(Boolean).join(", ");

        setLocationSearch(cleanName || place.display_name);
        setShowSuggestions(false);
        setSuggestions([]);
        setLocationError("");
    };

    const handleLocationChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setLocationSearch(e.target.value);
        // Reset coordinates if user starts typing again
        if (formData.latitude) {
            setFormData(prev => ({ ...prev, latitude: "", longitude: "" }));
        }
    };


    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!formData.date || !formData.time || !formData.latitude || !formData.longitude) {
            setLocationError("Please select a valid location from the dropdown suggestions.");
            return;
        }

        // Convert the input into a standard UTC Date object assuming the input is IST (+05:30)
        // Creating ISO string to parse local Indian time:
        const istOffsetString = "+05:30";
        const combinedDateTime = `${formData.date}T${formData.time}:00${istOffsetString}`;

        const utcDate = new Date(combinedDateTime);

        if (isNaN(utcDate.getTime())) {
            setLocationError("Invalid date or time provided.");
            return;
        }

        const payload = {
            name: formData.name || "Seeker",
            gender: formData.gender,
            year: utcDate.getUTCFullYear(),
            month: utcDate.getUTCMonth() + 1, // 0-indexed month
            day: utcDate.getUTCDate(),
            utc_hour: utcDate.getUTCHours(),
            utc_minute: utcDate.getUTCMinutes(),
            latitude: parseFloat(formData.latitude),
            longitude: parseFloat(formData.longitude),
            ayanamsa_type: formData.ayanamsa_type.toLowerCase()
        };

        onSubmit(payload);
    };

    return (
        <motion.form
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="w-full max-w-md p-8 rounded-xl bg-slate-900/50 backdrop-blur-xl border border-slate-800 shadow-2xl space-y-6"
            onSubmit={handleSubmit}
        >
            <div className="space-y-4">
                <div>
                    <label className="block text-xs font-semibold text-indigo-300 uppercase tracking-widest mb-1">Name</label>
                    <input
                        type="text"
                        required
                        className="w-full bg-slate-800/50 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-500/50 transition-all"
                        placeholder="Your Name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    />
                </div>

                <div>
                    <label className="block text-xs font-semibold text-indigo-300 uppercase tracking-widest mb-1">Gender</label>
                    <select
                        className="w-full bg-slate-800/50 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-amber-500/50 transition-all"
                        value={formData.gender}
                        onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                    >
                        <option>Male</option>
                        <option>Female</option>
                        <option>Other</option>
                    </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="block text-xs font-semibold text-indigo-300 uppercase tracking-widest mb-1 flex items-center gap-1"><Calendar className="w-3 h-3" /> Date</label>
                        <input
                            type="date"
                            required
                            className="w-full bg-slate-800/50 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-amber-500/50"
                            value={formData.date}
                            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-semibold text-indigo-300 uppercase tracking-widest mb-1 flex items-center gap-1"><Compass className="w-3 h-3" /> Time</label>
                        <input
                            type="time"
                            required
                            className="w-full bg-slate-800/50 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-amber-500/50"
                            value={formData.time}
                            onChange={(e) => setFormData({ ...formData, time: e.target.value })}
                        />
                    </div>
                </div>

                <div>
                    <label className="block text-xs font-semibold text-indigo-300 uppercase tracking-widest mb-1">Ayanamsa</label>
                    <select
                        className="w-full bg-slate-800/50 border border-slate-700 rounded-lg px-4 py-3 text-slate-100 focus:outline-none focus:ring-2 focus:ring-amber-500/50 transition-all font-medium"
                        value={formData.ayanamsa_type}
                        onChange={(e) => setFormData({ ...formData, ayanamsa_type: e.target.value })}
                    >
                        <option value="lahiri">Lahiri (Chitra Paksha)</option>
                        <option value="kp">KP (Krishnamurti Paddhati)</option>
                    </select>
                    {formData.ayanamsa_type === "kp" && (
                        <p className="mt-1 text-[10px] text-amber-500/80 leading-tight">
                            KP Ayanamsa uses the Placidus house system for precise sub-lord calculation.
                        </p>
                    )}
                </div>

                <div className="space-y-4 pt-2 border-t border-slate-700/50 relative">
                    <div>
                        <label className="block text-xs font-semibold text-indigo-300 uppercase tracking-widest mb-1 flex items-center justify-between">
                            <span className="flex items-center gap-1"><MapPin className="w-3 h-3" /> Birth City</span>
                            {isSearchingLocation && <Loader2 className="w-3 h-3 animate-spin text-amber-400" />}
                        </label>
                        <input
                            type="text"
                            required
                            className={`w-full bg-slate-800/50 border ${formData.latitude ? 'border-green-500/50 focus:ring-green-500/50' : 'border-slate-700 focus:ring-amber-500/50'} rounded-lg px-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 transition-all`}
                            placeholder="Start typing a city... (e.g. Bhopal)"
                            value={locationSearch}
                            onChange={handleLocationChange}
                        />
                        {/* Selected Location Confirmation Badge */}
                        {formData.latitude && !showSuggestions && (
                            <p className="text-green-400 text-xs mt-2 font-medium flex items-center gap-1">
                                ✓ Precise coordinates locked securely.
                            </p>
                        )}
                        {locationError && <p className="text-red-400 text-xs mt-2">{locationError}</p>}
                    </div>

                    {/* Autocomplete Dropdown */}
                    <AnimatePresence>
                        {showSuggestions && suggestions.length > 0 && (
                            <motion.ul
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                className="absolute z-50 w-full mt-1 bg-slate-800 border border-slate-700 rounded-lg shadow-xl overflow-hidden"
                            >
                                {suggestions.map((place, i) => (
                                    <li
                                        key={i}
                                        onClick={() => handleSelectLocation(place)}
                                        className="px-4 py-3 hover:bg-slate-700 cursor-pointer border-b border-slate-700/50 last:border-b-0"
                                    >
                                        <p className="text-sm font-medium text-slate-200">
                                            {place.address?.city || place.address?.town || place.address?.village || place.address?.state_district || place.name}
                                            {place.address?.postcode && <span className="ml-1 text-amber-400/70 text-xs">({place.address.postcode})</span>}
                                        </p>
                                        <p className="text-xs text-slate-400 truncate mt-0.5">
                                            {place.display_name}
                                        </p>
                                    </li>
                                ))}
                            </motion.ul>
                        )}
                    </AnimatePresence>
                </div>
            </div>

            <button
                type="submit"
                disabled={isLoading}
                className="w-full relative group overflow-hidden rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600 p-[1px] mt-4"
            >
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-500 to-purple-600 opacity-70 group-hover:opacity-100 blur transition-opacity duration-300"></div>
                <div className="relative flex items-center justify-center gap-2 bg-slate-900 px-8 py-4 rounded-lg transition-all duration-300 group-hover:bg-opacity-0">
                    <span className="font-bold text-white tracking-widest uppercase text-sm">
                        {isLoading ? "Consulting the Stars..." : "Generate Chart"}
                    </span>
                    {!isLoading && <Sparkles className="w-4 h-4 text-amber-300" />}
                </div>
            </button>
        </motion.form>
    );
}
