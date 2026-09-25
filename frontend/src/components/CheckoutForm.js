import React, { useState } from "react";

export default function CheckoutForm({ items, total, submitting, error, onClose, onSubmit }) {
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    onSubmit({
      customer_name: name.trim(),
      customer_phone: phone.trim() || null,
      delivery_address: address.trim() || null,
    });
  };

  return (
    <div className="overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="drawer-header">
          <h2>Checkout</h2>
          <button className="close-button" onClick={onClose} aria-label="Close checkout">
            ×
          </button>
        </div>

        <ul className="checkout-summary">
          {items.map(({ burger, quantity }) => (
            <li key={burger.id}>
              {quantity} × {burger.name}
              <span>${(quantity * Number(burger.price)).toFixed(2)}</span>
            </li>
          ))}
        </ul>
        <div className="cart-total">
          <span>Total</span>
          <span>${total.toFixed(2)}</span>
        </div>

        <form onSubmit={handleSubmit} className="checkout-form">
          <label>
            Name
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              placeholder="Your full name"
            />
          </label>
          <label>
            Phone
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="Optional"
            />
          </label>
          <label>
            Delivery address
            <input
              type="text"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              placeholder="Optional — leave blank for pickup"
            />
          </label>

          {error && <p className="status-text error">{error}</p>}

          <button type="submit" className="checkout-button" disabled={submitting}>
            {submitting ? "Placing order…" : "Place order"}
          </button>
        </form>
      </div>
    </div>
  );
}
