from datetime import date
from pathlib import Path

from covid19_scrapers.registry import Registry
from covid19_scrapers.scraper import ScraperBase
from covid19_scrapers.utils.testing import (
    FakeCensusApi, fake_webcache)


CENSUS_API = FakeCensusApi()


class MockScraperOneSeries(ScraperBase):
    def __init__(self):
        super().__init__(home_dir=Path('test'),
                         census_api=CENSUS_API)

    def _scrape(self, start_date, end_date):
        return [self._make_series()]


class MockScraperTwoSeries(ScraperBase):
    def __init__(self):
        super().__init__(home_dir=Path('test'),
                         census_api=CENSUS_API)

    def _scrape(self, start_date, end_date):
        return [self._make_series(), self._make_series()]


class TestRegistry(object):
    DATES = {
        'start_date': None,
        'end_date': date.today()
    }

    def setup(self):
        self.registry = Registry(
            web_cache=fake_webcache()[0])

    def test_empty_registry(self):
        df = self.registry.run_all_scrapers(**self.DATES)
        assert df.shape[0] == 0

    def test_oneseries_registry(self):
        self.registry.register_scraper(MockScraperOneSeries())
        df = self.registry.run_scraper('MockScraperOneSeries', **self.DATES)
        assert df.shape[0] == 1

        df = self.registry.run_scrapers(['MockScraperOneSeries'], **self.DATES)
        assert df.shape[0] == 1

        df = self.registry.run_all_scrapers(**self.DATES)
        assert df.shape[0] == 1

    def test_twoseries_registry(self):
        self.registry.register_scraper(MockScraperTwoSeries())
        df = self.registry.run_scraper('MockScraperTwoSeries', **self.DATES)
        assert df.shape[0] == 2

        df = self.registry.run_scrapers(['MockScraperTwoSeries'], **self.DATES)
        assert df.shape[0] == 2

        df = self.registry.run_all_scrapers(**self.DATES)
        assert df.shape[0] == 2

    def test_multi_registry(self):
        self.registry.register_scraper(MockScraperOneSeries())
        self.registry.register_scraper(MockScraperTwoSeries())

        df = self.registry.run_scraper('MockScraperOneSeries', **self.DATES)
        assert df.shape[0] == 1

        df = self.registry.run_scrapers(['MockScraperOneSeries'], **self.DATES)
        assert df.shape[0] == 1

        df = self.registry.run_scraper('MockScraperTwoSeries', **self.DATES)
        assert df.shape[0] == 2

        df = self.registry.run_scrapers(['MockScraperTwoSeries'], **self.DATES)
        assert df.shape[0] == 2

        df = self.registry.run_scrapers(['MockScraperOneSeries',
                                         'MockScraperTwoSeries'], **self.DATES)
        assert df.shape[0] == 3

        df = self.registry.run_all_scrapers(**self.DATES)
        assert df.shape[0] == 3
