import React, { useEffect, useState } from "react";
import loadingState from "../api/loadingState";
import GlobalLoader from "./GlobalLoader";

export function ApiLoadingProvider({ children }) {
  const [count, setCount] = useState(loadingState.getCount());

  useEffect(() => {
    const unsub = loadingState.subscribe((c) => setCount(c));
    return () => unsub();
  }, []);

  return (
    <>
      {children}
      {count > 0 && <GlobalLoader message="Đang tải dữ liệu..." />}
    </>
  );
}

export default ApiLoadingProvider;
