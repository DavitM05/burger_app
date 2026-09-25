import React from "react";

export default function Header({ cartCount, onCartClick }) {
  return (
    <header className="site-header">
      <div className="logo">
        Burger<span>House</span>
      </div>
      <nav className="header-actions">
        <a href="#menu" className="nav-link">
          Menu
        </a>
        <button className="cart-button" onClick={onCartClick}>
          Cart
          {cartCount > 0 && <span className="cart-count">{cartCount}</span>}
        </button>
      </nav>
    </header>
  );
}
