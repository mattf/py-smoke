# A basic Oshinko example app with Word2Vec

## Prerequisite

[Get started with Oshinko](http://radanalytics.io/get-started)


## Source-to-image (S2I) to launch the app

    oc new-app --template=oshinko-pyspark-build-dc -p GIT_URI=https://github.com/mattf/py-smoke -p APPLICATION_NAME=py-smoke


## Make sure it worked

    : This will return "Connection refused" while the app builds and starts. This can take 5-10 minutes depending on your network speed. It's much faster the second time.
    links -dump $(oc get svc/py-smoke --template='{{.spec.clusterIP}}:{{index .spec.ports 0 "port"}}')


------------------------------------

# Notes

### Two user experiences - *new-app* and *oshinko-s2i template*

Currently only *oshinko-s2i template* is available. This is because the *oshinko-s2i builders* require the ability to create new resources on their user's behalf. The builders achieve this by using the *oshinko ServiceAccount*. *oc new-app* does not allow the user to specify a *ServiceAccount*.

Options for enabling *oc new-app* -

* change *new-app* to accept a *ServiceAccount*
* run *oshinko-rest* and change the *oshinko-s2i builders* to fall back if a *ServiceAccount* is not available
