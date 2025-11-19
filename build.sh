#!/bin/bash
set -ex

if [ ! -n "$1" ]; then
  VER=$(git tag | grep -v "v" | tail -n 1 | python3 -c "import sys; vers=sys.stdin.readline().strip().split('.'); print('.'.join([*vers[:2], str(int(vers[2])+1)]))")
else
  VER="$1"
fi

git tag $VER
git push -u origin ${VER}

# 替换下列为你的阿里云 registry 地址与命名空间
REGISTRY="crpi-uwnl3lhgcvb4rlda.cn-guangzhou.personal.cr.aliyuncs.com/namespace0904"
IMAGE="${REGISTRY}/imagesite:${VER}"

docker build -t ${IMAGE} .
docker push ${IMAGE}
echo ${IMAGE}

