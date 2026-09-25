import React, { useEffect, useState, useCallback } from "react";
import "./App.css";
import { api } from "./api";
import Header from "./components/Header";
import Hero from "./components/Hero";
import BurgerGrid from "./components/BurgerGrid";
import CartDrawer from "./components/CartDrawer";
import CheckoutForm from "./components/CheckoutForm";
import OrderConfirmation from "./components/OrderConfirmation";

export default function App() {
  const [burgers, setBurgers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [cart, setCart] = useState({}); // { [burgerId]: quantity }
  const [cartOpen, setCartOpen] = useState(false);
  const [checkoutOpen, setCheckoutOpen] = useState(false);
  const [confirmedOrder, setConfirmedOrder] = useState(null);
  const [placingOrder, setPlacingOrder] = useState(false);
  const [orderError, setOrderError] = useState(null);

  const loadBurgers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getBurgers();
      setBurgers(data);
    } catch (err) {
      setError("Couldn't load the menu. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadBurgers();
  }, [loadBurgers]);

  const addToCart = (burgerId) => {
    setCart((prev) => ({ ...prev, [burgerId]: (prev[burgerId] || 0) + 1 }));
  };

  const changeQuantity = (burgerId, delta) => {
    setCart((prev) => {
      const next = { ...prev };
      const qty = (next[burgerId] || 0) + delta;
      if (qty <= 0) {
        delete next[burgerId];
      } else {
        next[burgerId] = qty;
      }
      return next;
    });
  };

  const cartItems = Object.entries(cart)
    .map(([id, quantity]) => {
      const burger = burgers.find((b) => b.id === Number(id));
      return burger ? { burger, quantity } : null;
    })
    .filter(Boolean);

  const cartCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);
  const cartTotal = cartItems.reduce(
    (sum, item) => sum + item.quantity * Number(item.burger.price),
    0
  );

  const handlePlaceOrder = async (customerDetails) => {
    setPlacingOrder(true);
    setOrderError(null);
    try {
      const order = await api.createOrder({
        ...customerDetails,
        items: cartItems.map((item) => ({
          burger_id: item.burger.id,
          quantity: item.quantity,
        })),
      });
      setConfirmedOrder(order);
      setCart({});
      setCheckoutOpen(false);
      setCartOpen(false);
    } catch (err) {
      setOrderError(err.message || "Something went wrong placing your order.");
    } finally {
      setPlacingOrder(false);
    }
  };

  return (
    <div className="app">
      <Header cartCount={cartCount} onCartClick={() => setCartOpen(true)} />
      <Hero />

      <main className="menu-section" id="menu">
        <h2 className="menu-heading">Today&apos;s Menu</h2>
        {loading && <p className="status-text">Firing up the grill…</p>}
        {error && <p className="status-text error">{error}</p>}
        {!loading && !error && (
          <BurgerGrid burgers={burgers} onAdd={addToCart} />
        )}
      </main>

      <footer className="footer">
        <p>Burger House — flame-grilled, ordered online, no drive-thru required.</p>
      </footer>

      {cartOpen && (
        <CartDrawer
          items={cartItems}
          total={cartTotal}
          onClose={() => setCartOpen(false)}
          onChangeQuantity={changeQuantity}
          onCheckout={() => {
            setCartOpen(false);
            setCheckoutOpen(true);
          }}
        />
      )}

      {checkoutOpen && (
        <CheckoutForm
          items={cartItems}
          total={cartTotal}
          submitting={placingOrder}
          error={orderError}
          onClose={() => setCheckoutOpen(false)}
          onSubmit={handlePlaceOrder}
        />
      )}

      {confirmedOrder && (
        <OrderConfirmation
          order={confirmedOrder}
          onClose={() => setConfirmedOrder(null)}
        />
      )}
    </div>
  );
}
