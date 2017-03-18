# A basic Oshinko example app with Word2Vec

## Prerequisite

[Get started with Oshinko](http://radanalytics.io/get-started)


## Source-to-image (S2I) to launch the app

    oc new-app --template=oshinko-pyspark-build-dc -p GIT_URI=https://github.com/mattf/py-smoke -p APPLICATION_NAME=py-smoke


## Make sure it worked

    : This will return "Connection refused" while the app builds and starts. This can take 5-10 minutes depending on your network speed. It's much faster the second time.
    links -dump $(oc get svc/py-smoke --template='{{.spec.clusterIP}}:{{index .spec.ports 0 "port"}}')
