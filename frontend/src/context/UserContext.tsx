"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";

interface Match {
  id: string;
  name: string;
  overall_score: number;
  report: any;
  personInfo: any;
  date_saved: string;
}

interface UserContextType {
  primaryProfile: any | null;
  setPrimaryProfile: (profile: any) => void;
  savedMatches: Match[];
  saveMatch: (match: Match) => void;
  removeMatch: (id: string) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [primaryProfile, setPrimaryProfileState] = useState<any | null>(null);
  const [savedMatches, setSavedMatchesState] = useState<Match[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const storedProfile = localStorage.getItem("astro_naught_profile");
      if (storedProfile) {
        setPrimaryProfileState(JSON.parse(storedProfile));
      }

      const storedMatches = localStorage.getItem("astro_naught_matches");
      if (storedMatches) {
        setSavedMatchesState(JSON.parse(storedMatches));
      }
    } catch (e) {
      console.error("Failed to parse local storage data", e);
    }
    setIsLoaded(true);
  }, []);

  const setPrimaryProfile = (profile: any) => {
    setPrimaryProfileState(profile);
    if (profile) {
      localStorage.setItem("astro_naught_profile", JSON.stringify(profile));
    } else {
      localStorage.removeItem("astro_naught_profile");
    }
  };

  const saveMatch = (match: Match) => {
    const updated = [...savedMatches, match];
    // Sort descending by score
    updated.sort((a, b) => b.overall_score - a.overall_score);
    setSavedMatchesState(updated);
    localStorage.setItem("astro_naught_matches", JSON.stringify(updated));
  };

  const removeMatch = (id: string) => {
    const updated = savedMatches.filter(m => m.id !== id);
    setSavedMatchesState(updated);
    localStorage.setItem("astro_naught_matches", JSON.stringify(updated));
  };

  if (!isLoaded) return null; // Avoid hydration mismatch

  return (
    <UserContext.Provider value={{ primaryProfile, setPrimaryProfile, savedMatches, saveMatch, removeMatch }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
}
