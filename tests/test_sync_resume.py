import io
import json
import unittest
from unittest.mock import patch

import scripts.sync_resume as sync_resume


class PortfolioFallbackTests(unittest.TestCase):
    @patch.object(sync_resume, "extract_resume_text", return_value="resume text")
    @patch.object(sync_resume, "call_groq_with_resume", side_effect=RuntimeError("Groq unavailable"))
    @patch.object(sync_resume, "call_gemini_with_resume", return_value={"provider": "gemini"})
    def test_uses_gemini_when_groq_fails(self, gemini_call, groq_call, _extract):
        result = sync_resume.update_portfolio_with_fallback(
            b"pdf", {"existing": True}, "groq-key", "gemini-key"
        )

        self.assertEqual(result, {"provider": "gemini"})
        groq_call.assert_called_once_with("groq-key", "resume text", {"existing": True})
        gemini_call.assert_called_once_with("gemini-key", "resume text", {"existing": True})

    @patch.object(sync_resume, "extract_resume_text", return_value="resume text")
    @patch.object(sync_resume, "call_groq_with_resume", return_value={"provider": "groq"})
    @patch.object(sync_resume, "call_gemini_with_resume")
    def test_does_not_call_gemini_when_groq_succeeds(self, gemini_call, groq_call, _extract):
        result = sync_resume.update_portfolio_with_fallback(
            b"pdf", {"existing": True}, "groq-key", "gemini-key"
        )

        self.assertEqual(result, {"provider": "groq"})
        gemini_call.assert_not_called()

    @patch.object(sync_resume.urllib.request, "urlopen")
    def test_gemini_fallback_uses_supported_latest_model(self, urlopen):
        response = io.BytesIO(json.dumps({
            "candidates": [{
                "content": {"parts": [{"text": '{"provider":"gemini"}'}]}
            }]
        }).encode())
        urlopen.return_value = response

        result = sync_resume.call_gemini_with_resume("test-key", "resume text", {})

        self.assertEqual(result, {"provider": "gemini"})
        request = urlopen.call_args.args[0]
        self.assertIn("/models/gemini-flash-lite-latest:generateContent", request.full_url)
        payload = json.loads(request.data)
        self.assertEqual(
            payload["generationConfig"]["responseMimeType"],
            "application/json"
        )


if __name__ == "__main__":
    unittest.main()
