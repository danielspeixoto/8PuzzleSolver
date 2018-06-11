#include <bits/stdc++.h>
using namespace std;

struct State {
    string to_string() const;
    string to_readable_string() const;
    static bool populate_from_string(State& state, const string& str);
    bool is_goal() const;

    array<array<int, 3>, 3> grid;
};

string State::to_string() const {
    string str;
    for (int i = 0; i < 3; ++i)
        for (int j = 0; j < 3; ++j)
            str.push_back('0'+grid[i][j]);
    return str;
}

string State::to_readable_string() const {
    string str;
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            str.push_back(grid[i][j] == 0 ? '.' : '0'+grid[i][j]);
        }
        str.push_back('\n');
    }
    return str;
}

bool State::populate_from_string(State& state, const string& str) {
    if (str.size() != 9)
        return false;
    for (int i = 0; i < 9; ++i) {
        if (str[i] < '0' || str[i] > '8')
            return false;
        state.grid[i / 3][i % 3] = str[i] - '0';
    }
    return true;
}

bool State::is_goal() const {
    array<array<int, 3>, 3> goal_grid{
        array<int, 3>{0, 1, 2},
        array<int, 3>{3, 4, 5},
        array<int, 3>{6, 7, 8}
    };
    return grid == goal_grid;
}

bool operator<(const State& lhs, const State& rhs) {
    return lhs.grid < rhs.grid;
}

vector<State> get_neighbors(const State& state) {
    int pi = -1, pj = -1;
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            if (state.grid[i][j] == 0) {
                pi = i;
                pj = j;
            }
        }
    }
    if (pi == -1) {
        throw std::runtime_error("invalid state: missing space");
    }
    const vector<pair<int, int>> displacements{{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    vector<State> neighbors;
    for (const auto& displacement : displacements) {
        const int new_pi = pi + displacement.first;
        const int new_pj = pj + displacement.second;
        if (0 <= new_pi && new_pi < 3 && 0 <= new_pj && new_pj < 3) {
            State new_state(state);
            swap(new_state.grid[pi][pj], new_state.grid[new_pi][new_pj]);
            neighbors.push_back(new_state);
        }
    }
    return neighbors;
}

struct Node {
    Node *const parent;
    const State state;
    const int distance;
};

vector<Node*> retrieve_history(Node* node) {
    vector<Node*> history;
    while (node != nullptr) {
        history.push_back(node);
        node = node->parent;
    }
    reverse(history.begin(), history.end());
    return history;
}

void solve(const State& initial_state, const bool detailed) {
    vector<unique_ptr<Node>> node_pool;
    Node *initial_node = new Node{nullptr, initial_state, 0};
    node_pool.emplace_back(initial_node);
    Node *final_node = nullptr;
    int explored_states = 0;
    if (initial_state.is_goal()) {
        final_node = initial_node;
    } else {
        set<State> visited;
        queue<Node*> q;
        visited.insert(initial_node->state);
        q.push(initial_node);
        while (!q.empty()) {
            Node *node = q.front();
            q.pop();
            //if (detailed) {
                //cout<<"Exploring state:"<<endl;
                //cout<<node->state.to_readable_string();
            //}
            ++explored_states;

            for (const State& new_state : get_neighbors(node->state)) {
                if (visited.insert(new_state).second) {
                    Node *new_node = new Node{node, new_state, node->distance+1};
                    node_pool.emplace_back(new_node);
                    if (new_state.is_goal()) {
                        final_node = new_node;
                        break;
                    }
                    q.push(new_node);
                }
            }

            if (final_node != nullptr) {
                break;
            }
        }
    }
    // Print response
    if (final_node == nullptr) {
        cout<<"No solution."<<endl;
    } else {
        cout<<"Solution in "<<final_node->distance<<" step(s)."<<endl;
        if (detailed) {
            cout<<"States explored: "<<explored_states<<"."<<endl;
            for (Node* node : retrieve_history(final_node)) {
                cout<<"---"<<endl;
                cout<<node->state.to_readable_string();
            }
        }
    }
}

int32_t main(int argc, char** argv) {
    // Read command-line arguments
    bool detailed = false;
    if (argc == 2 && string(argv[1]) == "detailed") {
        detailed = true;
    }
    // Read input
    string line;
    cin>>line;
    State initial_state;
    if (!State::populate_from_string(initial_state, line)) {
        cerr<<"Invalid input."<<endl;
        return 1;
    }
    // Solve instance
    solve(initial_state, detailed);
}
