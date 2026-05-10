import React from "react";

export function GlobalLoader({ message = "Đang tải..." }) {
  return (
    <div className="global-loading">
      <div className="global-loading-card">
        <div className="global-spinner" />
        <div className="global-loading-text">{message}</div>
      </div>
    </div>
  );
}

export default GlobalLoader;
