import type { Metadata } from "next";
import "./globals.css";
import HaloBackground from "./halo-background";

export const metadata: Metadata = {
  title: "CAPTOORA · Farmasi 31 OCT",
  description: "Mesa privada de selección, aprobación, contenido y reservas de la sesión Farmasi.",
  icons: { icon: "/favicon.svg" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="es-MX"><body><HaloBackground />{children}</body></html>;
}
