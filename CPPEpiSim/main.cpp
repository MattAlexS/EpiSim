#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <vector>
#include <typeinfo>
#include <math.h>


using namespace std;

int main () {
  //modifiable parameters
  srand(123);
  int sample_total = 100;
  int num_nodes = 303;
  int num_graphs = 30;
  string profile_name = "WDG-July.dat";
  string path = "Graphs/303node31pack/";
  string statfile_name = "303n31pBurnInSimStats.csv";
  //modifiable parameters

  //read in profile
  string profile_filename = path + profile_name;
  ifstream infile(profile_filename);
  vector<int> profile;
  if (infile.is_open()) {
    int a;
    while (infile >> a) {
      profile.push_back(a);
      cout << a << " ";
    }
    infile.close();
  }

  else {
    cout << "Unable to open file";
  }
  //read in profile

  //read in graphs
  map<int, map<int, vector<int> > > m;
  for (int i = 0; i < num_graphs; i++) {
    string num = to_string(i);
    string file = "Graph" + num + ".grf";
    cout << "Reading in: " << file << "\n";
    string file_name = path + file;
    ifstream infile(file_name);
    map<int, vector<int> > graph;
    for (int x = 0; x < num_nodes; x++) {
      vector<int> vect;
      graph[x] = vect;
    }
    if (infile.is_open()) {
      int a, b;
      while (infile >> a >> b) {
        graph[a].push_back(b);
        graph[b].push_back(a);
      }
      infile.close();
      m[i] = graph;
    }

    else {
      cout << "Unable to open file";
    }
  }
  //read in Graphs

  ofstream statfile;
  statfile.open (statfile_name);
  //map<int, vector <vector <double> > > output;
  //run epidemic simulation
  for (int i = 0; i < num_graphs; i++) {
    cout << "Simulating " << i << "\n";
    statfile << "Graph" << i << ".grf\n";
    //vector<vector<double> > nodes;
    for (int node = 0; node < num_nodes; node++) {
      //vector<double> samples;
      for (int sample = 0; sample < sample_total; sample++) {
        //define model states//
        vector<bool> sus(303);
        sus.flip();
        vector<bool> exp(303);
        vector<bool> eprime(303);
        vector<bool> asy(303);
        vector<bool> inf(303);
        vector<bool> rem(303);
        //define model states//

        //define state transition probabilities
        float se = 0.09;
        float ee = 0.2033;
        float ei = 0.3935 * 0.8;
        float ea = 0.3935 * 0.2;
        float ir = 0.1331;
        float top = RAND_MAX;
        float r;
        //define state transition probabilities

        //set patient zero
        eprime[node] = true;
        sus[node] = false;
        //set patient zero
        double value;
        int rmse = 0;
        //burn in
        int burn_in = 0;
        int burn_max = 10;
        int infections = 0;
        while (infections == 0 && burn_in < burn_max) {
          vector<int> to_be_inf;
          int daily_inf = 0;
          for (int scan = 0; scan < num_nodes; scan++) {
            if (eprime[scan] == true || asy[scan] == true || inf[scan] == true) {
              for (int neighbor = 0; neighbor < m[i][scan].size(); neighbor++) {
                if (sus[m[i][scan][neighbor]] == true) {
                  to_be_inf.push_back(m[i][scan][neighbor]);
                }
              }
            }
          }
          //check who will be exposed

          //Update states
          for (int scan = 0; scan < num_nodes; scan++) {
            //INFECTED --> REMOVED
            if (inf[scan] == true) {
              r = rand() / top;
              if (r <= ir) {
                inf[scan] = false;
                rem[scan] = true;
              }
            }
            //INFECTED --> REMOVED

            //ASYMPTOMATIC --> REMOVED
            else if (asy[scan] == true) {
              r = rand() / top;
              if (r <= ir) {
                asy[scan] = false;
                rem[scan] = true;
              }
            }
            //ASYMPTOMATIC --> REMOVED

            //EXPOSED PRIME --> INFECTED
            else if (eprime[scan] == true) {
              r = rand() / top;
              if (r <= ei) {
                eprime[scan] = false;
                inf[scan] = true;
                infections++;
              }
              //EXPOSED PRIME --> INFECTED

              //EXPOSED PRIME --> ASYMPTOMATIC
              else if ( r <= (ei + ea)) {
                eprime[scan] = false;
                asy[scan] = true;
              }
            }
            //EXPOSED PRIME --> ASYMPTOMATIC

            //EXPOSED --> EXPOSED PRIME
            else if (exp[scan] == true) {
              r = rand() / top;
              if (r <= (ee)) {
                exp[scan] = false;
                eprime[scan] = true;
              }
            }
            //EXPOSED --> EXPOSED PRIME
          }
          //SUSCEPTIBLE --> EXPOSED
          for (int scan = 0; scan < to_be_inf.size(); scan++) {
            if (sus[to_be_inf[scan]] == true) {
              r = rand() / top;
              if (r <= se) {
                sus[to_be_inf[scan]] = false;
                exp[to_be_inf[scan]] = true;

              }
            }
          }
          burn_in++;
        }
        rmse += ((infections - profile[0]) * (infections - profile[0]));
        //burn in


        for (int day = 1; day < profile.size(); day++) {
          //check who will be exposed
          vector<int> to_be_inf;
          int daily_inf = 0;
          for (int scan = 0; scan < num_nodes; scan++) {
            if (eprime[scan] == true || asy[scan] == true || inf[scan] == true) {
              for (int neighbor = 0; neighbor < m[i][scan].size(); neighbor++) {
                if (sus[m[i][scan][neighbor]] == true) {
                  to_be_inf.push_back(m[i][scan][neighbor]);
                }
              }
            }
          }
          //check who will be exposed

          //Update states
          for (int scan = 0; scan < num_nodes; scan++) {
            //INFECTED --> REMOVED
            if (inf[scan] == true) {
              r = rand() / top;
              if (r <= ir) {
                inf[scan] = false;
                rem[scan] = true;
              }
            }
            //INFECTED --> REMOVED

            //ASYMPTOMATIC --> REMOVED
            else if (asy[scan] == true) {
              r = rand() / top;
              if (r <= ir) {
                asy[scan] = false;
                rem[scan] = true;
              }
            }
            //ASYMPTOMATIC --> REMOVED

            //EXPOSED PRIME --> INFECTED
            else if (eprime[scan] == true) {
              r = rand() / top;
              if (r <= ei) {
                eprime[scan] = false;
                inf[scan] = true;
                daily_inf++;
              }
              //EXPOSED PRIME --> INFECTED

              //EXPOSED PRIME --> ASYMPTOMATIC
              else if ( r <= (ei + ea)) {
                eprime[scan] = false;
                asy[scan] = true;
              }
            }
            //EXPOSED PRIME --> ASYMPTOMATIC

            //EXPOSED --> EXPOSED PRIME
            else if (exp[scan] == true) {
              r = rand() / top;
              if (r <= (ee)) {
                exp[scan] = false;
                eprime[scan] = true;
              }
            }
            //EXPOSED --> EXPOSED PRIME
          }
          //SUSCEPTIBLE --> EXPOSED
          for (int scan = 0; scan < to_be_inf.size(); scan++) {
            if (sus[to_be_inf[scan]] == true) {
              r = rand() / top;
              if (r <= se) {
                sus[to_be_inf[scan]] = false;
                exp[to_be_inf[scan]] = true;

              }
            }
          }
          //SUSCEPTIBLE --> EXPOSED

          //sum squared error
          rmse += ((daily_inf - profile[day])*(daily_inf - profile[day]));
          //sum squared error
        }
        //append root mean squared error
        value = sqrt(rmse)/sqrt(profile.size());
        statfile << value << ",";
        //samples.push_back(sqrt(rmse)/sqrt(profile.size()));
        //append root mean squared error
      }
      //append all samples at a node
      statfile << "\n";
      //nodes.push_back(samples);
      //append all samples at a node
    }
    //store node data for each graph
    //output[i] = nodes;
  }
  statfile.close();
  return 0;
}
