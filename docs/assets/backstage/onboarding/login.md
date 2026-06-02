# Login guide

## Developer Hub (recommended entry)

1. Open `https://developer-hub.<hub-apps-domain>`
2. Sign in with **OIDC** (Keycloak).
3. Username: `userN` (e.g. `user1`) — same as Gitea.
4. Password: `Welcome123!` (demo default).

## OpenShift console (hub)

1. Open the hub cluster console URL.
2. Select identity provider **htpasswd_users** (or `htpasswd_users`).
3. User / password: `user1` / `Welcome123!`
4. Hub users have **cluster-reader** — you can view ACM, routes, and namespaces but not change cluster-scoped resources.

## Gitea

- URL: `https://gitea-gitea.<hub-apps-domain>`
- User: `user1` (your workshop id)
- Password: `Welcome123!`
- Your org: `ws-user1` (repos created by the scaffolder land here)

## DevSpaces (east or west)

DevSpaces runs **on the spoke** you selected in the template — not on the hub.

- East: `https://devspaces.<east-apps-domain>`
- West: `https://devspaces.<west-apps-domain>`
- Login: same `userN` / `Welcome123!` via cluster htpasswd on that spoke.

Use the **Open in DevSpaces** link on your catalog component so the correct spoke and Gitea repo are pre-filled.
