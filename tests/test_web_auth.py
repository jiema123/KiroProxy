import unittest
import importlib
import os
from unittest.mock import patch

from fastapi.testclient import TestClient

import kiro_proxy.api_auth as api_auth
import kiro_proxy.env_config as env_config
import kiro_proxy.web.auth as web_auth
from kiro_proxy.main import app


class WebAuthTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def _reload_auth_config(self):
        importlib.reload(env_config)
        importlib.reload(api_auth)
        importlib.reload(web_auth)

    def test_root_requires_login_by_default(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("KiroProxy Login", response.text)
        self.assertIn("username", response.text)

    def test_api_requires_login_by_default(self):
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Authentication required")

    def test_security_config_requires_login(self):
        response = self.client.get("/api/security-config")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Authentication required")

    def test_v1_endpoints_are_not_blocked_by_web_login(self):
        response = self.client.get(
            "/v1/models",
            headers={"Authorization": "Bearer sk-any"},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["object"], "list")

    def test_v1_endpoints_require_api_key(self):
        response = self.client.get("/v1/models")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Invalid API key")

    def test_v1_endpoints_reject_wrong_api_key(self):
        response = self.client.get(
            "/v1/models",
            headers={"Authorization": "Bearer wrong-key"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Invalid API key")

    def test_v1_endpoints_accept_configured_api_key(self):
        with patch.dict("os.environ", {"KIROPROXY_API_KEY": "secret-123"}):
            self._reload_auth_config()
            response = self.client.get(
                "/v1/models",
                headers={"Authorization": "Bearer secret-123"},
            )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["object"], "list")
        self._reload_auth_config()

    def test_login_sets_session_cookie_and_allows_api_access(self):
        response = self.client.post(
            "/auth/login",
            json={"username": "admin", "password": "kiroproxy"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertIn("kiroproxy_session", response.cookies)

        api_response = self.client.get("/api/status")
        self.assertEqual(api_response.status_code, 200)
        self.assertTrue(api_response.json()["ok"])

    def test_invalid_login_is_rejected(self):
        response = self.client.post(
            "/auth/login",
            json={"username": "admin", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Invalid credentials")

    def test_login_accepts_configured_admin_credentials(self):
        with patch.dict(
            os.environ,
            {
                "KIROPROXY_ADMIN_USERNAME": "root",
                "KIROPROXY_ADMIN_PASSWORD": "secret-pass",
            },
            clear=False,
        ):
            self._reload_auth_config()
            response = self.client.post(
                "/auth/login",
                json={"username": "root", "password": "secret-pass"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self._reload_auth_config()

    def test_security_config_masks_api_key(self):
        with patch.dict(
            os.environ,
            {
                "KIROPROXY_ADMIN_USERNAME": "root",
                "KIROPROXY_ADMIN_PASSWORD": "secret-pass",
                "KIROPROXY_API_KEY": "secret-xyz",
            },
            clear=False,
        ):
            self._reload_auth_config()
            login = self.client.post(
                "/auth/login",
                json={"username": "root", "password": "secret-pass"},
            )
            self.assertEqual(login.status_code, 200)
            response = self.client.get("/api/security-config")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["admin_username"], "root")
        self.assertEqual(payload["proxy_api_key_masked"], "sec***yz")
        self.assertFalse(payload["proxy_api_key_is_default"])
        self._reload_auth_config()

    def test_logout_clears_session(self):
        login = self.client.post(
            "/auth/login",
            json={"username": "admin", "password": "kiroproxy"},
        )
        self.assertEqual(login.status_code, 200)

        logout = self.client.post("/auth/logout")
        self.assertEqual(logout.status_code, 200)
        self.assertTrue(logout.json()["ok"])

        api_response = self.client.get("/api/status")
        self.assertEqual(api_response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
