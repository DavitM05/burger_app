import React from "react";

export default function Hero() {
  return (
    <section className="hero">
      <div className="hero-text">
        <h1>
          Stacked high.
          <br />
          Grilled hot.
          <br />
          Delivered fast.
        </h1>
        <p>
          Six burgers, one grill, zero shortcuts. Pick your stack and we'll
          have it fired up in minutes.
        </p>
        <a href="#menu" className="hero-cta">
          See the menu
        </a>
      </div>
      <div className="hero-mark" aria-hidden="true">
        🍔
      </div>
    </section>
  );
}
