#include <iostream>
#include <fstream>
#include <vector>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cctype>
#include <cmath>
#include <ctime>

using namespace std;

#include "setu.h"

//Decay parameter for diffusion character   0.5 is a special value
#define omega 0.5

int main(){
  int Z;

  for (int verts = 405; verts < 406; verts +=20){
    for (int samp = 39; samp < 50; samp ++){
      Z = verts;
      string filename = "PlCgraphs/" + to_string(verts) + "PLC" + to_string(samp) + ".grf";
      ifstream infile(filename);

      double M[Z][Z];  //diffusion character matrix [vextex][gas]
      double Ent[Z];   //entropy vector


      graph G(Z);  //Graph variable
      int i,j;     //loop index variables
      double E;    //entropy accumulator

      G.readadj(infile, Z); //read a python adjacency graph
      //G.Pn(64,7);      //create a graph -- read in python adj. list here
      //G.toggle(1,10);  //break the symmetry
      for(i=0;i<G.size();i++){//loop over the vertices
        G.DiffChar(i,omega,M[i]);  //compute the diffusion character for vertex i
      }

      for(i=0;i<G.size();i++){//loop over vertices
        E=0.0;  //prepare E for normalizing
        for(j=0;j<G.size();j++)E+=M[i][j];  //total the amount of gas at vertex i
        for(j=0;j<G.size();j++)M[i][j]/=E;  //normalize so sum(gas)=1
        E=0.0;  //zero the entropy accumulator
        for(j=0;j<G.size();j++){//build up the individual entropy terms
          E+=-M[i][j]*log(M[i][j]);  //this is entropy base E
        }
        Ent[i]=E/log(2);  //convert entropy to Log base 2
      }

      //Now sort the entropy vector
      do {//swap out-of-order entries
        j=0;  //no swaps
        for(i=0;i<G.size()-1;i++)if(Ent[i]<Ent[i+1]){
          E=Ent[i];Ent[i]=Ent[i+1];Ent[i+1]=E;  //swap
          j=1;  //set the flag that a swap happened
        }
      }while(j==1); //until in order

      ofstream outfile;
      string outfile_name = "PLCdcs/" + to_string(verts) + "PLC" + to_string(samp) + ".dc";
      outfile.open(outfile_name);
      outfile << Ent[0];
      for(i=1;i<G.size();i++)outfile << "," << Ent[i];
      outfile << endl;
      outfile.close();
      //Now we have the diffusion characters
    }
  }
  return 0;
}
