<template>
  <div class="bg-base-100">
    <div
      class="mx-auto max-w-2xl py-8 px-4 sm:py-8 sm:px-6 lg:max-w-7xl lg:px-8"
    >
      <h2 class="sr-only">Images</h2>

      <div
        class="grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-2 xl:gap-x-8"
      >
        <a v-for="(data, id) in tableData" :key="id" class="group">
          <div
            class="aspect-w-1 aspect-h-1 w-full overflow-hidden rounded-lg bg-gray-200 xl:aspect-w-7 xl:aspect-h-8"
          >
            <img
              :src="data.imageUrl"
              :alt="data.imageUrl"
              class="h-full w-full object-cover object-center group-hover:opacity-75"
            />
          </div>

          <h3 class="mt-4 text-sm text-white text-center">
            {{ data.imageName }}

            [{{ data.uploadTime }}]
          </h3>

          <div class="flex space-x-2 justify-center">
            <div>
              <button
                type="button"
                class="px-6 pt-2.5 pb-2 bg-blue-600 text-white font-medium text-sm leading-none uppercase rounded shadow-md hover:bg-blue-400 hover:shadow-lg focus:bg-blue-400 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-500 active:shadow-lg transition duration-150 ease-in-out flex align-center"
                @click="Download(data)"
              >
                <svg
                  aria-hidden="true"
                  focusable="false"
                  data-prefix="fas"
                  data-icon="download"
                  class="w-3 mr-2"
                  role="img"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 512 512"
                >
                  <path
                    fill="currentColor"
                    d="M216 0h80c13.3 0 24 10.7 24 24v168h87.7c17.8 0 26.7 21.5 14.1 34.1L269.7 378.3c-7.5 7.5-19.8 7.5-27.3 0L90.1 226.1c-12.6-12.6-3.7-34.1 14.1-34.1H192V24c0-13.3 10.7-24 24-24zm296 376v112c0 13.3-10.7 24-24 24H24c-13.3 0-24-10.7-24-24V376c0-13.3 10.7-24 24-24h146.7l49 49c20.1 20.1 52.5 20.1 72.6 0l49-49H488c13.3 0 24 10.7 24 24zm-124 88c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20zm64 0c0-11-9-20-20-20s-20 9-20 20 9 20 20 20 20-9 20-20z"
                  ></path>
                </svg>
                下载
              </button>
            </div>
          </div>
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
    };
  },

  mounted() {
    this.getPlanList();
  },

  beforeRouterEnter(to, from, next) {
    this.getPlanList();
  },

  methods: {
    getPlanList() {
      this.axios
        .get("/api/image/queryAll")
        .then((res) => {
          console.log(res.data);
          console.log(res);
          if (res.status === 200) {
            this.tableData = res.data.data;
            console.log(this.tableData);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getUrlBase64(url) {
      return new Promise((resolve) => {
        let canvas = document.createElement("canvas");
        let ctx = canvas.getContext("2d");
        let img = new Image();
        img.crossOrigin = "Anonymous"; //允许跨域
        img.src = url;
        img.onload = function () {
          canvas.width = img.width;
          canvas.height = img.height;
          ctx.drawImage(img, 0, 0, img.width, img.height);
          let dataURL = canvas.toDataURL("image/png");
          canvas = null;
          resolve(dataURL);
        };
      });
    },
    Download(data) {
      this.getUrlBase64(data.imageUrl).then((base64) => {
        let link = document.createElement("a");
        link.href = base64;
        link.download = data.imageName+".png";
        link.click();
      });
    },
  },
};
</script>
<style></style>
