import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import sys


def main():
    observation, target_months = get_data()
    time_period = [1, 2, 3, 4, 5, 6, 7, 8]
    alpha = input("Enter alpha between [0-1], q=quit, c= create csv:")


    try:
        while True:
            final_forecast = []
            if alpha == "q":
                print("+++ program exiting")

                return
            elif alpha =="c":
                if len(final_forecast) == 0:
                    print("There is no existing forecast")
                print("+++ creating csv file as forecast")
                break
            elif 0 <= float(alpha) <= 1:
                forecast = smoothing(observation, float(alpha))
                print(forecast)
                plot_chart(observation, forecast, time_period)

                print("good", end="")
            else:
                print("invalid option", end=" ")

            alpha = input(" Try another alpha[0-1]:")
    except Exception as e:
        print(e)
        sys.exit(0)


def get_data():
    df = pd.read_csv("HistoricalQuotes.csv")

    target_year = "2017"
    target_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']  # 8 months

    df['date'] = pd.to_datetime(df['date'])
    df['Year'] = df['date'].apply((lambda x: x.strftime("%Y")))
    df['Month'] = df['date'].apply((lambda x: x.strftime("%b")))

    df2 = df.groupby(["Year", 'Month'])

    observation = [
        (df2.get_group((target_year, month))['close'].iloc[-1])
        for month in target_months
    ]

    return observation, target_months


def smoothing(data, alpha):
    F = [data[0]]
    # F.extend([data[0], data[0]])

    # k = [1195, 1349, 2265,  2304, 2732, 2130, 1971, 1312, 1268]
    # j = [1195.00, 1195.00]
    # alpha = 0.25
    damping = 1 - alpha
    # forecast = []
    forecast = data[0]

    for x in data[1:]:
        forecast = (alpha * x) + (damping * forecast)
        F.append(forecast)

    return F


def plot_chart(observation, forecast, time_period):
    plt.plot(time_period, observation, color='red', label='stock value')
    plt.plot(time_period, forecast, color='blue', label='forecast value')

    plt.xlabel("Time Period")
    plt.ylabel("Stock Price [USD]")
    plt.title("Cisco Stock Price")
    plt.legend()
    plt.show()



if __name__ == '__main__':
    main()