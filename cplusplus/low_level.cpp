#include "Eigen/Dense"
#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>

#include <string>

using json = nlohmann::json;
using namespace std;

class Task {
private:
  Eigen::MatrixXf A;
  Eigen::VectorXf b;
  Eigen::VectorXf x;
  string identifier;

public:
  Task(std::string answer) {
    json task_data;

    task_data = json::parse(answer);

    auto matrixA = task_data["a"];
    auto matrixb = task_data["b"];

    int rowsA = matrixA.size();
    int colsA = matrixA[0].size();
    A.resize(rowsA, colsA);

    for (int i = 0; i < rowsA; i++)
      for (int j = 0; j < colsA; j++)
        A(i, j) = matrixA[i][j];

    int rowsb = matrixb.size();
    b.resize(rowsb);

    for (int i = 0; i < rowsb; i++)
      b(i) = matrixb[i];

    x.resize(rowsb);

    identifier = task_data["identifier"];
  }

  void work(void) { x = A.colPivHouseholderQr().solve(b); }

  Eigen::VectorXf get_x(void) { return x; }

  Eigen::MatrixXf get_A(void) { return A; }

  Eigen::VectorXf get_b(void) { return b; }

  string get_identifier(void) { return identifier; }

  json to_json(void) {
    // json out = {{"a", A}, {"b", b}, {"x", x}, {"identifier", identifier}};
  }
};

Task get_task(string URL, string ACCESS_KEY) {
  cpr::Response r = cpr::Get(cpr::Url{URL}, cpr::Bearer{ACCESS_KEY});

  if (r.status_code != 200) {
    std::cerr << "HTTP request failed with status: " << r.status_code
              << std::endl;
    exit(EXIT_FAILURE);
  }

  Task task(r.text);
  return task;
}

void do_task_then_post_result(Task task, string URL) {
  task.work();
  json post_data;

  post_data["identifier"] = task.get_identifier();
  post_data["a"] = post_data["b"] = post_data["x"] =

      cpr::Response r =
          cpr::Post(cpr::Url{URL}, cpr::Body{post_data.dump()},
                    cpr::Header{{"Content-Type", "application/json"}});
}

int main(int argc, char **argv) {

  string URL = "http://127.0.0.1:8000";
  string ACCESS_KEY = "abracadabra";

  return 0;
}
