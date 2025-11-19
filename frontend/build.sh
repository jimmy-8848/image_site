set -ex

npm run build
# cp -R dist/* ../imagesite_be/src/main/resources/static/
cp -R dist/* ../imagesite_py/dist/

if [ ! -n "$1" ]; then
    VER=`git tag | grep -v "v" | tail -n 1 |  python3 -c "import sys; vers = sys.stdin.readline().strip().split('.'); print('.'.join([*vers[:2], str(int(vers[2])+1)]))"`
else
    VER="$1"
fi
git tag $VER
git push -u origin ${VER}
