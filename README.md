# A basic Oshinko example app with Word2Vec

## Setup OpenShift

    oc cluster up

## Setup Oshinko

    : Launch Oshinko from a template
    oc new-app -f http://goo.gl/ZU02P4
    : Authorize Oshinko to create clusters
    oc policy add-role-to-user edit -z oshinko

## Source-to-image (S2I) to launch the app

    : Case0: [image]~[remote source code]
    oc new-app radanalyticsio/radanalytics-pyspark:pre-cli~https://github.com/mattf/py-smoke

    : Case1: [remote source repo] --docker-image
    oc new-app https://github.com/mattf/py-smoke --docker-image=radanalyticsio/radanalytics-pyspark:pre-cli

    : Case2: [image]~[local source repo] --docker-image
    git clone https://github.com/mattf/py-smoke
    oc new-app radanalyticsio/radanalytics-pyspark:pre-cli~py-smoke

    : Case3: [local source repo] --docker-image
    git clone https://github.com/mattf/py-smoke
    oc new-app py-smoke --docker-image=radanalyticsio/radanalytics-pyspark:pre-cli

    : Case4: --template
    oc create -f https://raw.githubusercontent.com/radanalyticsio/oshinko-s2i/master/pyspark/pysparkbuilddc.json
    : configmap needed until https://github.com/radanalyticsio/oshinko-s2i/pull/68 is merged
    oc create configmap oshinko-spark-driver-config
    oc new-app --template=oshinko-pyspark-build-dc -p GIT_URI=https://github.com/mattf/py-smoke -lapp=py-smoke
    oc create service clusterip py-smoke --tcp=8080

    : Case: --file
    : TODO

## Make sure it worked

    : This will return "Connection refused" while the app builds and starts. This can take 5-10 minutes depending on your network speed. It's much faster the second time.
    links -dump $(oc get svc/py-smoke --template='{{.spec.clusterIP}}:{{index .spec.ports 0 "port"}}')


# Notes

### Two user experiences - *CLI* and *Console*

The user experiences should have parity. Parity is missing in a few cases and with a caveat -

* Parity gap: the CLI process automatically creates a Service
* Parity gap: the CLI requires oshinko-rest
* Parity gap: the Console allows for overriding APP_FILE
* Parity gap: the Console process uses forcePull for the builder image
* Parity gap: the resource labeling differs
* Caveat: it is assumed all Parameters on the Console S2I template can be provided as Environment variables to the CLI process

### The curious case of oshinko-rest

The pod that comes out of the S2I process needs to be able to create new pods (Spark cluster creation). The *oshinko* ServiceAccount with *edit* permissions enabled this.

The Console experience does not require oshinko-rest because the *oshinko* ServiceAccount is present in the S2I template.

The CLI experience does require oshinko-rest because there is no way to attach the *oshinko* ServiceAccount to the result of the S2I process. In this case the resulting pod must communicate with oshinko-rest, which has access to the *oshinko* ServiceAccount to create the Spark clusters.
