#!/usr/bin/bash
# use buildah to create a container

if [ ! -z "$1" ]; then
  TAG=$1
else
  TAG='latest'
fi

echo "Build image with the tag: $TAG"

IMAGE="alpine:edge"

container=$(buildah from $IMAGE)
buildah run $container apk add python3


buildah copy $container ../exporter.py /exporter.py
buildah run $container chmod go+x /exporter.py

# entrypoint
buildah config --entrypoint "./exporter.py" $container

# finalize
buildah config --label maintainer="Paul Cuzner <pcuzner@redhat.com>" $container
buildah config --label description="simple test prometheus exporter" $container
buildah config --label summary="simple prometheus exporter example" $container
buildah commit --format docker --squash $container test-exporter:$TAG
