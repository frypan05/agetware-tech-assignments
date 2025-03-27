#include<bits/stdc++.h>
using namespace std;

string formatIndianCurrency(double num) {
    stringstream ss;
    ss << fixed << setprecision(4) << num;
    string numStr = ss.str();

    string intPart = numStr.substr(0, numStr.find('.'));
    string decPart = numStr.substr(numStr.find('.'));

    int n = intPart.length();
    string result = "";

    int count = 0;
    for (int i = n - 1; i >= 0; i--) {
        result = intPart[i] + result;
        count++;
        
        if (i > 0) {
            if ((count == 3 && n > 3) || (count > 3 && (count - 3) % 2 == 0)) {
                result = "," + result;
            }
        }
    }

    return result + decPart;
}

int main() {
    double num;
    cout << "Enter a number: ";
    cin >> num;

    cout << "Formatted Indian Currency: " << formatIndianCurrency(num) << endl;
    return 0;
}
