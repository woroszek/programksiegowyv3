from func import manager


while True:
    manager.execute("balance_his")
    manager.execute("history_file")
    manager.execute("warehouse_actual")
    print('Podaj komendę. Wpisz pomoc, jeśli chcesz zobaczyć dostępne komendy')
    command = input().lower()
    if command == 'pomoc':
        print('s - dodanie lub odjecie kwoty z konta')
        print('z - zakup')
        print('sp - sprzedaż')
        print('sk - stan konta')
        print('st - stan magaznu')
        print('m - stan magazynu dla konkretnego produktu')
        print('h - historia działań aplikacji')
        print('k - zamknięcie programu')

    if command == 's':
        print('Wpisz: D, jeśli chcesz dodać lub O, jeśli odjać: ')
        command_s = input().lower()
        manager.execute("balancee", command_s)

    if command == 'z':
        manager.execute("purchase")

    if command == 'sp':
        manager.execute("sell")

    if command == 'sk':
        print(f'Stan Twojego konta to: {manager.balance}')

    if command == 'st':
        manager.execute("warehouse")

    if command == 'm':
        manager.execute("warehouse_per_item")

    if command == 'h':
        manager.execute("history")

    if len(manager.history) > 0:
        with open("history.txt", "w") as file:
            for item in manager.history:
                file.write(str(item) + '\n')

    with open("balance.txt", "w") as text:
        text.write(str(manager.balance))

    if command == 'k':
        break
