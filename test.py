from download import manual_download_dir

def test1():
    def press_enter_to_continue():
        input("Press Enter to continue...")
        print("\033[F\033[K", end="")  # Moves up one line and clears it

    # Example usage
    print("Step 1: Complete this action.")
    press_enter_to_continue()

    print("Step 2: Moving to the next step.")
    press_enter_to_continue()

    print("Program finished.")


def test2():
    print("Downloading file...")
    manual_download_dir("https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9157425", "file.pdf", "downloads", show_download_dir=True)
    print("File downloaded.")


if __name__ == "__main__":
    test2()