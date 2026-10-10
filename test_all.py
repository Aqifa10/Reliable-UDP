"""test_all.py: every test in the project, in one file.

Run everything:        python test_all.py
Run only your part:    python test_all.py gbn      (tests whose name starts with test_gbn)

Each section belongs to one person. Your tests fail until you write your
code; that is expected. Tests use small files and a 2 ms delay so they run fast.
"""

import sys
import time
import traceback
import packet


# --- Atul: packet.py ---
def test_packet_checksum_known_value():
    assert packet.checksum(b"\x00\x01\xf2\x03\xf4\xf5\xf6\xf7") == 0x220D  # RFC 1071 example


def test_packet_hello_bytes():
    raw = packet.make_packet(7, 0, packet.DATA | packet.FIN, b"hello")
    assert raw.hex(" ") == "00 00 00 07 00 00 00 00 05 00 05 23 b5 68 65 6c 6c 6f"


def test_packet_flipped_bit_is_rejected():
    raw = bytearray(packet.make_packet(1, 0, packet.DATA, b"payload"))
    raw[15] ^= 0x04
    assert packet.parse_packet(bytes(raw)) is None


def test_packet_split_file():
    assert packet.split_file(b"") == [b""]
    assert [len(c) for c in packet.split_file(b"x" * 2500)] == [1024, 1024, 452]


def main():
    words = [w for w in sys.argv[1:] if w != "-v"]

    # Matches the word you typed in the terminal to the tests in this file
    tests = [(name, fn) for name, fn in globals().items()
             if name.startswith("test_") and callable(fn) and
             (not words or any(name.startswith("test_" + w) for w in words))]

    failed = 0
    start = time.monotonic()

    for name, fn in tests:
        try:
            fn()
            print(f"PASS {name}")
        except NotImplementedError:
            failed += 1
            print(f"TODO {name} (not written yet)")
        except Exception as e:
            failed += 1
            print(f"FAIL {name} {type(e).__name__}: {e}")
            if "-v" in sys.argv:
                traceback.print_exc()

    passed = len(tests) - failed
    print(f"\n{passed} passed, {failed} failed, {time.monotonic() - start:.0f} s")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
