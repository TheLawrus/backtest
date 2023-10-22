# CardinalTradingSystem

This is just a short start on our backtesting system.

## Usage

1. First you want to generate your own factors.
   
You want to create a .csv file that has n rows and m columns, where n = number of backtesting time frame and m = number of tickers.
It should look something like this.
![image](https://github.com/Cardinal-Trading-UW-Madison/EDA/assets/127585484/6ff74dfd-c5cf-4ffb-bc38-51a71831bcb3)
Read get_RSI.py for detailed instructions.

2. Start backtesting!

You can simply run main.py.
![image](https://github.com/Cardinal-Trading-UW-Madison/EDA/assets/127585484/81199f71-441f-47d7-9c60-0f1ca7c01a39)
Basically all you should change is just the step which loads the factors for picking the tickers with highest factor values.
In the given example the index starts at 14 because the RSI factor requires the previous two weeks of data to be calculated.
If your factor only uses the current day information, feel free to change it to 1 or something else that fits.
And then voilà! Here is our first plot of the backtesting result:
![image](https://github.com/Cardinal-Trading-UW-Madison/EDA/assets/127585484/06cdad1f-0fd9-4a19-9418-7eec1ccb89bb)
Looks pretty ugly for now, but we are going to plot something really cool like this one day (hopefully).
![image](https://github.com/Cardinal-Trading-UW-Madison/EDA/assets/127585484/96633fe4-e38e-4e22-9c59-ae9a6cc2bcaa)



## Contributing

* Help improve the logic of backtesting
* Help improve the runtime by optimizing the algorithm
* Generate new strategy to make use of factors
