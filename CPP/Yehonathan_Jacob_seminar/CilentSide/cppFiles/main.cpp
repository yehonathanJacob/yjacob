#include <iostream>
#include <string>
#include "main.h"
#include "inputs.h"
#include "connections.h"
#include <string> 
#include <stdio.h>
#include <string.h>

using namespace std;

void get_data(char buf[]) {
	cin >> buf;
	return;
}

void log_in() {
	cout << "Loged In" << endl;
}

void denaid() {
	cout << "Denaid" << endl;
}
bool check(char buf[]){
	return buf == string("my_password");
}
int main()
{
	char buf[50];
	cout << "type password" << endl;
	get_data(buf);
	if (check(buf))
		log_in();
	else
		denaid();
	return 0;
}
// //Client.cpp
// class Person{
// public:
// 	void virtual print1(){ printf("In person 1\n");}
// 	void print2(){ printf("In person 2\n");}
// };

// class Profesor: public Person{
// public:
// 	void print1(){ printf("In Profesor 1\n");}
// 	void print2(){ printf("In Profesor 2\n");}
// };
// int main(int argc, char const *argv[])
// {
// 	Person *arr[2] = {new Person, new Profesor};	
// 	(*arr[0]).print1(); // expected In person 1
// 	(*arr[0]).print2(); // expected In person 2
// 	(*arr[1]).print1(); // expected In person 1 actual In Profesor 1
// 	(*arr[1]).print2(); // expected In person 2
// 	Profesor* pf1 = reinterpret_cast<Profesor*>(arr[1]);	
// 	pf1->print1(); // expected In Profesor 1
// 	pf1->print2(); // expected In Profesor 2
// 	return 0;
// }// CP: Yehonathan Jacob Seminar 2019












// class Person{
// public:
// 	Person(string name){ this->name = name; cout<< "in Person name is: " << name<< endl;}
// 	int sum(int a1,int a2){ return a1 + a2;}
// 	double sum(double a1,double a2){ return a1 + a2;} //overloading 
// 	string sum(string a1,string a2){ return a1 +" "+ a2;} //overloading 
// 	virtual string get_name(){return name;}
// private:
// 	string name;
// };

// class Profesor: public Person{
// public:
// 	Profesor(string name):Person(name){ cout<< "in Profesor" << endl;}
// 	string get_name(){return "Profesor: "+Person::get_name();}
// };

// int main(int argc, char const *argv[])
// {
// 	Person p1("Yehonathan"), *p2;
// 	Profesor pf1("Jacob");
// 	p2 = &pf1;
// 	cout << p1.sum("sum this ","text") << endl; //expected int sum(), overloaded string sum()
// 	cout << "name is: " << (*p2).get_name()<< endl; // expected "Jacob", overridden: "Profesor Jacob"
// 	return 0;
// }// CP: Yehonathan Jacob Seminar 2019

// class Parent
// {
// public:
// 	int get_val(){ return canNotAccess; }
// protected:
// 	void set_val(int val){cout << "in parent\n";canNotAccess = val; }
// private:
// 	int canNotAccess;
// };

// class Child: public Parent
// {
// public:
// 	void set_val(int val){ cout << "in child\n\t"; Parent::set_val(val); }
// };

// int main() {
// 	Child c;
// 	c.set_val(5);
// 	int output = c.get_val();
// 	cout << output;
	
//  }// CP: Yehonathan Jacob Seminar 2019

