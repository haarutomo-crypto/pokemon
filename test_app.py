import os
from app import BattleTracker

def run_tests():
    test_filepath = "test_records.jsonl"

    # Cleanup before test
    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    tracker = BattleTracker(filepath=test_filepath)

    print("Testing save_record...")
    tracker.save_record("Pikachu", "320", "Electric mouse")
    tracker.save_record("Charizard", "534", "Fire flying dragon")

    assert os.path.exists(test_filepath), "File should be created"

    print("Testing search_records with empty keyword...")
    all_records = tracker.search_records("")
    assert len(all_records) == 2, f"Expected 2 records, got {len(all_records)}"

    print("Testing search_records with specific keyword...")
    electric_records = tracker.search_records("Electric")
    assert len(electric_records) == 1, "Expected 1 record"
    assert electric_records[0]["name"] == "Pikachu", "Expected Pikachu record"

    print("Testing search_records with case-insensitivity...")
    charizard_records = tracker.search_records("charizard")
    assert len(charizard_records) == 1, "Expected 1 record"
    assert charizard_records[0]["base_stats"] == "534", "Expected base stats 534"

    # Cleanup after test
    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
