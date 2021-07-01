

def test_count_symb():
    phrase = input("Set a phrase: ")
    job_len = 15
    count = len(phrase)
    print(f"Lenght of inserted phrase is {count}.")
    assert count < job_len, f"Phrase length more than {job_len}."
