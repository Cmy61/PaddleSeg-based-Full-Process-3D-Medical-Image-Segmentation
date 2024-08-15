<template>
	<div>
		<div  class="nifti-image-container">
			<div style="position: relative;" v-for="item in dicomList" :key="item.id" oncontextmenu="return false"
				unselectable="on" onselectstart="return false;" onmousedown="return false;">
				<div class="dicom-info ">
					<span>{{ item.currImgIdIndex + 1 }} / {{ item.total }}</span>
				</div>
				<div ref="viewports" class="nifti-image" :id="item.id"></div>
			</div>
			
			<div  id="nifti-image" class="nifti-image" ref='dicom_canvas'></div>
		</div>
	</div>
</template>

<script>
	var loaded = false
	const Tools = ["OrientationMarkers", "Pan", "Zoom"];
	const synchronizer = new cornerstoneTools.Synchronizer(
	  "cornerstonenewimage",
	  cornerstoneTools.updateImageSynchronizer
	);
	import * as cornerstone from 'cornerstone-core'
	import * as cornerstoneMath from 'cornerstone-math'
	import * as Hammerjs from 'hammerjs'
	import * as cornerstoneTools from 'cornerstone-tools'
	import * as cornerstoneNIFTIImageLoader from 'cornerstone-nifti-image-loader'
	import {getnii} from '@/api/index.js'
	import * as Three from 'three';
	import * as Nifti from 'nifti-reader-js';
	import SubScene1 from '../components/SubScene1.vue';
	export default {
		components: {
			SubScene1
		},
		data() {
			return {
				ImageId: "",
				loaded: false,
				dicomList: [{
						id: "nifti-image-z",
						axis: "z",
						currImgIdIndex: 0,
						total: 0,
				 	complete: false,
						scale: 0,
						overlayUrl: "",
						overlayPixels: [],
					},
					{
				  id: "nifti-image-x",
						axis: "x",
						currImgIdIndex: 0,
						total: 0,
						complete: false,
						scale: 0,
						overlayUrl: "",
						overlayPixels: [],
					},
					{
						id: "nifti-image-y",
						axis: "y",
						currImgIdIndex: 0,
						total: 0,
						complete: false,
						scale: 0,
						overlayUrl: "",
						overlayPixels: [],
					},
				],
				flag_point_material: null,
				mesh: null,
			}
		},
		props: {
			Select_url: {
				type: [String, Number],
				default: "http://localhost:8888/path/C:/Users/92090/Desktop/3D医学影像/base_train/labelsTr/test_label.nii", //默认值为空现在测试阶段
			},
		},
		watch: {
			Select_url: {
				handler(val) {
					this.display();
				},
			}
		},
		mounted() {
			cornerstoneNIFTIImageLoader.external.cornerstone = cornerstone;
			cornerstoneTools.external.cornerstoneMath = cornerstoneMath;
			cornerstoneTools.external.cornerstone = cornerstone;
			cornerstoneTools.external.Hammer = Hammer;
			cornerstoneNIFTIImageLoader.nifti.streamingMode = true;
			this.ImageId = cornerstoneNIFTIImageLoader.nifti.ImageId;
			cornerstoneTools.init();
			const element = document.getElementById('nifti-image');
			this.$refs.viewports.forEach((element) => {
				element.addEventListener("cornerstonetoolsmousewheel", (e) => {
					e.preventDefault()
					this.$nextTick(() =>{
						 this.handleStackScroll(e)
					});
				});
				// render事件
				element.addEventListener(cornerstone.EVENTS.IMAGE_RENDERED, (e) => {
					e.preventDefault()
					this.$nextTick(() => {
						this.handleEnabled(e);
						console.log(e.detail.viewport)
						// console.log(cornerstone);
					});
				});

			});
			this.display()
		},
		methods: {
			getExampleImage(imageId) {
				const width = 256;
				const height = 256;

				function getPixelData() {
					if (imageId === 'example://1') {
						return image1PixelData;
					} else if (imageId === 'example://2') {
						return image2PixelData;
					}

					throw "unknown imageId";
				}

				var image = {
					imageId: imageId,
					minPixelValue: 0,
					maxPixelValue: 257,
					slope: 1.0,
					intercept: 0,
					windowCenter: 127,
					windowWidth: 256,
					getPixelData: getPixelData,
					rows: height,
					columns: width,
					height: height,
					width: width,
					color: false,
					columnPixelSpacing: .8984375,
					rowPixelSpacing: .8984375,
					sizeInBytes: width * height * 2
				};

				return {
					promise: new Promise((resolve)=>{
						resolve(image);
					}
					),
					cancelFn: undefined
				};
			},
			async display(){
				let timepoint = 0;
				// let url=window.SITE_CONFIG.baseUrl + "/static"+ this.Select_url;
                let url = this.Select_url;
				for (let i = 0; i < this.dicomList.length; i++) {
					const canvas = document.getElementById(this.dicomList[i].id);
					console.log(this.Select_url);
					const imageIdObject = this.ImageId.fromURL("nifti:" +
						`${url}#${this.dicomList[i].axis},t-${timepoint}`);
				await	this.loadAndViewImage(
						canvas,
						`nifti:${imageIdObject.filePath}#${this.dicomList[i].axis},t-${timepoint}`,
						i
					);
				}
				this.$emit('current-loaded')
			},
			handleStackScroll(e) {
				// 滚动事件
				const element = e.detail.element;
				const toolData = cornerstoneTools.getToolState(element, "stack");
				const stackData = toolData.data[0];

				let currImgIdIndex = stackData.currentImageIdIndex;
				let dicom = this.dicomList.find((item) => item.id === element.id);
				
				dicom.currImgIdIndex = currImgIdIndex;
			},
			handleEnabled(e) {
				// render事件
				const viewport = e.detail.viewport;
				const element = e.detail.element;
				const toolData = cornerstoneTools.getToolState(element, "stack");
				const stackData = toolData.data[0];
				let dicom = this.dicomList.find((item) => item.id === element.id);
				// console.log(toolData);
				// console.log(viewport);
				// console.log(element);
				// console.log(dicom);
				// console.log(stackData);
				


				dicom.scale = viewport.scale.toFixed(4);
				dicom.currImgIdIndex = stackData.currentImageIdIndex;
			},
			loadAndViewImage(element, imageId, i) {
				cornerstone.enable(element);

				const _this = this;
				const imageIdObject = this.ImageId.fromURL(imageId);
				console.log(imageIdObject);
				element.dataset.imageId = imageIdObject.url;

				return new Promise((resolve) => {
					try {
						cornerstone.loadAndCacheImage(imageIdObject.url).then(function(image) {
							// 设置图片信息
							let imagePlaneModule = cornerstone.metaData.get(
								"imagePlaneModule",
								image.imageId
							);
							console.log("------")
							console.log(image);
							resolve(image);
							const numberOfSlices = cornerstone.metaData.get(
								"multiFrameModule",
								imageIdObject.url
							).numberOfFrames;
							const imageIds = Array.from(
								Array(numberOfSlices),
								(_, i) =>
								`nifti:${imageIdObject.filePath}#${imageIdObject.slice.dimension}-${i},t-0`
							);
							const stack = {
								currentImageIdIndex: imageIdObject.slice.index,
								imageIds,
							};
							image.color = true;
							
							// console.log(element);
							// console.log(image);
							// // console.log(viewport);
							// const pixeldata = image.getPixelData();
							// var colormap = new Uint8Array(pixeldata.length * 4);
							// for (let i=0;i<pixeldata.length;++i){
							// 	if (pixeldata[i]==1){
							// 		colormap[i*4] = 255;
							// 		colormap[i*4+1] = 0;
							// 		colormap[i*4+2] = 0;
							// 		colormap[i*4+3] = 255;
							// 	}
							// 	else {
							// 		colormap[i*4] = 255;
							// 		colormap[i*4+1] = 0;
							// 		colormap[i*4+2] = 0;
							// 		colormap[i*4+3] = 255;
							// 	}
							// }
							// // image.pixeldata = colormap;
							// // image.color = true;
							// image.color = true;
							// image.render = cornerstone.renderColorImage;
							// image.labelmap = true;
							// console.log(image);
							// console.log(cornerstone.colors.getColormapsList())
							
							


							const viewport = cornerstone.getDefaultViewportForImage(element, image);
							// 像素渲染
							const enabledElement = cornerstone.getEnabledElement(element);
							
							// viewport.colormap = colormap;
							// console.log(viewport)
							
							
							// let qcolormap = cornerstone.colors.getColormap('myCustomColorMap');
							
							// qcolormap.setNumberOfColors(13);

							// // You can also use `addColor` but in this case it wouldn't work.
							// // Any colormap returned by `getColormap` lasts forever (global) and
							// // calling `addColor` would result in duplicated colors.
							// qcolormap.insertColor(0, [255,0,0, 255]); // Banana
							// qcolormap.insertColor(1, [245, 222, 179, 255]); // Wheat
							// qcolormap.insertColor(2, [255, 125,  64, 255]); // Flesh
							// qcolormap.insertColor(3, [135,  38,  87, 255]); // Raspberry
							// qcolormap.insertColor(4, [227, 206,  199, 255]); // Mint
							// qcolormap.insertColor(5, [ 51, 160, 201, 255]); // Peacock
							// qcolormap.insertColor(6, [245, 222, 179, 255]); // Wheat
							// qcolormap.insertColor(7, [77, 125,  64, 255]); // Flesh
							// qcolormap.insertColor(8, [160,  38,  255, 255]); // Raspberry
							// qcolormap.insertColor(9, [227, 206,  87, 255]); // Mint
							// qcolormap.insertColor(10, [ 99, 179, 222, 255]); // Peacock
							// qcolormap.insertColor(11, [ 111, 99, 201, 255]); // Peacock
							// qcolormap.insertColor(12, [ 78, 23, 131, 255]); // Peacock
							// // colormap.insertColor(10, [ 51, 160, 201, 255]); // Peacock

							// // let temp_viewport = cornerstone.getViewport(element);
							// viewport.colormap = qcolormap;
							// const lookupTable = qcolormap.createLookupTable();
							// lookupTable.setTableRange(0, 12);
							// cornerstone.setViewport(element, viewport);
							// cornerstone.updateImage(element, true);
							// // console.log(viewport);
							
							// console.log(qcolormap)
							// console.log(viewport);
							// console.log(lookupTable);
							

							_this.dicomList[i]["total"] = imageIds.length;
							cornerstone.displayImage(element, image, viewport);
							cornerstone.resize(element, true);
							// enabledElement.viewport.pixelReplication = true;

							cornerstoneTools.addStackStateManager(element, ["stack", "Crosshairs"]);
							cornerstoneTools.addToolState(element, "stack", stack);

							// 设置 Pan、Zoom、Orient工具
							Tools.forEach((tool) => {
								let key = tool === "Pan" ? 2 : 1;
								cornerstoneTools.addToolForElement(
									element,
									cornerstoneTools[`${tool}Tool`]
								);
								cornerstoneTools.setToolActive(tool, {
									mouseButtonMask: key,
								});
							});

							// 鼠标滑动
							cornerstoneTools.addToolForElement(
								element,
								cornerstoneTools["StackScrollMouseWheelTool"]
							);
							cornerstoneTools.setToolActive("StackScrollMouseWheel", {
								mouseButtonMask: 0,
							});
							synchronizer.add(element);
							// 十字线
							cornerstoneTools.stackPrefetch.enable(element);
							cornerstoneTools.addToolForElement(
								element,
								cornerstoneTools.ReferenceLinesTool
							);
							cornerstoneTools.setToolEnabled("ReferenceLines", {
								synchronizationContext: synchronizer,
							});
							// 光标
							cornerstoneTools.addToolForElement(
								element,
								cornerstoneTools["CrosshairsTool"]
							);
							cornerstoneTools.setToolActive("Crosshairs", {
								mouseButtonMask: 1,
								synchronizationContext: synchronizer,
							});
						});
					} catch (err) {
						throw err;
					}
				});
			},
		},
	}
</script>

<style scoped>
	.nifti-image-container{
		display: flex;
		flex-flow: row wrap;
		width: 100%;
		height: auto;
	}
	.nifti-image {
		margin: 30px 10px 10px 20px;
		width: 400px;
		height: 200px;
	}
	.dicom-info{
		color: #FFFFFF;
		position: absolute;
		bottom: 20px;
		left: 40px;
		z-index: 11;
	}
</style>

