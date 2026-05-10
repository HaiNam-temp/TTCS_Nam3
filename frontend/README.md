Frontend React for PriceComp

Run local:
1. cd frontend
2. npm install
3. npm run dev

Environment:
- VITE_API_BASE_URL defaults to http://price-comp-alb-2137356393.ap-southeast-2.elb.amazonaws.com
- You can copy .env.example to .env and adjust endpoint.

Layered structure:
- src/app: application shell and route composition
- src/pages: page-level composition
- src/features: feature-specific state and flows
- src/shared: shared api client and reusable components
- src/styles: global styles
