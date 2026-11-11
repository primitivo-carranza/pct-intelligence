# PCT Intelligence · Engineering Resources

Aplicación estática publicada en https://primitivo-carranza.github.io/pct-intelligence/ .

## Datos y sincronización

`data/weekly-feed.json` contiene investigación pública compartida. `sync.js` valida y fusiona proyectos, señales, actores, empresas prospectadas, oportunidades, fuentes y revisiones al abrir la aplicación o volver a la pestaña. Configuración permite actualizar manualmente.

Los registros manuales siguen en localStorage (`pct-intelligence-v1`), no se publican ni se sustituyen. Los registros públicos usan identificadores estables y se actualizan sin duplicarse. Al eliminar uno se conserva una marca local para que no reaparezca en la próxima consulta. La importación JSON fusiona registros y conserva una copia previa local; exportar periódicamente la copia completa.

## Actualización por agente

Actualizar el feed en la rama main mediante GitHub autenticado; el flujo de Pages publica cada cambio. Conservar IDs, registros previos, fuentes, fechas y separación entre proyectos confirmados e hipótesis comerciales. Ejecutar `node tests/sync.test.cjs` antes de publicar. No incluir contactos personales, correos, precios internos, notas de solvencia o estrategias privadas en este repositorio público.

La revisión y el email se ejecutan desde la tarea programada de Codex/ChatGPT, no desde JavaScript del navegador. Su estado se confirma en la tarea; esta web no realiza envíos de correo.

## Carga inicial y límites

La base pública incluye cuatro proyectos de obra en Alemania y cinco señales contrastadas en páginas de promotores y comunicados de contratistas. Las fechas históricas se distinguen de la fecha de comprobación. No representa el histórico completo de PCT.

Los datos históricos privados se importan localmente en Configuración y nunca se suben al repositorio. Las oportunidades son hipótesis de investigación, no licitaciones abiertas ni contratos. Los actores pueden ser clientes, socios o competidores según alcance.
