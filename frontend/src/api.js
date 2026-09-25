// In production (docker-compose), nginx proxies /api to the backend service,
// so a relative path works both in dev (with the proxy below) and in prod.
const BASE_URL = process.env.REACT_APP_API_URL || "/api";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed with status ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  getBurgers: () => request("/burgers/?available_only=true"),
  createOrder: (order) =>
    request("/orders/", { method: "POST", body: JSON.stringify(order) }),
  getOrder: (id) => request(`/orders/${id}`),
};
