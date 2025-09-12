#include "child/ChildInterface/bmi_child.hxx"
#include "bmi_grpc_server.h"


int main(int argc, char *argv[])
{
    printf("CHILD model grpc4bmi server\n");

    Model* model = new Model();

    {
        std::string model_name;
        model_name = model->GetComponentName();
        printf("%s\n", model_name.c_str());
    }

    delete model;
    return 0;
}
