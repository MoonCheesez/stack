// TEST 3
// Knapsack DP
// [Marks]
// 1 <= N <= 10      - 10m
// 1 <= N <= 10000   - 5m
// 1 <= N <+ 1000000 - 2m
// Tricky Cases - 2m
//
// Average time needed to produce file of N:
// N = 10      - 0.002s
// N = 10000   - 0.081s too long
// N = 1000000 - 7.668s too long

// File manipulation
#include <fstream>
// Random generators
#include <cstdlib>
#include <ctime>
// Data manipulation
#include <sstream>
#include <string>
#include <vector>
#include <numeric>
#include <algorithm>

#include <iostream>

using namespace std;

static const long LONG_WARNING_LIMIT = 4292967293;

/* Struct for large numbers
 * Large numbers are calculated by ax + c where:
 * a is the coefficient
 * x is LONG_WARNING_LIMIT
 * c is the constant
 *
 * Initialization:
 * coefficient - The coefficient of the number. (Default to 0)
 * constant    - The constant of the number.
 */
struct BigNumber {
    
    unsigned long coefficient;
    unsigned long constant;
    BigNumber(unsigned long constant, unsigned long coefficient=0) {
        this->coefficient = coefficient;
        this->constant = constant;
    }
    string getNumber() {
        return to_string((this->coefficient)*LONG_WARNING_LIMIT +
                          this->constant);
    }
};
            
int main() {
    /* Generate test cases for dp knapsack
     * qout_name - The name of the question file to be outputted
     * aout_name - The name of the answer file to be outputted
     * tmp_name  - The name of the temporary file to be created
     * lim       - The upper limit of the number of data sets and queries
     */
    const char qout_name[] = "qout.txt";
    const char aout_name[] = "aout.txt";
    const char tmp_name[]  = "tmp.txt";
    const long lim         = 10000;

    // Initialize random
    srand(time(NULL));

    // Open temp file
    fstream tmp;
    tmp.open(tmp_name, ios::out | ios::trunc | ios::in);

    // Create test cases
    long number_of_papers = lim;//rand() % lim + 1;
    unsigned long paper_sum = 0;
    vector<unsigned long> paper_sum_constants;
    for (int i=0; i<number_of_papers; i++) {
        long size = rand() % lim + 1;
        if (paper_sum + size > LONG_WARNING_LIMIT) {
            // size max is 1,000,000
            // vector at most 244 elements
            paper_sum_constants.push_back(paper_sum + size -
                                          LONG_WARNING_LIMIT);
            paper_sum = 0;
        } else {
            paper_sum += size;
        }
        tmp << to_string(size) << " " << to_string(rand() % lim + 1) << endl;
    }
    //   Calculate paper_sum
    const unsigned long paper_sum_constant = accumulate(
            paper_sum_constants.begin(), paper_sum_constants.end(), 0);
    const int paper_sum_coeff = paper_sum_constants.size();

    // Open question file
    fstream qout;
    qout.open(qout_name, ios::out | ios::trunc | ios::in);

    qout << to_string(rand() % (LONG_WARNING_LIMIT * paper_sum_coeff + 
            paper_sum + paper_sum_constant)) << endl;
    qout << to_string(number_of_papers) << endl;
    // Move tmp file pointer to beginning to read
    tmp.seekg(0, ios::beg);
    while (!tmp.eof()) {
        string line;
        getline(tmp, line);
        qout << line << endl;
    }

    // Close temp file and delete temp file
    tmp.close();
    remove(tmp_name);

    /* Start solving question */
    string line;

    // Reset file
    qout.seekg(0, ios::beg);

    // Get knapsack size
    getline(qout, line);
    long knapsack_size = stol(line);
    // Get number of items
    getline(qout, line);
    long number_of_lines = stol(line);
    // Get papers
    vector<vector<long>> papers;
    for (int i=0; i<number_of_lines; i++) {
        vector<long> cur;
        string val;
        
        getline(qout, line);
        stringstream linestream(line);
        
        getline(linestream, val, ' ');
        cur.push_back(stol(val));
        
        getline(linestream, val, ' ');
        cur.push_back(stol(val));

        papers.push_back(cur);
    }
    qout.close();
    // Finished reading data

    // Vectors to contain two lines of data
    vector<BigNumber> v1;
    vector<BigNumber> v2;
    // Fill with zeros
    v1.assign(knapsack_size+1, BigNumber(0));
    v2.assign(knapsack_size+1, BigNumber(0));
    // Assign for the first time
    fill(v1.begin()+papers[0][0], v1.end(), BigNumber(papers[0][1])); 

    for (vector<vector<long>>::iterator paper=papers.begin()+1;
            paper!=papers.end(); ++paper) {
        
        // v1 is the previous row
        // v2 is the current row
        long paper_size = (*paper)[0];
        long paper_val = (*paper)[1];

        for (long col=0; col<=knapsack_size; col++) {
            if (col < paper_size) {
                v2[col] = v1[col];
            } else {
                long leftover_space = col - paper_size;
                if (leftover_space < 0) {
                    leftover_space = 0;
                }
                // If choosing item <= not choosing item
                // If v1[leftover_space] + paper_val <= v2[col]
                if (paper_val + 
                        v1[leftover_space].coefficient * LONG_WARNING_LIMIT +
                        v1[leftover_space].constant <
                        v1[col].coefficient * LONG_WARNING_LIMIT +
                        v1[col].constant) {
                    v2[col] = v1[col];
                } else {
                    // Use the item
                    //cout << "Use item at" << col << endl;
                    if (paper_val + v1[leftover_space].constant >
                            LONG_WARNING_LIMIT) {
                        // Addition exceeds long limit
                        unsigned long new_constant = paper_val +
                            v1[leftover_space].constant - LONG_WARNING_LIMIT;
                        v2[col] = BigNumber(new_constant,
                                            v1[leftover_space].coefficient);
                    } else {
                        // Addition does not exceed long limit
                        v2[col] = v1[leftover_space];
                        v2[col].constant += paper_val;
                    }
                }
            }
        }
        v1.swap(v2);
    }

    // Write answer
    ofstream aout;
    aout.open(aout_name, ios::out | ios::trunc);
    aout << v1[knapsack_size].getNumber();
    aout.close();
}

