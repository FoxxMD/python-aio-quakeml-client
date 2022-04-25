"""Test for the generic QuakeML feed."""
import asyncio
from unittest.mock import MagicMock

import aiohttp
import pytest
from aiohttp import ClientOSError

from aio_quakeml_client.consts import UPDATE_ERROR, UPDATE_OK
# from aio_geojson_client.filter_definition import GeoJsonFeedFilterDefinition
# from aio_geojson_client.geometries.point import Point
# from aio_geojson_client.geometries.polygon import Polygon
from tests import MockQuakeMLFeed
from tests.utils import load_fixture


@pytest.mark.asyncio
async def test_update_ok(aresponses, event_loop):
    """Test updating feed is ok."""
    home_coordinates = (-31.0, 151.0)
    aresponses.add(
        "test.url",
        "/testpath",
        "get",
        aresponses.Response(text=load_fixture("generic_feed_1.xml"), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:

        feed = MockQuakeMLFeed(websession, home_coordinates, "http://test.url/testpath")
        assert (
            repr(feed) == "<MockQuakeMLFeed(home=(-31.0, 151.0), "
            "url=http://test.url/testpath, radius=None)>"
        )
        status, entries = await feed.update()
        assert status == UPDATE_OK
        assert entries is not None
        assert len(entries) == 1

        feed_entry = entries[0]
        assert feed_entry is not None
        # assert feed_entry.title == "Title 1"
        assert feed_entry.external_id == "smi:webservices.ingv.it/fdsnws/event/1/query?eventId=30116321"
        assert feed_entry.coordinates == (42.5218, 13.3833)
        assert feed_entry.description == "Region name: 4 km S Campotosto (AQ)"
        assert round(abs(feed_entry.distance_to_home - 16074.6), 1) == 0
        assert repr(feed_entry) == "<MockFeedEntry(id=smi:webservices.ingv.it/fdsnws/event/1/query?eventId=30116321)>"

        # feed_entry = entries[1]
        # assert feed_entry is not None
        # assert feed_entry.title == "Title 2"
        # assert feed_entry.external_id == "4567"
        #
        # feed_entry = entries[2]
        # assert feed_entry is not None
        # assert feed_entry.title == "Title 3"
        # assert feed_entry.external_id == "Title 3"
        #
        # feed_entry = entries[3]
        # assert feed_entry is not None
        # assert feed_entry.title is None
        # assert feed_entry.external_id == hash(feed_entry.coordinates)
        #
        # feed_entry = entries[4]
        # assert feed_entry is not None
        # assert feed_entry.title == "Title 5"
        # assert feed_entry.external_id == "7890"


# @pytest.mark.asyncio
# async def test_update_ok_with_filtering(aresponses, event_loop):
#     """Test updating feed is ok."""
#     home_coordinates = (-37.0, 150.0)
#     aresponses.add(
#         "test.url",
#         "/testpath",
#         "get",
#         aresponses.Response(text=load_fixture("generic_feed_1.json"), status=200),
#     )
#
#     async with aiohttp.ClientSession(loop=event_loop) as websession:
#         feed = MockGeoJsonFeed(
#             websession, home_coordinates, "http://test.url/testpath", filter_radius=90.0
#         )
#         status, entries = await feed.update()
#         assert status == UPDATE_OK
#         assert entries is not None
#         assert len(entries) == 4
#         assert round(abs(entries[0].distance_to_home - 82.0), 1) == 0
#         assert round(abs(entries[1].distance_to_home - 77.0), 1) == 0
#         assert round(abs(entries[2].distance_to_home - 84.6), 1) == 0
#
#
# @pytest.mark.asyncio
# async def test_update_ok_with_filter_override(aresponses, event_loop):
#     """Test updating feed is ok."""
#     home_coordinates = (-37.0, 150.0)
#     aresponses.add(
#         "test.url",
#         "/testpath",
#         "get",
#         aresponses.Response(text=load_fixture("generic_feed_1.json"), status=200),
#     )
#
#     async with aiohttp.ClientSession(loop=event_loop) as websession:
#         feed = MockGeoJsonFeed(
#             websession, home_coordinates, "http://test.url/testpath", filter_radius=60.0
#         )
#         status, entries = await feed.update_override(
#             filter_overrides=GeoJsonFeedFilterDefinition(radius=90.0)
#         )
#         assert status == UPDATE_OK
#         assert entries is not None
#         assert len(entries) == 4
#         assert round(abs(entries[0].distance_to_home - 82.0), 1) == 0
#         assert round(abs(entries[1].distance_to_home - 77.0), 1) == 0
#         assert round(abs(entries[2].distance_to_home - 84.6), 1) == 0
#
#
# @pytest.mark.asyncio
# async def test_update_geometries(aresponses, event_loop):
#     """Test updating feed is ok."""
#     home_coordinates = (-31.0, 151.0)
#     aresponses.add(
#         "test.url",
#         "/testpath",
#         "get",
#         aresponses.Response(text=load_fixture("generic_feed_3.json"), status=200),
#     )
#
#     async with aiohttp.ClientSession(loop=event_loop) as websession:
#
#         feed = MockGeoJsonFeed(websession, home_coordinates, "http://test.url/testpath")
#         assert (
#             repr(feed) == "<MockGeoJsonFeed(home=(-31.0, 151.0), "
#             "url=http://test.url/testpath, radius=None)>"
#         )
#         status, entries = await feed.update()
#         assert status == UPDATE_OK
#         assert entries is not None
#         assert len(entries) == 3
#
#         feed_entry = entries[0]
#         assert feed_entry is not None
#         assert feed_entry.title == "Title 1"
#         assert feed_entry.external_id == "1234"
#         assert isinstance(feed_entry.geometries[0], Point)
#         assert feed_entry.coordinates == (-35.5, 150.5)
#         assert round(abs(feed_entry.distance_to_home - 502.5), 1) == 0
#         assert repr(feed_entry) == "<MockFeedEntry(id=1234)>"
#
#         feed_entry = entries[1]
#         assert feed_entry is not None
#         assert feed_entry.title == "Title 2"
#         assert feed_entry.external_id == "2345"
#         assert isinstance(feed_entry.geometries[0], Polygon)
#         assert feed_entry.coordinates == (-28.0, 152.0)
#
#         feed_entry = entries[2]
#         assert feed_entry is not None
#         assert feed_entry.title == "Title 3"
#         assert feed_entry.external_id == "3456"
#         assert isinstance(feed_entry.geometries[0], Point)
#         assert isinstance(feed_entry.geometries[1], Polygon)
#         assert feed_entry.coordinates == (-35.5, 150.5)
#
#
# @pytest.mark.asyncio
# async def test_update_with_client_exception(event_loop):
#     """Test updating feed results in error."""
#     home_coordinates = (-31.0, 151.0)
#
#     async with aiohttp.ClientSession(loop=event_loop):
#         mock_websession = MagicMock()
#         mock_websession.request.side_effect = ClientOSError
#         feed = MockGeoJsonFeed(
#             mock_websession, home_coordinates, "http://test.url/badpath"
#         )
#         status, entries = await feed.update()
#         assert status == UPDATE_ERROR
#         assert feed.last_timestamp is None
#
#
# @pytest.mark.asyncio
# async def test_update_with_request_exception(aresponses, event_loop):
#     """Test updating feed results in error."""
#     home_coordinates = (-31.0, 151.0)
#     aresponses.add("test.url", "/badpath", "get", aresponses.Response(status=404))
#
#     async with aiohttp.ClientSession(loop=event_loop) as websession:
#         feed = MockGeoJsonFeed(websession, home_coordinates, "http://test.url/badpath")
#         status, entries = await feed.update()
#         assert status == UPDATE_ERROR
#         assert feed.last_timestamp is None
#
#
# @pytest.mark.asyncio
# async def test_update_with_json_decode_error(aresponses, event_loop):
#     """Test updating feed raises exception."""
#     home_coordinates = (-31.0, 151.0)
#     aresponses.add(
#         "test.url", "/badjson", "get", aresponses.Response(text="NOT JSON", status=200)
#     )
#
#     async with aiohttp.ClientSession(loop=event_loop) as websession:
#         feed = MockGeoJsonFeed(websession, home_coordinates, "http://test.url/badjson")
#         status, entries = await feed.update()
#         assert status == UPDATE_ERROR
#         assert entries is None
#
#
# @pytest.mark.asyncio
# async def test_update_with_timeout_error(event_loop):
#     """Test updating feed results in timeout error."""
#     home_coordinates = (-31.0, 151.0)
#
#     async with aiohttp.ClientSession(loop=event_loop):
#         mock_websession = MagicMock()
#         mock_websession.request.side_effect = asyncio.TimeoutError
#         feed = MockGeoJsonFeed(
#             mock_websession, home_coordinates, "http://test.url/goodpath"
#         )
#         status, entries = await feed.update()
#         assert status == UPDATE_ERROR
#         assert feed.last_timestamp is None
#
#
# @pytest.mark.asyncio
# async def test_update_ok_feed_feature(aresponses, event_loop):
#     """Test updating feed is ok."""
#     home_coordinates = (-31.0, 151.0)
#     aresponses.add(
#         "test.url",
#         "/testpath",
#         "get",
#         aresponses.Response(text=load_fixture("generic_feed_4.json"), status=200),
#     )
#
#     async with aiohttp.ClientSession(loop=event_loop) as websession:
#
#         feed = MockGeoJsonFeed(websession, home_coordinates, "http://test.url/testpath")
#         assert (
#             repr(feed) == "<MockGeoJsonFeed(home=(-31.0, 151.0), "
#             "url=http://test.url/testpath, radius=None)>"
#         )
#         status, entries = await feed.update()
#         assert status == UPDATE_OK
#         assert entries is not None
#         assert len(entries) == 1
#
#         feed_entry = entries[0]
#         assert feed_entry is not None
#         assert feed_entry.title == "Title 1"
#         assert feed_entry.external_id == "3456"
#         assert feed_entry.coordinates == (-37.2345, 149.1234)
#         assert round(abs(feed_entry.distance_to_home - 714.4), 1) == 0
#         assert repr(feed_entry) == "<MockFeedEntry(id=3456)>"
#
#
# @pytest.mark.asyncio
# async def test_unsupported_object(aresponses, event_loop, caplog):
#     """Test updating feed is ok."""
#     home_coordinates = (-31.0, 151.0)
#     aresponses.add(
#         "test.url",
#         "/testpath",
#         "get",
#         aresponses.Response(text=load_fixture("generic_feed_5.json"), status=200),
#     )
#
#     async with aiohttp.ClientSession(loop=event_loop) as websession:
#
#         feed = MockGeoJsonFeed(websession, home_coordinates, "http://test.url/testpath")
#         assert (
#             repr(feed) == "<MockGeoJsonFeed(home=(-31.0, 151.0), "
#             "url=http://test.url/testpath, radius=None)>"
#         )
#         status, entries = await feed.update()
#         assert status == UPDATE_OK
#         assert entries is not None
#         assert len(entries) == 0
#
#         assert (
#             "Unsupported GeoJSON object found: <class 'geojson.geometry.Point'>"
#             in caplog.text
#         )