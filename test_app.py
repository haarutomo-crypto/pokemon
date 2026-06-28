import os
from app import BattleTracker

def run_tests():
    test_filepath = "test_records.jsonl"

    # Cleanup before test
    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    tracker = BattleTracker(filepath=test_filepath)

    print("Testing save_record with list notes...")
    tracker.save_record("Pikachu", "せっかち", "35", "55", "40", "50", "50", "90", "4", "0", "0", "252", "0", "252", "First note\nSecond note\nThird note")

    all_records = tracker.search_records("")
    assert len(all_records) == 1
    pika_id = all_records[0]["id"]

    assert all_records[0]["nature"] == "せっかち"
    assert all_records[0]["ev_speed"] == 252

    # Notes should be stored cleanly without numbers
    assert len(all_records[0]["notes"]) == 3
    assert all_records[0]["notes"][0] == "First note"

    print("Testing format removal numbering...")
    # Test that save_record correctly cleans existing numbers from user input
    tracker.save_record("Charizard", "ひかえめ", "78", "84", "78", "109", "85", "100", "0", "0", "0", "252", "4", "252", "1. Fire\n2) Flying\n[3] Cool\n100% accuracy")
    all_records = tracker.search_records("")
    charizard = next(r for r in all_records if r["name"] == "Charizard")
    assert charizard["notes"][0] == "Fire", "Expected '1. ' to be stripped"
    assert charizard["notes"][1] == "Flying", "Expected '2) ' to be stripped"
    assert charizard["notes"][2] == "Cool", "Expected '[3] ' to be stripped"

    print("Testing update_record...")
    tracker.update_record(pika_id, "Pikachu", "おくびょう", "35", "55", "40", "50", "50", "90", "4", "0", "0", "252", "0", "252", "Updated note")
    all_records = tracker.search_records("")
    updated_pika = next(r for r in all_records if r["id"] == pika_id)
    assert len(updated_pika["notes"]) == 1
    assert updated_pika["notes"][0] == "Updated note"

    print("Testing delete_record...")
    tracker.delete_record(pika_id)
    all_records = tracker.search_records("")
    assert len(all_records) == 1
    assert all_records[0]["name"] == "Charizard"

    # Cleanup after test
    if os.path.exists(test_filepath):
        os.remove(test_filepath)

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
