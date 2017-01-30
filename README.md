# A basic Oshinko example app with Word2Vec

## Setup OpenShift

    oc cluster up

## Setup Oshinko

    : Create and authorize the ServiceAccount for Oshinko to create clusters
    oc create serviceaccount oshinko
    oc policy add-role-to-user edit -z oshinko
    : Install the Oshinko source-to-image template
    oc create -f https://raw.githubusercontent.com/radanalyticsio/oshinko-s2i/master/pyspark/pysparkbuilddc.json
    : Launch the Oshinko Web UI
    oc new-app https://raw.githubusercontent.com/radanalyticsio/oshinko-webui/master/tools/ui-template.yaml


## Source-to-image (S2I) to launch the app

    oc new-app --template=oshinko-pyspark-build-dc -p GIT_URI=https://github.com/mattf/py-smoke -lapp=py-smoke
    oc create service clusterip py-smoke --tcp=8080


## Make sure it worked

    : This will return "Connection refused" while the app builds and starts. This can take 5-10 minutes depending on your network speed. It's much faster the second time.
    links -dump $(oc get svc/py-smoke --template='{{.spec.clusterIP}}:{{index .spec.ports 0 "port"}}')


------------------------------------


## Setup Oshinko (alternative path)

    : Launch Oshinko (oshinko-webui and oshinko-rest) from a template
    oc new-app -f http://goo.gl/ZU02P4
    : Authorize Oshinko to create clusters
    oc policy add-role-to-user edit -z oshinko

## Source-to-image (S2I) to launch the app (alternative path)

    : Case0: [image]~[remote source code] (equiv: [remote source repo] --docker-image)
    oc new-app radanalyticsio/radanalytics-pyspark:pre-cli~https://github.com/mattf/py-smoke

    : Case1: [image]~[local source repo] (equiv: [local source repo] --docker-image)
    git clone https://github.com/mattf/py-smoke
    oc new-app radanalyticsio/radanalytics-pyspark:pre-cli~py-smoke



# Notes

### Two user experiences - *new-app* and *oshinko-s2i template*

Currently only *oshinko-s2i template* is available. This is because the *oshinko-s2i builders* require the ability to create new resources on their user's behalf. The builders achieve this by using the *oshinko ServiceAccount*. *oc new-app* does not allow the user to specify a *ServiceAccount*.

Options for enabling *oc new-app* -

* change *new-app* to accept a *ServiceAccount*
* run *oshinko-rest* and change the *oshinko-s2i builders* to fall back if a *ServiceAccount* is not available

The two user experiences should have parity. Parity is missing in a few cases and with a caveat -

* Parity gap: *new-app* automatically creates a Service
* Parity gap: *new-app* requires oshinko-rest
* Parity gap: *oshinko-s2i template* allows for overriding APP_FILE
* Parity gap: *oshinko-s2i template* uses forcePull for the builder image
* Parity gap: the resource labeling differs
* Caveat: it is assumed all Parameters on the *oshinko-s2i template* can be provided as Environment variables to *new-app*
