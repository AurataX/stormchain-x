"use client";
import { useCallback, useEffect, useState } from "react";
import { call } from "./api";

export function useApi<T>(path: string | null, refresh = 0) {
  const [state, set] = useState<{ data: T | null; error: string | null; loading: boolean }>({
    data: null,
    error: null,
    loading: path !== null,
  });
  const [tick, setTick] = useState(0);
  useEffect(() => {
    if (!path) return;
    let live = true;
    set((old) => ({ ...old, loading: true, error: null }));
    call<T>(path)
      .then((data) => live && set({ data, error: null, loading: false }))
      .catch((error: Error) => live && set({ data: null, error: error.message, loading: false }));
    return () => {
      live = false;
    };
  }, [path, tick, refresh]);
  return { ...state, reload: useCallback(() => setTick((value) => value + 1), []) };
}
