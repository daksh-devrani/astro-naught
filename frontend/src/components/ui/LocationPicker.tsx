import { useState, useEffect, useRef } from "react";
import { Search, MapPin, Edit3 } from "lucide-react";

interface LocationPickerProps {
  latitude: number;
  longitude: number;
  onChange: (lat: number, lon: number) => void;
  label?: string;
}

export default function LocationPicker({ latitude, longitude, onChange, label = "Birth Location" }: LocationPickerProps) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const [manualMode, setManualMode] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  useEffect(() => {
    const delayDebounceFn = setTimeout(async () => {
      if (query.length > 2 && !manualMode) {
        setIsSearching(true);
        try {
          const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&limit=5`);
          const data = await res.json();
          setResults(data);
          setShowDropdown(true);
        } catch (err) {
          console.error("Geocoding error", err);
        } finally {
          setIsSearching(false);
        }
      } else {
        setResults([]);
        setShowDropdown(false);
      }
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [query, manualMode]);

  const handleSelectLocation = (lat: string, lon: string, displayName: string) => {
    setQuery(displayName.split(",")[0]); // Set just the city name in the input
    onChange(parseFloat(lat), parseFloat(lon));
    setShowDropdown(false);
  };

  if (manualMode) {
    return (
      <div className="space-y-2 col-span-2 md:col-span-1 lg:col-span-2">
        <div className="flex justify-between items-center mb-1">
          <label className="block text-xs uppercase tracking-widest text-slate-400">{label} Coordinates</label>
          <button 
            type="button" 
            onClick={() => setManualMode(false)}
            className="text-[10px] text-indigo-400 hover:text-indigo-300 uppercase flex items-center gap-1"
          >
            <Search className="w-3 h-3" /> Search City Instead
          </button>
        </div>
        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-[10px] text-slate-500 mb-1">Latitude</label>
            <input 
              type="number" step="any" 
              value={latitude} 
              onChange={e => onChange(parseFloat(e.target.value), longitude)} 
              className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none text-sm" 
              required 
            />
          </div>
          <div>
            <label className="block text-[10px] text-slate-500 mb-1">Longitude</label>
            <input 
              type="number" step="any" 
              value={longitude} 
              onChange={e => onChange(latitude, parseFloat(e.target.value))} 
              className="w-full bg-slate-900/80 border border-slate-700 rounded-lg p-2 text-white focus:border-indigo-500 focus:outline-none text-sm" 
              required 
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative col-span-2 md:col-span-1 lg:col-span-2" ref={dropdownRef}>
      <div className="flex justify-between items-center mb-1">
        <label className="block text-xs uppercase tracking-widest text-slate-400">{label}</label>
        <button 
          type="button" 
          onClick={() => setManualMode(true)}
          className="text-[10px] text-indigo-400 hover:text-indigo-300 uppercase flex items-center gap-1"
        >
          <Edit3 className="w-3 h-3" /> Enter Lat/Lon
        </button>
      </div>
      
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <MapPin className="h-4 w-4 text-slate-500" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => { if (results.length > 0) setShowDropdown(true); }}
          className="w-full bg-slate-900/80 border border-slate-700 rounded-lg pl-10 p-2 text-white focus:border-indigo-500 focus:outline-none text-sm"
          placeholder="Search city (e.g., London, New York)"
        />
        {isSearching && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            <div className="w-4 h-4 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        )}
      </div>

      {/* Lat/Lon Hidden Inputs to ensure form submission still works if needed */}
      <input type="hidden" value={latitude} required />
      <input type="hidden" value={longitude} required />

      {/* Autocomplete Dropdown */}
      {showDropdown && results.length > 0 && (
        <div className="absolute z-50 w-full mt-1 bg-slate-800 border border-slate-700 rounded-lg shadow-xl max-h-60 overflow-y-auto">
          {results.map((result: any) => (
            <button
              key={result.place_id}
              type="button"
              onClick={() => handleSelectLocation(result.lat, result.lon, result.display_name)}
              className="w-full text-left px-4 py-3 hover:bg-slate-700 focus:bg-slate-700 transition-colors border-b border-slate-700/50 last:border-0 flex flex-col"
            >
              <span className="text-sm text-white font-medium">{result.name}</span>
              <span className="text-xs text-slate-400 truncate">{result.display_name}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
