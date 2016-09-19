// TEST 4
// FizzBuzz
// [Marks]
//

// File manipulation
#include <fstream>
// Random generators
#include <cstdlib>
#include <ctime>
// Data manipulation
#include <string>
#include <vector>

using namespace std;

int main() {
    /* Generate test cases for FizzBuzz
     * qout_name       - The name of the question file to be outputted
     * aout_name       - The name of the answer file to be outputted
     * lim             - The upper limit of the number of data sets and queries
     * number_of_lines - The number of lines of FizzBuzz questions to output
     */
    const char qout_name[]     = "qout.txt";
    const char aout_name[]     = "aout.txt";
    const long lim             = 10000;
    const long number_of_lines = 10000;

    // Initialize random
    srand(time(NULL));

    // Open question file
    ofstream qout;
    qout.open(qout_name, ios::out | ios::trunc);
    // Open answer file
    ofstream aout;
    aout.open(aout_name, ios::out | ios::trunc);

    for (long line_no=0; line_no<number_of_lines; line_no++) {
        long range = rand() % lim + 1;
        long div1 = rand() % range + 1;
        long div2 = rand() % range + 1;
        qout << div1 << " " << div2 << " " << range << endl;
        for (long r=1; r<=range; r++) {
            string fb = "";
            if (r % div1 == 0) {
                fb += "F";
            }
            if (r % div2 == 0) {
                fb += "B";
            }
            if (fb.empty()) {
                fb = to_string(r);
            }
            aout << fb << " ";
        }
        aout << endl;
    }

    // Close files
    aout.close();
    qout.close();
}
