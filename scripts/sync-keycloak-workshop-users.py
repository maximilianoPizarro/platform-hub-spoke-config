#!/usr/bin/env python3
"""Create or reset user1..userN in Keycloak realm backstage (Developer Hub OIDC)."""
import json
import os
import ssl
import subprocess
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("KEYCLOAK_BASE_URL", "https://sso.apps.cluster-xqg4c.dynamic2.redhatworkshops.io")
REALM = "backstage"
PASSWORD = os.environ.get("WORKSHOP_PASSWORD", "Welcome123!")
USER_COUNT = int(os.environ.get("USER_COUNT", "50"))


def oc(*args: str) -> str:
    return subprocess.check_output(["oc", *args], text=True).strip()


def post_form(url: str, data: dict) -> dict:
    body = "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in data.items()).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())


def api(method: str, url: str, token: str, data=None):
    headers = {"Authorization": f"Bearer {token}"}
    body = None
    if data is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=CTX) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def main() -> int:
    import base64

    admin_user = base64.b64decode(
        oc("get", "secret", "keycloak-initial-admin", "-n", "keycloak", "-o", "jsonpath={.data.username}")
    ).decode()
    admin_pass = base64.b64decode(
        oc("get", "secret", "keycloak-initial-admin", "-n", "keycloak", "-o", "jsonpath={.data.password}")
    ).decode()

    token = post_form(
        f"{BASE}/realms/master/protocol/openid-connect/token",
        {
            "client_id": "admin-cli",
            "username": admin_user,
            "password": admin_pass,
            "grant_type": "password",
        },
    )["access_token"]

    _, raw = api("GET", f"{BASE}/admin/realms/{REALM}/users?max=500", token)
    existing = json.loads(raw)
    by_name = {u["username"]: u["id"] for u in existing}
    print(f"Existing users in {REALM}: {len(by_name)}")

    ok = 0
    for i in range(1, USER_COUNT + 1):
        uname = f"user{i}"
        if uname in by_name:
            st, _ = api(
                "PUT",
                f"{BASE}/admin/realms/{REALM}/users/{by_name[uname]}/reset-password",
                token,
                {"type": "password", "value": PASSWORD, "temporary": False},
            )
            if st == 204:
                ok += 1
            continue
        payload = {
            "username": uname,
            "enabled": True,
            "emailVerified": True,
            "firstName": "Workshop",
            "lastName": f"User {i}",
            "email": f"{uname}@developer-hub.local",
            "credentials": [{"type": "password", "value": PASSWORD, "temporary": False}],
            "realmRoles": ["developer"],
            "groups": ["developers"],
        }
        st, body = api("POST", f"{BASE}/admin/realms/{REALM}/users", token, payload)
        if st in (201, 204):
            ok += 1
        else:
            print(f"  {uname}: HTTP {st} {body[:120]!r}")

    print(f"Created/reset: {ok}/{USER_COUNT}")
    client_secret = base64.b64decode(
        oc(
            "get", "secret", "developer-hub-oidc-auth", "-n", "developer-hub",
            "-o", "jsonpath={.data.OIDC_CLIENT_SECRET}",
        )
    ).decode()
    test = post_form(
        f"{BASE}/realms/{REALM}/protocol/openid-connect/token",
        {
            "client_id": "developer-hub",
            "client_secret": client_secret,
            "username": "user1",
            "password": PASSWORD,
            "grant_type": "password",
        },
    )
    print("user1 OIDC test:", "OK" if test.get("access_token") else test)
    return 0 if test.get("access_token") else 1


if __name__ == "__main__":
    sys.exit(main())
