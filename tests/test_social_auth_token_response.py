import unittest
from datetime import datetime, timezone

from kiro_proxy.auth.device_flow import _normalize_social_token_response


class SocialAuthTokenResponseTests(unittest.TestCase):
    def test_accepts_kiro_camel_case_token_response(self):
        ok, result = _normalize_social_token_response(
            {
                "accessToken": "access-token",
                "refreshToken": "refresh-token",
                "expiresIn": 3600,
                "profileArn": "arn:aws:codewhisperer:us-east-1:123:profile/test",
            },
            "Google",
        )

        self.assertTrue(ok)
        credentials = result["credentials"]
        self.assertEqual(credentials["accessToken"], "access-token")
        self.assertEqual(credentials["refreshToken"], "refresh-token")
        self.assertEqual(credentials["profileArn"], "arn:aws:codewhisperer:us-east-1:123:profile/test")
        self.assertEqual(credentials["provider"], "Google")
        self.assertEqual(credentials["authMethod"], "social")

        expires_at = datetime.fromisoformat(credentials["expiresAt"])
        self.assertGreater(expires_at, datetime.now(timezone.utc))

    def test_rejects_response_without_access_token(self):
        ok, result = _normalize_social_token_response(
            {
                "refreshToken": "refresh-token",
                "expiresIn": 3600,
            },
            "GitHub",
        )

        self.assertFalse(ok)
        self.assertIn("access_token/accessToken", result["error"])
        self.assertIn("refreshToken", result["error"])


if __name__ == "__main__":
    unittest.main()
