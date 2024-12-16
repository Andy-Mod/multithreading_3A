#include <Eigen/Dense>
#include <iostream>
#include <string>

using Eigen::MatrixXd;

class Task {
private:
  int id;
  std::string name;

public:
  // Constructor
  Task(int id, const std::string &name) : id(id), name(name) {}

  // Setter for ID
  void setId(int newId) { id = newId; }

  // Getter for ID
  int getId() const { return id; }

  // Setter for Name
  void setName(const std::string &newName) { name = newName; }

  // Getter for Name
  std::string getName() const { return name; }

  // Method to display class details
  void display() const {
    std::cout << "ID: " << id << ", Name: " << name << std::endl;
  }
};

int main() {
  Task obj(1, "Example");
  obj.display();

  obj.setId(2);
  obj.setName("Updated Example");
  obj.display();

  return 0;
}
