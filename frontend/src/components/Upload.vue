<template>
  <div
    class="relative min-h-screen flex justify-center bg-base-100 py-12 px-4 sm:px-6 lg:px-8 bg-no-repeat bg-cover items-center"
  >
    <div class="absolute bg-black opacity-60 inset-0 z-0"></div>
    <div class="sm:max-w-lg w-full p-10 bg-white rounded-xl z-10">
      <div class="text-center">
        <h2 class="mt-5 text-3xl font-bold text-gray-900">图片上传</h2>
        <p class="mt-2 text-sm text-gray-400">
          填写文件名, 选择图片后，点击上传
        </p>
      </div>
      <form class="mt-8 space-y-3">
        <div class="grid grid-cols-1 space-y-2">
          <label class="text-sm font-bold text-gray-500 tracking-wide"
            >文件名</label
          >
          <input
            class="text-base p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500"
            type=""
            placeholder="请输入文件名"
            v-model="imageName"
          />
        </div>
        <div class="grid grid-cols-1 space-y-2">
          <label class="text-sm font-bold text-gray-500 tracking-wide"
            >上传图片</label
          >
          <div class="flex items-center justify-center w-full">
            <label
              class="flex flex-col rounded-lg border-4 border-dashed w-full h-60 p-10 group text-center"
            >
              <div
                class="h-full w-full text-center flex flex-col items-center justify-center"
              >
                <div class="flex flex-auto max-h-48 w-3/5 mx-auto -mt-10">
                  <img
                    class="has-mask h-36 object-center"
                    :src="imageSrc"
                    alt="upload image"
                  />
                </div>
                <p class="pointer-none text-gray-500">
                  <span class="text-sm">拖拽</span>图片<br />
                  或
                  <span href="#" id="" class="text-blue-600 hover:underline"
                    >选取图片</span
                  >
                </p>
              </div>
              <input
                accept=".png, .jpg, .jpeg, .webp, .gif"
                type="file"
                class="hidden"
                @change="selectFile"
              />
            </label>
          </div>
        </div>
        <p class="text-sm text-gray-300">
          <span>File type: jpg, jpeg, png, webp, gif</span>
        </p>
        <div>
          <button
            @click="uploadOss"
            class="my-5 w-full flex justify-center bg-blue-500 text-gray-100 p-4 rounded-full tracking-wide font-semibold focus:outline-none focus:shadow-outline hover:bg-blue-600 shadow-lg cursor-pointer transition ease-in duration-300"
          >
            上传至服务器
          </button>
        </div>
        <progress
          class="progress progress-info"
          :value="percentage"
          max="100"
        ></progress>
      </form>
    </div>
  </div>
</template>
<script>
import { client } from "../utils/alioss.js";
import moment from "moment";
import uploadImg from "../assets/upload.webp";

export default {
  data() {
    return {
      msg: "重新上传,建议刷新",
      fileList: [],
      imageName: "",
      ext: ".jpg",
      imageSrc: uploadImg,
      percentage: 0,
      Addfrom: {
        url: "",
      },
    };
  },
  methods: {
    selectFile(e) {
      const file = e.target.files[0];

      if (!this.handleBeforeUpload(file)) {
        return;
      }

      this.fileList = e.target.files;
      this.imageName = file.name.split(".")[0];
      this.ext = file.name.split(".")[1];
      this.imageSrc = URL.createObjectURL(file);
    },

    // 上传文件之前的方法
    handleBeforeUpload(file) {
      const isJPEG = file.name.split(".")[1] === "jpeg";
      const isJPG = file.name.split(".")[1] === "jpg";
      const isPNG = file.name.split(".")[1] === "png";
      const isWEBP = file.name.split(".")[1] === "webp";
      const isGIF = file.name.split(".")[1] === "gif";
      const isLt4M = file.size / 1024 / 1024 < 4;
      if (!isJPG && !isJPEG && !isPNG && !isWEBP && !isGIF) {
        alert("上传图片只能是 JPEG/JPG/PNG 格式!");
      }
      if (!isLt4M) {
        alert("单张图片大小不能超过 4mb!");
      }
      return (isJPEG || isJPG || isPNG || isWEBP || isGIF) && isLt4M;
    },

    uploadOss(e) {
      e.preventDefault();
      for (var i = 0; i < this.fileList.length; i++) {
        let fileName =
          `${moment().format("YYYYMMDD/")}` +
          `${this.imageName}` +
          `${this.fileList[i].lastModified}` +
          `.${this.ext}`;

        //定义唯一的文件名
        //定义唯一的文件名，打印出来的uid其实就是时间戳
        client()
          .multipartUpload(fileName, this.fileList[i], {
            // eslint-disable-next-line no-unused-vars
            progress: (percentage, cpt) => {
              console.log("打印进度", percentage);
              this.percentage = percentage * 100;
            },
          })
          .then((res) => {
            console.log("complete:", res);
            alert("上传成功");
            //上传成功之后，回显操作，拼接桶名+域名+文件名
          })
          .catch((err) => {
            console.log("error:", err);
            alert("上传失败");
          });
        
        const formData = {
          'imageUrl': "https://images-share-seig.oss-cn-guangzhou.aliyuncs.com/" + fileName,
          'imageName': this.imageName
        }

        if (this.imageName != "") {
          this.axios
            .post("/api/image/add", formData)
            .then(function () {})
            .catch(function (e) {
              alert(e);
            });
        } else {
          alert("请填写图片名称");
        }
      }
      this.fileList = [];
      this.$router.push("/scrolling");
    },
  },
};
</script>

<style scoped>
.has-mask {
  position: absolute;
  clip: rect(10px, 150px, 130px, 10px);
}
</style>
