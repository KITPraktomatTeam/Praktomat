A very small readme for Praktomat feature "C/C++ UnitChecker 2" by Robert.Hartmann@h-brs.de

After cloning (installing) Praktomat semester instance
Update DIRS variable in bash script 
         Praktomat/src/checker/scripts/cTestrunner
(line 24) with suitable path information

Bash scripts 
- Praktomat/src/checker/scripts/cTestrunner
- Praktomat/src/checker/scripts/dressObjects
- Praktomat/src/checker/scripts/findMainInObject
have to be execuable for right user or usergroup.


Praktomat-Checker
- Praktomat/src/checker/checker/CUnitChecker_v2.py (Unit Checks for C and CPP)
- Praktomat/src/checker/compiler/CLinker.py (create an executable or shared object from objectfiles)
with modificated
- Praktomat/src/checker/compiler/Builder.py
- Praktomat/src/checker/compiler/CBuilder.py
- Praktomat/src/checker/compiler/CXXBuilder.py


and above listed Bash scripts needs
- bash
- ulimit
- nm, objcopy (from GNU Binutils)
- gcc , g++
- fusermount, bindfs, fakechroot
- grep, read


"C/C++ UnitChecker 2" can run with CUnit 2.1-3 , CppUnit 1.12.1
      sudo apt install libcunit1-dev libcppunit-dev 


If you find any this "C/C++ UnitChecker 2" feature related problems or bugs
please write a mail to 
     praktomat@inf.h-brs.de

Template for bug report for feature CunitCppUnit_Checker:

=================
summary:

component (which Checker, script, ...) :

What did you do? (steps to reproduce) :

What happened? (actual results) :

What should happened? (expected results) :

Your python version ( $ python --version ) :

Your python environment ( $ pip freeze ) :

=================
