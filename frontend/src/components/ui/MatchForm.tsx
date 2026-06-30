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
    date: "",
    time: "",
    latitude: 28.6139,
    longitude: 77.2090,
    gender: "Male",
  });

  const { primaryProfile } = useUser();

  useEffect(() => {
    if (primaryProfile) {
      setPersonA({
        name: primaryProfile.name || "Me",
        date: `${primaryProfile.year}-${String(primaryProfile.month).padStart(2, '0')}-${String(primaryProfile.day).padStart(2, '0')}`,
        time: `${String(primaryProfile.utc_hour).padStart(2, '0')}:${String(primaryProfile.utc_minute).padStart(2, '0')}`,
        latitude: primaryProfile.latitude,
        longitude: primaryProfile.longitude,
        gender: primaryProfile.gender || "Male",
      });
    }
  }, [primaryProfile]);

  const [personB, setPersonB] = useState({
    name: "",
    date: "",
    time: "",
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
    
    const getUtcDate = (dateStr: string, timeStr: string) => {
      if (!dateStr || !timeStr) return { y: 1990, mo: 1, d: 1, h: 12, m: 0 };
      const [year, month, day] = dateStr.split('-').map(Number);
      const [hour, min] = timeStr.split(':').map(Number);
      const d = new Date(Date.UTC(year, month - 1, day, hour, min));
      // IST is UTC + 5:30. To get UTC from IST, subtract 5.5 hours.
      d.setUTCHours(d.getUTCHours() - 5);
      d.setUTCMinutes(d.getUTCMinutes() - 30);
      return { 
        y: d.getUTCFullYear(), 
        mo: d.getUTCMonth() + 1, 
        d: d.getUTCDate(), 
        h: d.getUTCHours(), 
        m: d.getUTCMinutes() 
      };
    };

    const utc_a = getUtcDate(personA.date, personA.time);
    const utc_b = getUtcDate(personB.date, personB.time);

    onSubmit({
      person_a: {
        name: personA.name || "Person A",
        gender: personA.gender,
        year: sanitizeNum(utc_a.y, 1990),
        month: sanitizeNum(utc_a.mo, 1),
        day: sanitizeNum(utc_a.d, 1),
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
        year: sanitizeNum(utc_b.y, 1990),
        month: sanitizeNum(utc_b.mo, 1),
        day: sanitizeNum(utc_b.d, 1),
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
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-xs uppercase tracking-widest text-slate-400 mb-1">Date</label>
            <input type="date" value={person.date} onChange={e => setPerson({...person, date: e.target.value})} className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none" required />
          </div>
          <div>
            <label className="block text-xs uppercase tracking-widest text-slate-400 mb-1">Time (Local)</label>
            <input type="time" value={person.time} onChange={e => setPerson({...person, time: e.target.value})} className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none" required />
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
