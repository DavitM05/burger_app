import React from "react";

export default function OrderConfirmation({ order, onClose }) {
  return (
    <div className="overlay" onClick={onClose}>
      <div className="modal confirmation" onClick={(e) => e.stopPropagation()}>
        <h2>Order #{order.id} confirmed</h2>
        <p className="status-text">
          Thanks, {order.customer_name} — your order is {order.status}. We'll
          have it ready soon.
        </p>
        <ul className="checkout-summary">
          {order.items.map((item) => (
            <li key={item.id}>
              {item.quantity} × {item.burger?.name || `Burger #${item.burger_id}`}
              <span>${(item.quantity * Number(item.unit_price)).toFixed(2)}</span>
            </li>
          ))}
        </ul>
        <div className="cart-total">
          <span>Total</span>
          <span>${Number(order.total_price).toFixed(2)}</span>
        </div>
        <button className="checkout-button" onClick={onClose}>
          Back to menu
        </button>
      </div>
    </div>
  );
}
