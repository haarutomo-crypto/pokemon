import os
from app import BattleTracker

def run_tests():
    test_filepath = "test_records.jsonl"

    # Cleanup before test
    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    tracker = BattleTracker(filepath=test_filepath)

    print("Testing save_record with individual stats...")
    # save_record(name, hp, attack, defense, sp_atk, sp_def, speed, notes)
    tracker.save_record("Pikachu", "35", "55", "40", "50", "50", "90", "Electric mouse")
    tracker.save_record("Charizard", "78", "84", "78", "109", "85", "100", "Fire flying dragon")
    tracker.save_record("Snorlax", "160", "110", "65", "65", "110", "30", "Heavy sleeper")

    assert os.path.exists(test_filepath), "File should be created"

    print("Testing search_records with empty keyword...")
    all_records = tracker.search_records("")
    assert len(all_records) == 3, f"Expected 3 records, got {len(all_records)}"

    print("Testing get_all_names for suggestions...")
    names = tracker.get_all_names()
    assert len(names) == 3, "Expected 3 unique names"
    assert "Pikachu" in names
    assert "Snorlax" in names

    print("Testing data sorting simulation...")
    all_records.sort(key=lambda x: x.get("speed", 0), reverse=True)
    assert all_records[0]["name"] == "Charizard", "Expected Charizard to be fastest"
    assert all_records[2]["name"] == "Snorlax", "Expected Snorlax to be slowest"

    all_records.sort(key=lambda x: x.get("hp", 0), reverse=False)
    assert all_records[0]["name"] == "Pikachu", "Expected Pikachu to have lowest HP"
    assert all_records[2]["name"] == "Snorlax", "Expected Snorlax to have highest HP"

    # Cleanup after test
    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
