# Sincronización del relevo

Ruta canónica: `ponchogf88/captoora`, rama `main`, carpeta `proyectos/farmasi-799`. La rama `farmasi/continuidad-edicion-799` también conserva el paquete operativo.
Después de cada lote/aprobación:
1. Actualizar estado/versión/decisión y lectura verificada de Drive en el expediente operativo. Ningún script puede deducir aprobaciones de otro chat.
2. Reconstruir registros con `preparar_respaldo.py --source /ruta/FARMASI_799 --dest /ruta/paquete`, y ejecutar los dos validadores. No genera fotos ni llama a API.
3. Mantener CONTINUAR, README, recetas y bitácora vigentes. Los estados antiguos solo viven en historial.
4. Crear un worktree limpio desde el main remoto actualizado. Copiar SOLO este paquete textual y los índices/documentación autorizados. No fusionar la rama antigua completa ni arrastrar cambios de web, campañas u otros proyectos.
5. Revisar diff, prohibir fotos/binarios/secretos/URLs de descarga temporales, commit y push normal sin fuerza. Si main cambió simultáneamente, integrar solo estos documentos sobre la nueva punta; no sobrescribir trabajo ajeno.
6. Verificar rama remota/commit, conteos, prompts y rutas accesibles. Un push iniciado no prueba sincronización. Replicar el paquete en la rama de continuidad si se sigue usando ese respaldo.

Abrir o validar estos documentos no reanuda la programación nocturna ni autoriza generación masiva, compras o cargos. El siguiente editor necesita acceso real a fuentes y una herramienta capaz de preservar sujetos antes de producir.
