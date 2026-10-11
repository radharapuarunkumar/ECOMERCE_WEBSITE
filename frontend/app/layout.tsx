import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";
export const metadata: Metadata = { title: "NovaCart — Shop smarter", description: "NovaCart online shopping" };
export default function RootLayout({children}:{children:React.ReactNode}) { return <html lang="en"><body><header className="topbar"><Link className="brand" href="/">✦ Nova<span>Cart</span></Link><nav><Link href="/">Shop</Link><Link href="/orders">My orders</Link><Link href="/admin">Admin</Link><Link href="/cart" className="cart-link">Bag <span>↗</span></Link><Link href="/login" className="nav-login">Sign in</Link></nav></header><main>{children}</main><footer className="footer"><div className="brand">✦ Nova<span>Cart</span></div><p>Good finds. Great prices. A smarter way to shop.</p><small>Demo e-commerce project · Secure checkout integration required before real sales.</small></footer></body></html>; }
