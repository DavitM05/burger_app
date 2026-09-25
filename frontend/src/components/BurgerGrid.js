import React from "react";

function BurgerCard({ burger, onAdd }) {
  return (
    <article className="burger-card">
      <div className="burger-image-wrap">
        {burger.image_url ? (
          <img src={burger.image_url} alt={burger.name} loading="lazy" />
        ) : (
          <div className="burger-image-placeholder">🍔</div>
        )}
        <span className="burger-category">{burger.category}</span>
      </div>
      <div className="burger-info">
        <h3>{burger.name}</h3>
        <p className="burger-description">{burger.description}</p>
        <div className="burger-footer">
          <span className="burger-price">${Number(burger.price).toFixed(2)}</span>
          <button className="add-button" onClick={() => onAdd(burger.id)}>
            Add
          </button>
        </div>
      </div>
    </article>
  );
}

export default function BurgerGrid({ burgers, onAdd }) {
  if (burgers.length === 0) {
    return <p className="status-text">Nothing on the menu right now — check back soon.</p>;
  }
  return (
    <div className="burger-grid">
      {burgers.map((burger) => (
        <BurgerCard key={burger.id} burger={burger} onAdd={onAdd} />
      ))}
    </div>
  );
}
