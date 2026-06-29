import { useState, useEffect } from 'react';

export interface SavedChart {
  id: string; // usually name
  name: string;
  gender: string;
  date: string;
  time: string;
  latitude: string;
  longitude: string;
  locationName?: string;
  ayanamsa_type: string;
  timestamp: number;
}

const STORAGE_KEY = 'astro_naught_history';
const MAX_HISTORY = 30;

export function useChartHistory() {
  const [history, setHistory] = useState<SavedChart[]>([]);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        setHistory(JSON.parse(stored));
      }
    } catch (err) {
      console.error("Failed to load chart history", err);
    }
  }, []);

  const saveChart = (chart: Omit<SavedChart, 'id' | 'timestamp'>) => {
    setHistory(prev => {
      // Remove any existing chart with the same name to keep names unique
      const filtered = prev.filter(c => c.name.toLowerCase() !== chart.name.toLowerCase());
      
      const newChart: SavedChart = {
        ...chart,
        id: chart.name.toLowerCase(),
        timestamp: Date.now()
      };

      const updated = [newChart, ...filtered].slice(0, MAX_HISTORY);
      
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      } catch (err) {
        console.error("Failed to save chart history", err);
      }
      
      return updated;
    });
  };

  const removeChart = (id: string) => {
    setHistory(prev => {
      const updated = prev.filter(c => c.id !== id);
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      } catch (err) {
        console.error("Failed to save chart history", err);
      }
      return updated;
    });
  };

  return { history, saveChart, removeChart };
}
