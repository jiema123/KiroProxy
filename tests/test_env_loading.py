import importlib
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class EnvLoadingTests(unittest.TestCase):
    def test_frozen_mode_prefers_executable_directory_dotenv(self):
        temp_dir = Path(tempfile.mkdtemp(prefix="kiroproxy-env-"))
        try:
            fake_exe = temp_dir / "KiroProxy"
            fake_exe.write_text("", encoding="utf-8")
            (temp_dir / ".env").write_text(
                "\n".join(
                    [
                        "KIRO_SERVER_PORT=19080",
                        "KIROPROXY_ADMIN_USERNAME=exe-admin",
                        "KIROPROXY_ADMIN_PASSWORD=exe-pass",
                        "KIROPROXY_API_KEY=exe-key",
                    ]
                ),
                encoding="utf-8",
            )

            import kiro_proxy.env_config as env_config

            with patch.dict(
                os.environ,
                {
                    "KIRO_SERVER_PORT": " ",
                    "KIROPROXY_ADMIN_USERNAME": " ",
                    "KIROPROXY_ADMIN_PASSWORD": " ",
                    "KIROPROXY_API_KEY": " ",
                },
                clear=False,
            ):
                with patch("sys.frozen", True, create=True), patch("sys.executable", str(fake_exe)):
                    reloaded = importlib.reload(env_config)

            self.assertEqual(reloaded.SERVER_PORT, 19080)
            self.assertEqual(reloaded.ADMIN_USERNAME, "exe-admin")
            self.assertEqual(reloaded.ADMIN_PASSWORD, "exe-pass")
            self.assertEqual(reloaded.PROXY_API_KEY, "exe-key")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
