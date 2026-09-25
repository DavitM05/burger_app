import React from "react";

export default function CartDrawer({ items, total, onClose, onChangeQuantity, onCheckout }) {
  return (
    <div className="overlay" onClick={onClose}>
      <aside className="drawer" onClick={(e) => e.stopPropagation()}>
        <div className="drawer-header">
          <h2>Your Order</h2>
          <button className="close-button" onClick={onClose} aria-label="Close cart">
            ×
          </button>
        </div>

        {items.length === 0 ? (
          <p className="status-text">Your cart is empty. Go grab a burger.</p>
        ) : (
          <>
            <ul className="cart-list">
              {items.map(({ burger, quantity }) => (
                <li key={burger.id} className="cart-item">
                  <div>
                    <p className="cart-item-name">{burger.name}</p>
                    <p className="cart-item-price">
                      ${Number(burger.price).toFixed(2)} each
                    </p>
                  </div>
                  <div className="qty-controls">
                    <button onClick={() => onChangeQuantity(burger.id, -1)}>−</button>
                    <span>{quantity}</span>
                    <button onClick={() => onChangeQuantity(burger.id, 1)}>+</button>
                  </div>
                </li>
              ))}
            </ul>
            <div className="cart-total">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>
            <button className="checkout-button" onClick={onCheckout}>
              Checkout
            </button>
          </>
        )}
      </aside>
    </div>
  );
}
