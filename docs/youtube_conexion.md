# Conectar tu canal de YouTube (una sola vez, ~10 minutos)

La agencia publica en tu canal con la **API oficial de YouTube**. Google exige que el dueño
del canal autorice el acceso; nadie más puede hacerlo por ti. Nunca pegues estas claves en un chat.

## 1. Proyecto en Google Cloud
1. Entra a https://console.cloud.google.com con la cuenta de Google dueña del canal y crea un proyecto (p. ej. "Agencia YouTube").
2. En **APIs y servicios → Biblioteca**, habilita **YouTube Data API v3** y **YouTube Analytics API**.

## 2. Pantalla de consentimiento
3. En **Google Auth Platform** (o "Pantalla de consentimiento de OAuth"): tipo **Externo**, nombre de la app y tu correo.
4. En **Público**, agrega tu correo como usuario de prueba.
5. **Importante:** cuando termines, pulsa **Publicar app** (pasarla a "En producción"). En modo "Prueba" el permiso
   caduca cada 7 días. Para uso propio no necesitas verificación de Google; solo verás un aviso de "app no verificada"
   al autorizar, que puedes aceptar porque la app es tuya.

## 3. Credenciales
6. En **Credenciales → Crear credenciales → ID de cliente de OAuth**, tipo **Aplicación web**.
7. En **URI de redireccionamiento autorizados** agrega: `https://developers.google.com/oauthplayground`
8. Guarda el **ID de cliente** y el **Secreto de cliente**.

## 4. Obtener el token de acceso (sin programar)
9. Abre https://developers.google.com/oauthplayground
10. Engranaje (arriba a la derecha) → marca **Use your own OAuth credentials** → pega tu ID y secreto.
11. En "Step 1", en la caja de texto, pega estos permisos separados por espacio y pulsa **Authorize APIs**:
    `https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.force-ssl https://www.googleapis.com/auth/yt-analytics.readonly`
12. Inicia sesión y **elige el canal** correcto (si tienes varios o una cuenta de marca).
13. En "Step 2", pulsa **Exchange authorization code for tokens** y copia el **Refresh token**.

## 5. Guardarlo en el entorno de Claude (no en el chat)
14. En la sesión de Claude Code: menú del entorno en la barra de título → **Editar** → variables de entorno. Agrega:
    - `YT_CLIENT_ID` = ID de cliente
    - `YT_CLIENT_SECRET` = secreto de cliente
    - `YT_REFRESH_TOKEN` = refresh token
15. Abre una sesión nueva (las variables se cargan al iniciar). Verifica con: `python -m ugc_agency yt-estado`

Para revocar el acceso cuando quieras: https://myaccount.google.com/permissions
