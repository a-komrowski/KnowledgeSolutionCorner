from src.dataland_pipeline.persist import create_envelope

def test_envelope_has_basic_fields():
    env = create_envelope("/x", 200, {"q":"a"}, {})
    assert env["endpoint"] == "/x"
    assert env["status"] == 200
    assert "ts" in env
