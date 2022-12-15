from prettytable import PrettyTable
from itertools import combinations
import time
import csv

MAX_CLIENT_WALLET = 500
CSV_FILE = "csv/actions.csv"
# CSV_FILE = "csv/dataset1.csv"
# CSV_FILE = 'csv/dataset2.csv'


def consult_csv():
    list_actions = []
    with open(CSV_FILE) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            list_actions.append((row[0], float(row[1]), float(row[2])))

        return list_actions


def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("\nDurée d'exécution : {:1.3}s\n\n".format(end_time - start_time))

    return wrapper


def best_actions_mix(list_actions):

    best_wallet = []
    best_income = 0

    for i in range(len(list_actions)):
        list_actions_mix = combinations(list_actions, i)

        for actions_mix in list_actions_mix:
            cost_price = wallet_cost(actions_mix)

            if cost_price <= MAX_CLIENT_WALLET:
                sum_profit = cumul_profit(actions_mix)

            if sum_profit > best_income:
                best_income = sum_profit
                best_wallet = actions_mix

    return best_wallet


def cumul_profit(actions_mix):
    total_profit = []
    for item in actions_mix:
        total_profit.append(item[1] * item[2] / 100)

    total_profit = sum(total_profit)
    return total_profit


def wallet_cost(actions_mix):
    total_price = []
    for item in actions_mix:
        total_price.append(item[1])

    total_price = sum(total_price)
    return total_price


def display(best_wallet):
    print("\n************************* AlgoInvest&Trade ****************************")
    print(
        f"\nMeilleur portefeuille d'actions pour un investissement de {MAX_CLIENT_WALLET} euros :\n"
    )

    table = PrettyTable()
    table.field_names = [
        "Action",
        "Coût par action (en euros)",
        "Bénéfice (en € après 2 ans)",
    ]
    for item in best_wallet:
        table.add_row([item[0], item[1], round(item[1] * item[2] / 100, 2)])
        # table.add_row(item)

    table.add_row([10 * "-", 26 * "-", 26 * "-"])
    table.add_row(
        [
            "Total",
            f"{round(wallet_cost(best_wallet),2)}€",
            f"+ {round(cumul_profit(best_wallet),2)}€",
        ]
    )

    print(table)


@execution_time
def main():
    display(best_actions_mix(consult_csv()))


if __name__ == "__main__":
    main()
