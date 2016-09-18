// TEST 2
// SDM Database Retrieval
// [Marks]
// 1 <= S <= 10;Q = 1           - 20m
// 1 <= S <= 10000;Q = 1000     - 10m
// 1 <= S <= 1000000;Q = 100000 - 2m
// Tricky Cases                 - 2m

// File manipulation
#include <fstream>
// Random generators
#include <cstdlib>
#include <ctime>
#include <algorithm>
// Data manipulation
#include <string>
#include <vector>
#include <deque>

using namespace std;

vector<char> alphabets = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                          'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                          's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
string gibber(bool space=false, int min_len=5, int max_len=10) {
    /* Generates gibberish text
     * space   - Whether or not to include space. (Default to false)
     * min_len - Minimum length of the string. (Default to 5)
     * max_len - Maximum length of the string. (Default to 10)
     */

    if (space) {
        alphabets.push_back(' ');
    }

    int gibber_len = rand() % (max_len-min_len+1) + min_len;
    string text = "";
    for (int i=0; i < gibber_len; i++) {
        text += alphabets[rand() % (alphabets.size())];
    }
    if (space) {
        alphabets.pop_back();
    }
    return text;
}

int main() {
    /* Generate test cases for database retrieval
     * qout_name - The name of the question file to be outputted
     * aout_name - The name of the answer file to be outputted
     * lim       - The uppper limit of the number of data sets and queries
     */
    const char qout_name[] = "qout.txt";
    const char aout_name[] = "aout.txt";
    const long lim         = 1000;
    
    // Initialize random
    srand(time(NULL));

    // Open question file
    ofstream qout;
    qout.open(qout_name, ios::out | ios::trunc);
    // Open answer file
    ofstream aout;
    aout.open(aout_name, ios::out | ios::trunc);

    const long S = 10000;//rand() % lim + 1;
    const long Q = 9999;//rand() % S + 1;

    qout << S << endl << Q << endl;

    deque<long> queried;
    for (long i = 0; i < S; i++) queried.push_back(i);
    random_shuffle(queried.begin(), queried.end());
    queried.erase(queried.begin()+Q, queried.begin()+S);
    
    vector<string> names;
    string query_text = "";
    // Generate people
    for (long i = 0; i < S; i++) {
        string name = gibber(true);
        while (find(names.begin(), names.end(), name) != names.end()) {
            name = gibber(true);
        }
        names.push_back(name);
        string c = gibber(false, 4, 4);
        string index = to_string(rand() % 25 + 1);
        string grade = to_string(rand() % 101);

        qout << name << endl << c << endl;
        qout << index << endl << grade << endl;
        qout << endl;

        // Generate query
        if (i == queried[0]) {
            queried.pop_front();
            string attribute;
            int att = rand() % 3;
            switch (att) {
            case 0:
                attribute = "CLASS";
                aout << c << endl;
                break;
            case 1:
                attribute = "INDEX_NO";
                aout << index << endl;
                break;
            case 2:
                attribute = "GRADE";
                aout << grade << endl;
                break;
            }
            query_text += name + "\n" + attribute + "\n\n";
        }
    }

    // Write the queries
    qout << query_text;

    // Close files
    qout.close();
    aout.close();
}
