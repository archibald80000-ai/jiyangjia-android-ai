from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/check_provider_env.py")


def test_provider_env_check_reports_missing_without_values(tmp_path: Path) -> None:
    env_file = tmp_path / ".env.local"
    env_file.write_text(
        "\n".join(
            [
                "JIYANGJIA_ASR_PROVIDER=doubao",
                "JIYANGJIA_TTS_PROVIDER=doubao",
                "JIYANGJIA_LLM_PROVIDER=doubao",
                "JIYANGJIA_EMBEDDING_PROVIDER=doubao",
                "DOUBAO_TTS_SPEAKER=secret-speaker",
            ]
        ),
        encoding="utf-8",
    )
    compose_file = tmp_path / "docker-compose.yml"
    compose_file.write_text("env_file:\n  - ../secrets/.env.local\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--env-file",
            str(env_file),
            "--compose-file",
            str(compose_file),
            "--require-real-mvp",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["real_mvp_ready"] is False
    assert payload["compose"]["points_to_expected_env_file"] is True
    assert payload["providers"]["asr"]["missing"] == ["DOUBAO_ASR_AUTH"]
    assert "secret-speaker" not in result.stdout


def test_provider_env_check_accepts_configured_doubao_chain(tmp_path: Path) -> None:
    env_file = tmp_path / ".env.local"
    env_file.write_text(
        "\n".join(
            [
                "JIYANGJIA_ASR_PROVIDER=doubao",
                "JIYANGJIA_TTS_PROVIDER=doubao",
                "JIYANGJIA_LLM_PROVIDER=doubao",
                "JIYANGJIA_EMBEDDING_PROVIDER=doubao",
                "DOUBAO_ASR_API_KEY=secret-asr",
                "DOUBAO_TTS_API_KEY=secret-tts",
                "DOUBAO_TTS_SPEAKER=secret-speaker",
                "DOUBAO_API_KEY=secret-ark",
                "DOUBAO_MODEL=secret-model",
            ]
        ),
        encoding="utf-8",
    )
    compose_file = tmp_path / "docker-compose.yml"
    compose_file.write_text("env_file:\n  - ../secrets/.env.local\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--env-file",
            str(env_file),
            "--compose-file",
            str(compose_file),
            "--require-real-mvp",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["real_mvp_ready"] is True
    assert payload["providers"]["embedding"]["ready"] is True
    assert "secret-" not in result.stdout
