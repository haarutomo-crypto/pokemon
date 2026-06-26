import os
from app import BattleTracker

def run_tests():
    test_filepath = "test_records.jsonl"

    # Cleanup before test
    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    tracker = BattleTracker(filepath=test_filepath)

    print("Testing save_record...")
    tracker.save_record("Pikachu", "Charizard", "Win", "Used Thunderbolt")
    tracker.save_record("Gengar", "Alakazam", "Loss", "Outsped")

    assert os.path.exists(test_filepath), "File should be created"

    print("Testing search_records with empty keyword...")
    all_records = tracker.search_records("")
    assert len(all_records) == 2, f"Expected 2 records, got {len(all_records)}"

    print("Testing search_records with specific keyword...")
    win_records = tracker.search_records("Win")
    assert len(win_records) == 1, "Expected 1 record"
    assert win_records[0]["my_pokemon"] == "Pikachu", "Expected Pikachu record"

    print("Testing search_records with case-insensitivity...")
    charizard_records = tracker.search_records("charizard")
    assert len(charizard_records) == 1, "Expected 1 record"
    assert charizard_records[0]["opp_pokemon"] == "Charizard", "Expected Charizard record"

    # Cleanup after test
    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
