class Manager:
    def __init__(self):
        self.actions = {}
        self.warehouse = []
        self.history = []
        self.balance = 0

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb

        return decorate

    def execute(self, name, *args, **kwargs):
        if name in self.actions:
            return self.actions[name](self, *args, **kwargs)
        else:
            print("Action not defined")

    def is_or_not(self, item):
        if len(self.warehouse) > 0:
            for i in self.warehouse:
                if i[0] == item:
                    return True

            return False
        else:
            return False

    def item_in(self, item):
        for i in self.warehouse:
            if i[0] == item:
                ilosc = i[1]['ilosc']
                return ilosc

    def item_cost(self, item):
        for i in self.warehouse:
            if i[0] == item:
                koszt = i[1]['koszt']
                return koszt


manager = Manager()


@manager.assign("balancee")
def balancee(manager, command_s):
    if command_s == 'd':
        add = input('Podaj kwotę do dodania: ')
        if add.isnumeric():
            add = float(add)
            manager.balance += add
            manager.history.append(f'Dodano {add}')
        else:
            print('Podano nieprawidłowe dane. Podaj liczbę.')
    elif command_s == 'o':
        sub = input('Podaj kwotę do odjęcia: ')
        if sub.isnumeric():
            sub = float(sub)
            if manager.balance - sub < 0:
                print('Nieprawidlowe dane. Saldo Twojego konta nie może być ujemne.')
            else:
                manager.balance -= sub
                manager.history.append(f'Odjeto {sub}')
        else:
            print('Podano nieprawidłowe dane. Podaj liczbę.')
    else:
        print('Nieprawidłowa komenda.')

    with open("balance.txt", "w") as text:
        text.write(str(manager.balance))


@manager.assign("purchase")
def purchase(manager):
    item = input('Podaj nazwę produktu: ').upper()
    quantity = int(input('Podaj ilość zakupionego produktu: '))
    cost = float(input('Podaj cenę produktu: '))
    if manager.is_or_not(item):
        for i in manager.warehouse:
            if manager.balance - quantity * cost < 0:
                print('Zakup nie jest możliwy. Brak środków.')
                break
            if i[0] == item and manager.balance - quantity * cost >= 0:
                if i[1]['koszt'] != cost:
                    print('Niestety. Podaleś różne ceny dla tego samego produktu.')
                    break

                print('Produkt już znajduje się w magazynie. Ilość poprawnie zmieniona.')
                i[1]['ilosc'] += quantity
                manager.history.append(f'Zaaktualizowano ilosc produktu {item} o {quantity}')
                manager.balance = manager.balance - quantity * cost
                manager.execute("wareh_write")
                break
    if not manager.is_or_not(item):
        if manager.balance - quantity * cost >= 0:
            manager.warehouse.append([item, {'ilosc': quantity, 'koszt': cost}])
            manager.history.append(f'Dodano produkt {item} w cenie {cost} w ilości {quantity}')
            manager.balance = manager.balance - quantity * cost
            manager.execute("wareh_write")
        else:
            print('Brak środków na pokrycie zakupu.')


@manager.assign("sell")
def sell(manager):
    item = input('Podaj nazwę produktu: ').upper()
    if manager.is_or_not(item):
        print('Produkt znajduje się w magazynie.')
        print(f'Mamy {manager.item_in(item)} sztuk. Ile pragniesz sprzedać?')
        quantity = int(input())
        if quantity > manager.item_in(item):
            print(f'Podano liczbę większą niz stan magazynu. Nie możesz sprzedać więcej niż {manager.item_in(item)}')
        else:
            manager.balance = manager.balance + manager.item_cost(item) * quantity
            for a in manager.warehouse:
                a[1]['ilosc'] -= quantity
                if item == a[0]:
                    if a[1]['ilosc'] <= 0:
                        manager.history.append(f'Sprzedano {quantity} sztuk przedmiotu {item}')
                        manager.warehouse.remove(a)
                        manager.execute("wareh_write")
                        break

                    else:
                        manager.history.append(f'Sprzedano {quantity} sztuk przedmiotu {item}')
                        manager.execute("wareh_write")
                        break
    else:
        print(f'Brak produktu {item} na stanie magazynu.')


@manager.assign("warehouse")
def warahouse(manager):
    if len(manager.warehouse) < 1:
        print('Magazyn jest pusty.')
    else:
        print('Stan magazynu:')
        for i in manager.warehouse:
            ilosc = i[1]['ilosc']
            koszt = i[1]['koszt']
            print(f'{i[0]}({ilosc}x) w cenie {koszt} za sztukę. Wartość łącznie: {ilosc * koszt}')


@manager.assign("balance_his")
def balance_his(manager):
    try:
        with open('balance.txt') as balan:
            manager.balance = float(balan.read())
    except:
        manager.balance = 0
    return manager.balance

@manager.assign("history")
def history(manager):
    if len(manager.history) > 0:
        print(f'Wykonano łącznie {len(manager.history)} operacji.')
        print('Możesz wybrać zakres operacji. ')
        print(f'Możliwy przedział to: 1 do {len(manager.history)}')
        od = input("Wprowadź numer operacji od której pragniesz zaczać.")
        if od.isnumeric() is False or int(od) < 1 or int(od) > len(manager.history):
            print(f'Błędna wartość. Możliwy przedział to: 1 do {len(manager.history)}')
            print('Wyświetlam wyniki od operacji pierwszej.')
            od = 1
        do = input("Wprowadź numer operacji na której pragniesz zakończyć.")
        if do.isnumeric() is False or int(do) > len(manager.history) or int(od) > int(do):
            print(f'Błędna wartość. Możliwy przedział to: 1 do {len(manager.history)}')
            print('Wyświetlam wyniki do samego końca.')
            do = int(len(manager.history))
        manager.execute("history_number", od, do)
    else:
        print("Historia wykonanych operacji jest pusta.")

@manager.assign("history_number")
def history_number(manager, od, do, a=0):
    od = int(od)
    do = int(do)
    if od > 0:
        for i in manager.history:
            a = a + 1
            if a < od or a > do:
                continue
            print(f'Opercja numer: {a} to  {i}')
            print('***************************************************')

@manager.assign("warehouse_actual")
def warehouse_actual(manager):
    try:
        if len(manager.warehouse) < 1:
            with open('warehouse.txt') as warehous:
                for line in warehous:
                    manager.warehouse.append(eval(line))
    except:
        pass
@manager.assign("warehouse_per_item")
def warehouse_per_item(manager):
    item = input('Podaj nazwę produktu: ').upper()
    if manager.is_or_not(item):
        for i in manager.warehouse:
            if i[0] == item:
                ilosc = i[1]['ilosc']
                cena = i[1]['koszt']
                print('Stan magazynu:')
                print(f'Dla produktu {item}, to {ilosc}. Cena jednej sztuki: {cena}.')

@manager.assign("wareh_write")
def wareh_write(manager):
    with open("warehouse.txt", "w") as file:
        for item in manager.warehouse:
            file.write(str(item) + "\n")

@manager.assign("history_file")
def history_file(manager):
    try:
        if len(manager.history) == 0:
            with open('history.txt') as file:
                for line in file:
                    x = line.strip()
                    manager.history.append(x)
    except:
        pass
