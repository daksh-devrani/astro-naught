import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Users, Heart } from "lucide-react";
import { LoadingSpinner } from "./Loading";
import { useUser } from "@/context/UserContext";
import LocationPicker from "@/components/ui/LocationPicker";

interface MatchFormProps {
  onSubmit: (formData: any) => void;
  isLoading: boolean;
}

export default function MatchForm({ onSubmit, isLoading }: MatchFormProps) {
  const [personA, setPersonA] = useState({
    name: "",
    year: 1990,
    month: 1,
    day: 1,
    hour: 12,
    minute: 0,
    latitude: 28.6139,
    longitude: 77.2090,
    gender: "Male",
  });

  const { primaryProfile } = useUser();

  useEffect(() => {
    if (primaryProfile) {
      setPersonA({
        name: primaryProfile.name || "Me",
        year: primaryProfile.year,
        month: primaryProfile.month,
        day: primaryProfile.day,
        hour: primaryProfile.utc_hour,
        minute: primaryProfile.utc_minute,
        latitude: primaryProfile.latitude,
        longitude: primaryProfile.longitude,
        gender: primaryProfile.gender || "Male",
      });
    }
  }, [primaryProfile]);

  const [personB, setPersonB] = useState({
    name: "",
    year: 1990,
    month: 1,
    day: 1,
    hour: 12,
    minute: 0,
    latitude: 28.6139,
    longitude: 77.2090,
    gender: "Female",
  });

  const sanitizeNum = (val: any, fallback: number) => {
    const num = Number(val);
    return Number.isNaN(num) ? fallback : num;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // We assume IST (+05:30) like the rest of the app for now, but handle proper timezone 
    // conversion via standard Date object.
    const getUtcTime = (year: number, month: number, day: number, hour: number, min: number) => {
      const p_date = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      const p_time = `${String(hour).padStart(2, '0')}:${String(min).padStart(2, '0')}:00`;
      const localDate = new Date(`${p_date}T${p_time}+05:30`);
      return { h: localDate.getUTCHours(), m: localDate.getUTCMinutes() };
    };

    const utc_a = getUtcTime(personA.year, personA.month, personA.day, personA.hour, personA.minute);
    const utc_b = getUtcTime(personB.year, personB.month, personB.day, personB.hour, personB.minute);

    onSubmit({
      person_a: {
        name: personA.name || "Person A",
        gender: personA.gender,
        year: sanitizeNum(personA.year, 1990),
        month: sanitizeNum(personA.month, 1),
        day: sanitizeNum(personA.day, 1),
        utc_hour: sanitizeNum(utc_a.h, 12),
        utc_minute: sanitizeNum(utc_a.m, 0),
        latitude: sanitizeNum(personA.latitude, 28.6139),
        longitude: sanitizeNum(personA.longitude, 77.2090),
        ayanamsa_type: "kp",
        preferred_system: "kp"
      },
      person_b: {
        name: personB.name || "Person B",
        gender: personB.gender,
        year: sanitizeNum(personB.year, 1990),
        month: sanitizeNum(personB.month, 1),
        day: sanitizeNum(personB.day, 1),
        utc_hour: sanitizeNum(utc_b.h, 12),
        utc_minute: sanitizeNum(utc_b.m, 0),
        latitude: sanitizeNum(personB.latitude, 28.6139),
        longitude: sanitizeNum(personB.longitude, 77.2090),
        ayanamsa_type: "kp",
        preferred_system: "kp"
      }
    });
  };

  if (isLoading) {
    return <LoadingSpinner message="Calculating Synastry Alignment..." />;
  }

  const renderPersonForm = (person: any, setPerson: any, title: string, color: string, zIndexClass: string) => (
    <div className={`p-4 sm:p-6 rounded-2xl bg-black/40 border ${color} backdrop-blur-sm shadow-xl flex-1 relative ${zIndexClass}`}>
      <h3 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
        <Users className="w-5 h-5 text-indigo-400" /> {title}
      </h3>
      <div className="space-y-4">
        <div>
          <label className="block text-xs uppercase tracking-widest text-slate-400 mb-1">Name</label>
          <input type="text" value={person.name} onChange={e => setPerson({...person, name: e.target.value})} className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none" placeholder={`Enter ${title}'s Name`} required />
        </div>
        <div className="grid grid-cols-3 gap-2">
          <div>
            <label className="block text-xs uppercase tracking-widest text-slate-400 mb-1">DD</label>
            <input type="number" min="1" max="31" value={Number.isNaN(person.day) ? "" : person.day} onChange={e => setPerson({...person, day: parseInt(e.target.value)})} className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none" required />
          </div>
          <div>
            <label className="block text-xs uppercase tracking-widest text-slate-400 mb-1">MM</label>
            <input type="number" min="1" max="12" value={Number.isNaN(person.month) ? "" : person.month} onChange={e => setPerson({...person, month: parseInt(e.target.value)})} className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none" required />
          </div>
          <div>
            <label className="block text-xs uppercase tracking-widest text-slate-400 mb-1">YYYY</label>
            <input type="number" min="1900" max="2100" value={Number.isNaN(person.year) ? "" : person.year} onChange={e => setPerson({...person, year: parseInt(e.target.value)})} className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none" required />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-xs uppercase tracking-widest text-slate-400 mb-1">Hour (Local)</label>
            <input type="number" min="0" max="23" value={Number.isNaN(person.hour) ? "" : person.hour} onChange={e => setPerson({...person, hour: parseInt(e.target.value)})} className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none" required />
          </div>
          <div>
            <label className="block text-xs uppercase tracking-widest text-slate-400 mb-1">Minute</label>
            <input type="number" min="0" max="59" value={Number.isNaN(person.minute) ? "" : person.minute} onChange={e => setPerson({...person, minute: parseInt(e.target.value)})} className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none" required />
          </div>
        </div>
        
        {/* Location Picker */}
        <LocationPicker
          latitude={person.latitude}
          longitude={person.longitude}
          onChange={(lat, lon) => setPerson({...person, latitude: lat, longitude: lon})}
          label={`${title} Location`}
        />
      </div>
    </div>
  );

  return (
    <motion.form 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-5xl mx-auto space-y-8"
      onSubmit={handleSubmit}
    >
      <div className="text-center mb-8">
        <h2 className="text-3xl font-light text-white font-serif flex items-center justify-center gap-3">
          <Heart className="w-6 h-6 text-pink-500" />
          Synastry Engine
          <Heart className="w-6 h-6 text-pink-500" />
        </h2>
        <p className="text-slate-400 mt-2 text-sm uppercase tracking-widest">Deterministic Relationship Compatibility</p>
      </div>

      <div className="flex flex-col md:flex-row gap-6">
        {renderPersonForm(personA, setPersonA, "Partner 1", "border-indigo-500/20 hover:border-indigo-500/50", "z-50")}
        {renderPersonForm(personB, setPersonB, "Partner 2", "border-pink-500/20 hover:border-pink-500/50", "z-40")}
      </div>

      <div className="flex justify-center pt-8">
        <button type="submit" className="px-12 py-4 bg-gradient-to-r from-indigo-600 to-pink-600 text-white font-bold rounded-full shadow-[0_0_30px_rgba(99,102,241,0.3)] hover:shadow-[0_0_40px_rgba(236,72,153,0.4)] transition-all uppercase tracking-widest text-sm hover:scale-105 active:scale-95">
          Generate Match Report
        </button>
      </div>
    </motion.form>
  );
}
