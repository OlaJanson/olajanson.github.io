# Komodoro — körning & Spotify-setup

Fristående prototyp (vanilla HTML/JS, ingen backend). Speglar produktionsvägarna
`olajanson.se/komodoro` + `/callback`.

## Köra lokalt
```sh
cd olajanson.github.io && python3 -m http.server 8090
```
Öppna **http://127.0.0.1:8090/komodoro/** (använd `127.0.0.1`, INTE `localhost`).

## Spotify-app
- Client ID: `146c72f11c944dd0a26999ffea7ef350`
- Redirect URI som måste vara registrerad: `http://127.0.0.1:8090/callback`
- Scopes: `user-library-read streaming user-read-email user-read-private`

## Fällor vi gick på (löste 2026-06-28)
1. **`localhost` är bannlyst** i nya Spotify-redirect-URIs — måste vara `127.0.0.1`.
   (Gamla `localhost:8080` var grandfathered men porten togs av Obsidians TaskNotes-API.)
2. **Save-knappen** i Spotify-dashboardens Edit Settings — "Add" stagear bara, inget
   persisteras förrän man scrollar ner och klickar gröna Save. Mismatch fram tills dess.
3. **Web Playback SDK kräver `user-read-email` + `user-read-private`** utöver `streaming`,
   annars `authentication_error` strax efter "ready".
4. **Konsekvent origin** — starta login och ta emot callback på SAMMA host (127.0.0.1),
   annars hittas inte PKCE-verifiern i localStorage.
5. Uppspelning kräver **Spotify Premium**.

`?selftest` på komodoro-sidan kör pass-algoritmens assertions i konsolen.
