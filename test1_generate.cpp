// TEST 1
// Sally's calculator
// [Marks]
// 1 <= N <= 10         - 5m 
// 1 <= N <= 10000      - 5m 
// 1 <= N <= 1000000    - 2m
// Tricky Cases         - 2m
//
// Average time taken to produce each case (tricky=2)
// N = 10         - 0.002s
// N = 10000      - 0.029s
// N = 1000000    - 2.508s

// File manipulation
#include <fstream>
// Random generators
#include <cstdlib>
#include <ctime>
// Data manipulation
#include <vector>

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
   /* Generate test cases for Sally's calculator 
    * qout_name - The name of the question file to be outputted
    * aout_name - The name of the answer file to be outputted
    * lim       - The upper limit of the number of data sets and queries
    * tricky    - Whether or not calculator would be generated
    *
    * tricky == 0: no calculator
    * tricky == 1: always have calculator
    * tricky == 2: random (50%)
    */
    const char qout_name[] = "qout.txt";
    const char aout_name[] = "aout.txt";
    const long lim         = 10;
    const int  tricky      = 2;

    // Initialize random
    srand(time(NULL));

    // Open question file
    ofstream qout;
    qout.open(qout_name, ios::out | ios::trunc);

    // Open answer file
    ofstream aout;
    aout.open(aout_name, ios::out | ios::trunc);

    const long number_of_items = rand() % lim + 1;
    long calculator_position;

    if (tricky == 0) {
        calculator_position = -1;
    } else if (tricky == 1) {
        calculator_position = rand() % number_of_items;
    } else if (number_of_items){
        calculator_position = rand() % (2*number_of_items) -
            number_of_items;
        if (calculator_position < 0) {
            calculator_position = -1;
        }
    }

    aout << calculator_position + 1 << endl;
    aout.close();

    qout << number_of_items << endl;
    for (int i=0; i<number_of_items; i++) {
        if (i == calculator_position) {
            qout << "calculator" << endl;
        } else {
            qout << gibber() << endl;
        }
    }
    qout.close();    
}
