#include <bits/stdc++.h>
using namespace std;

int32_t main() {
    string grid("012345678");
    do {
        cout<<grid<<'\n';
    } while (next_permutation(grid.begin(), grid.end()));
}
