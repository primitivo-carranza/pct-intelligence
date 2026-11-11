# PCT Intelligence · Engineering Resources

Aplicación web en `index.html`, con registro de proyectos industriales, señales, competidores, clientes, oportunidades, fuentes y revisión semanal. Los registros privados se guardan **solo en localStorage** del navegador.

## Publicar

1. Revisar los archivos y poner el repositorio **público** en **Settings → General → Danger Zone → Change repository visibility**; publicar únicamente contenidos que puedan ser públicos.
2. Abrir **Settings → Pages**, seleccionar **GitHub Actions** en **Build and deployment** (el flujo `.github/workflows/deploy-pages.yml` ya existe).
3. URL prevista después del primer despliegue exitoso: https://primitivo-carranza.github.io/pct-intelligence/

## Agentes

Feed de solo lectura: `data/weekly-feed.json`. La publicación web por sí misma **no crea una ChatGPT Skill** ni una API de escritura. Para que un agente actualice información compartida se necesita un backend autenticado o commits automatizados a GitHub.

## Privacidad

No subir información comercial confidencial (contactos personales, ofertas, precios internos) a archivos públicos. Los registros introducidos en el navegador no se sincronizan entre dispositivos.

## Estado

Esta versión del repositorio es una **base web operativa** con entrada y exportación/importación JSON. El paquete original descargable en ChatGPT tiene otros componentes pendientes de incorporar al repositorio. No contiene aún el histórico completo de proyectos detectados.
