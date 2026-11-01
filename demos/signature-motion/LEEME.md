# Demo Captoora Signature

Página aislada. No toca `index.html` ni el sitio público.

El porqué del stack, lo que no hay que instalar y las reservas del iMac 2015 están en [docs/motion-stack/README.md](../../docs/motion-stack/README.md).

## Abrirla en la iMac

Hace falta Node 20 (la LTS que todavía publica binario para Mac Intel) y una terminal. macOS Monterey 12 es el techo oficial de esa iMac. Safari de Monterey alcanza. El Capitan, Sierra y High Sierra no son un objetivo de esta demo.

```bash
nvm install 20
nvm use 20
node -v

cd demos/signature-motion
npm install
npm start
```

Abre http://127.0.0.1:4173/

`npm start` compila `src/main.js` a `dist/demo.js` y levanta un servidor solo en esta carpeta. Hay que entrar por ese enlace: abrir el HTML con doble clic deja la foto en un origen nulo y WebGL no puede leerla.
