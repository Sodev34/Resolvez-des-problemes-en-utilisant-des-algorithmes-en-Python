from prettytable import PrettyTable
import time
import csv

MAX_CLIENT_WALLET = 500
CSV_FILE = "csv/actions.csv"
# CSV_FILE = "csv/dataset1.csv"
# CSV_FILE = "csv/dataset2.csv"


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


def best_actions(list_actions):
    best_wallet = []
    cumul_profit = 0
    wallet_cost = 0

    actions_list_sorted = sorted(
        #list_actions, key=lambda x: x[1] * x[2] / 100, reverse=True,
        list_actions, key=lambda x: x[2], reverse=True,
    )

    for action in actions_list_sorted:
        if (wallet_cost + action[1]) <= MAX_CLIENT_WALLET and action[1] > 0:
            best_wallet.append(action)
            wallet_cost += action[1]
            cumul_profit += action[2]

    # print(best_wallet)
    return best_wallet


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

    table.add_row([10 * "-", 26 * "-", 26 * "-"])
    table.add_row(
        [
            "Total",
            f"{round(sum(item[1] for item in best_wallet), 2)}€",
            f"+{round(sum(item[1] * item[2]/100 for item in best_wallet), 2)}€",
        ]
    )

    print(table)


@execution_time
def main():
    display(best_actions(consult_csv()))
    # best_actions(consult_csv())


if __name__ == "__main__":
    main()
