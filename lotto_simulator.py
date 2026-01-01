import random
from collections import Counter

MIN_NUM = 1
MAX_NUM = 49
PICKS = 6


def generate_ticket(numbers=None):
    """Return a sorted list of PREFERRED ticket numbers.
    If numbers is None, return a random ticket (6 unique numbers).
    If numbers is provided, validate and return it sorted.
    """
    if numbers is None:
        ticket = sorted(random.sample(range(MIN_NUM, MAX_NUM + 1), PICKS))
        return ticket
    nums = sorted(set(numbers))
    if len(nums) != PICKS or any(n < MIN_NUM or n > MAX_NUM for n in nums):
        raise ValueError(f"Bitte {PICKS} eindeutige Zahlen zwischen {MIN_NUM} und {MAX_NUM} angeben.")
    return nums


def draw():
    """Simulate a lotto draw and return sorted list of numbers."""
    return sorted(random.sample(range(MIN_NUM, MAX_NUM + 1), PICKS))


def check_ticket(ticket, drawn):
    """Return (matches_set, count)."""
    tset = set(ticket)
    dset = set(drawn)
    matches = tset & dset
    return matches, len(matches)


def simulate(n_draws, ticket=None):
    """Simulate n_draws and return a Counter of match counts.
    If ticket is None a random ticket is generated once and used.
    """
    if ticket is None:
        ticket = generate_ticket()
    counts = Counter()
    for _ in range(n_draws):
        drawn = draw()
        _, c = check_ticket(ticket, drawn)
        counts[c] += 1
    return ticket, counts


def pretty_show(ticket, drawn, matches):
    print(f"Ihr Tipp:      {ticket}")
    print(f"Gezogene Nr.: {drawn}")
    print(f"Treffer ({len(matches)}): {sorted(matches)}")


def main():
    while True:
        print('\nLotto-Simulator (6 aus 49)')
        print('1) Zufallstipp erstellen und einmal ziehen')
        print('2) Manuelle Zahlen eingeben und ziehen')
        print('3) Simulation: viele Ziehungen für einen Tipp')
        print('4) Beenden')
        choice = input('Wahl (1-4): ').strip()
        if choice == '1':
            ticket = generate_ticket()
            drawn = draw()
            matches, _ = check_ticket(ticket, drawn)
            pretty_show(ticket, drawn, matches)
        elif choice == '2':
            raw = input('Geben Sie 6 Zahlen (getrennt durch Leerzeichen): ').strip()
            try:
                nums = [int(x) for x in raw.split()]
                ticket = generate_ticket(nums)
            except Exception as e:
                print('Ungültige Eingabe:', e)
                continue
            drawn = draw()
            matches, _ = check_ticket(ticket, drawn)
            pretty_show(ticket, drawn, matches)
        elif choice == '3':
            raw = input('Anzahl der Ziehungen: ').strip()
            try:
                n = int(raw)
                if n <= 0:
                    raise ValueError()
            except:
                print('Bitte eine positive ganze Zahl eingeben.')
                continue
            sub = input('Tipp verwenden? Eingabe: "j" für eigenen Tipp, sonst Zufall: ').strip().lower()
            if sub == 'j':
                raw2 = input('Geben Sie 6 Zahlen (getrennt durch Leerzeichen): ').strip()
                try:
                    nums = [int(x) for x in raw2.split()]
                    ticket = generate_ticket(nums)
                except Exception as e:
                    print('Ungültige Eingabe:', e)
                    continue
            else:
                ticket = None
            ticket, counts = simulate(n, ticket)
            print(f'Verwendeter Tipp: {ticket}')
            for matches in sorted(counts.keys(), reverse=True):
                print(f'{matches} Treffer: {counts[matches]} mal')
        elif choice == '4':
            print('Auf Wiedersehen!')
            break
        else:
            print('Ungültige Wahl.')


if __name__ == '__main__':
    main()
