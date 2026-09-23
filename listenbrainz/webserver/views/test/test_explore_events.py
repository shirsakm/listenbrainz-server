from unittest import mock
from unittest.mock import patch

from listenbrainz.tests.integration import IntegrationTestCase


class ExploreEventsTestCase(IntegrationTestCase):

    @patch("listenbrainz.db.event_feed.get_upcoming_events_global", return_value=([], 0))
    def test_get_events(self, mock_global):
        resp = self.client.get(self.custom_url_for("explore_api_v1.get_events"))
        self.assert200(resp)
        payload = resp.json["payload"]
        self.assertIn("events", payload)
        self.assertIn("total_count", payload)
        self.assertEqual(payload["total_count"], 0)
        self.assertEqual(payload["events"], [])

    @patch("listenbrainz.db.event_feed.get_upcoming_events_global", return_value=([], 0))
    def test_get_events_default_params(self, mock_global):
        """Default count and offset are forwarded to the DB function."""
        self.client.get(self.custom_url_for("explore_api_v1.get_events"))
        mock_global.assert_called_with(mock.ANY, 25, 0)

    @patch("listenbrainz.db.event_feed.get_upcoming_events_global", return_value=([], 0))
    def test_get_events_with_count_offset(self, mock_global):
        self.client.get(self.custom_url_for("explore_api_v1.get_events", count=10, offset=20))
        mock_global.assert_called_with(mock.ANY, 10, 20)

    def test_get_events_invalid_count(self):
        resp = self.client.get(self.custom_url_for("explore_api_v1.get_events", count="notanint"))
        self.assert400(resp)

    def test_get_events_count_exceeds_max(self):
        resp = self.client.get(self.custom_url_for("explore_api_v1.get_events", count=9999))
        self.assert400(resp)

    def test_get_events_count_zero(self):
        resp = self.client.get(self.custom_url_for("explore_api_v1.get_events", count=0))
        self.assert400(resp)

    def test_get_events_negative_offset(self):
        resp = self.client.get(self.custom_url_for("explore_api_v1.get_events", offset=-1))
        self.assert400(resp)
