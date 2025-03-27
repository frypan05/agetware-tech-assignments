#include<bits/stdc++.h>
using namespace std;

void findMinLoss(vector<int>& prices) {
    int minLoss = INT_MAX;
    int buyYear = -1, sellYear = -1;

    for (int i = 0; i < prices.size(); i++) {
        for (int j = i + 1; j < prices.size(); j++) {
            if (prices[j] < prices[i]) {
                int loss = prices[i] - prices[j];
                if (loss < minLoss) {
                    minLoss = loss;
                    buyYear = i + 1;
                    sellYear = j + 1;
                }
            }
        }
    }

    if (buyYear != -1 && sellYear != -1) {
        cout << "Buy in year " << buyYear << " and sell in year " << sellYear << " with a loss of " << minLoss << endl;
    } else {
        cout << "No valid loss found" << endl;
    }
}

int main() {
    int n;
    cout << "Enter number of years: ";
    cin >> n;

    vector<int> prices(n);
    cout << "Enter house prices for " << n << " years: ";
    for (int i = 0; i < n; i++) {
        cin >> prices[i];
    }

    findMinLoss(prices);

    return 0;
}