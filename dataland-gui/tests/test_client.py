from dataland_gui import client as dl

class MockResp:
    def __init__(self, json_data, status_code=200, headers=None):
        self._json = json_data
        self.status_code = status_code
        self.headers = headers or {}
    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise Exception(self.status_code)
    def json(self):
        return self._json

def test_search_companies(monkeypatch):
    def fake_get(url, params=None, headers=None, timeout=None):
        return MockResp([{"companyId": "1", "companyName": "Foo AG"}])
    monkeypatch.setattr(dl.requests, "get", fake_get)
    res = dl.search_companies("Foo")
    assert res and res[0].company_name == "Foo AG"

def test_get_company_sfdr(monkeypatch):
    def fake_get(url, params=None, headers=None, timeout=None):
        return MockResp({"ok": True, "params": params})
    monkeypatch.setattr(dl.requests, "get", fake_get)
    res = dl.get_company_sfdr("abc", reporting_period=2023, show_only_active=True)
    assert res["ok"] is True
