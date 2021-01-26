# Keystroke_Dynamics_Gen
This code is inspired by the one located in https://github.com/nileshprasad137/keystroke-dynamics-datagen but some changes were done. 

# Improvements
* Bug fixing: 
  * Some mistakes in the logic of the code were found and fixed
  * Append output dataset fixed to create CSV output.
* Dead code: Some lines of dead code were found and removed
* Code refactoring: Original code uses one single script to do all the tasks. The refactoring aimed to divide the script in functions in order to put them inside a Class. That brings the oportunity to create objects of that class to invoke its functions and make the integration with other apps easier.
* New features: 
  * Capability to set a custom quantity of sessions and reps per session was added. The original [dataset](https://www.cs.cmu.edu/~keystroke/) is set with 8 sessions and 50 reps per session.
  * Fields subject (user), sessionid and rep included in the output dataset.

# How to use
1) Clone the repo.
2) Open a Terminal window and run the file "main.py".
3) Set your user name, number of sessions and number of reps per session.
4) Type the word requested by the program.
5) When you have finished, you will see a message requesting you to press ESC to exit.
6) You will find a CSV file with your data in the output folder.

# Dependencies
In order to run the program you will need to use PIP to install the following modules:
* CSV Module
* Time Module
* Pyxhook Module

# License
This code is under the MIT License.
