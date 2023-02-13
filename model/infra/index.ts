import * as awsx from "@pulumi/awsx";
import * as pulumi from "@pulumi/pulumi";
import * as k8s from "@pulumi/kubernetes";
import * as kx from "@pulumi/kubernetesx";
import TraefikRoute from './TraefikRoute';
import S3ServiceAccount from './S3ServiceAccount';

const config = new pulumi.Config()
// Create a repository.
const repo = new awsx.ecr.Repository("model");
const appImage = repo.buildAndPushImage(`../`);

//Read base pulumi project

const baseStack= new pulumi.StackReference("ssaeed/Downloads/mlplatform")



// Create a k8s provider.
const provider = new k8s.Provider("provider", {
    kubeconfig: baseStack.getOutput("kubeconfig"),
    
});

// Define the Pod for the Deployment.
const pb = new kx.PodBuilder({
    containers: [{
        image: appImage,
        ports: { "http": 80 },
        env:{
            "MLFLOW_TRACKING_URI":"http://ml.mlplatform.click/mlflow"
            "MLFLOW_RUN_ID":config.require("runID")
        }
    }],

    serviceAccountName: baseStack.getOutput("modelsServiceAccount"),

});

// Create a Deployment of the Pod defined by the PodBuilder.
const appDeploymentKx = new kx.Deployment("app-kx", {
    spec: pb.asDeploymentSpec(),
}, { provider: provider });


const service= appDeploymentKx.createService();

new TraefikRoute('my-model-route', {
    prefix: '/models/model ',
    service: service
    namespace: 'default',
  }, { provider: provider});





export const kubeconfig= cluster.kubeconfig

