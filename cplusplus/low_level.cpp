#include <cpr/cpr.h>
#include <iostream>
#include <nlohmann/json.hpp>
using json = nlohmann::json;

int main(int argc, char **argv) {

  cpr::Response r =
      cpr::Get(cpr::Url{"http://127.0.0.1:8000"}, cpr::Bearer{"abracadabra"});

  json task_data = json::parse(r.text);
  return 0;
}
