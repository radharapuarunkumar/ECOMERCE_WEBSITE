export const API = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api").replace(/\/$/, "");
export function token() { if (typeof window === "undefined") return ""; return localStorage.getItem("novacart_token") || ""; }
export async function api(path: string, options: RequestInit = {}) {
  const headers = new Headers(options.headers || {});
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const t = token(); if (t) headers.set("Authorization", `Bearer ${t}`);
  const response = await fetch(`${API}${path}`, { ...options, headers, cache: "no-store" });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || data.message || `Request failed (${response.status})`);
  return data;
}
export function money(value: number) { return new Intl.NumberFormat("en-IN", {style:"currency",currency:"INR",maximumFractionDigits:0}).format(value || 0); }
export type Product = {id:number; name:string; category:string; price:number; old_price:number; rating:number; image:string; description:string; stock:number; badge:string};
