"""Tests for QuakeML library."""
from datetime import datetime
from typing import Optional, Tuple, Dict

from aio_quakeml_client import QuakeMLFeed, FeedEntry, Event, T_FEED_ENTRY


class MockFeedEntry(FeedEntry):

    @property
    def attribution(self) -> Optional[str]:
        return None


class MockQuakeMLFeed(QuakeMLFeed[MockFeedEntry]):

    def _extract_from_feed(self, feed) -> Optional:
        return None

    def _extract_last_timestamp(self, feed_entries) -> Optional[datetime]:
        return None

    def _new_entry(self, home_coordinates: Tuple[float, float],
                   event: Event, global_data: Dict) -> MockFeedEntry:
        return MockFeedEntry(home_coordinates, event)