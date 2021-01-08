/* Header Image Snippet */

e.prototype.render = function() {
var e = this.props,
	t = e.rgLogoImages,
	n = e.editMode,
	r = e.logoPosition,
	i = e.className,
	o = e.classNameNoLogo,
	a = e.fnOnPositionChanged,
	s = e.height,
	c = this.state,
	l = c.bFallbackHeader,
	u = c.bHasLogoImage,
	p = [i, Is.a.TopCapsule, !this.state.bHasHeaderImage && Is.a.NoArt, (!this.props.hasHeroImage || l) && Is.a.FallbackArt, !u && o];
/*console.log(this.m_refBackgroundImage)*/
return D.createElement("div", {
	className: er.a.apply(void 0, p),
	style: null == s ? void 0 : {
		height: s + "px"/*,
		background: "url(assets/" + this.props.appid + "_library_hero.jpg)"*/
		/*background: "url(assets/255710_library_hero.jpg?t=1589447656)"*/
	}
},


/* ======== */

return D.createElement("div", {
	className: Object(er.a)(Is.a.HeaderBackgroundImage, Is.a.Glassy)
}, !this.state.bUseCanvasBlur && this.state.bBackgroundLoaded && this.props.rgBlurImages[this.state.nBlurImageIndex] && D.createElement("img", {
	src: this.props.rgBlurImages[this.state.nBlurImageIndex],
	className: Object(er.a)(Is.a.ImgSrc, Is.a.ImgBlur),
	onError: this.OnBlurImageFailed
}), this.state.bUseCanvasBlur && this.state.bBackgroundLoaded && !this.props.bLowPerfMode && D.createElement(Os.a, {
	className: Object(er.a)(Is.a.ImgSrc, Is.a.ImgBlur),
	elementRef: this.m_refCanvasBlurImage,
	updateRate: 0,
	width: 192,
	height: 62,
	reductionFactor: 10,
	blurAmount: 3
}), D.createElement("div", {
	className: Is.a.ImgContainer
}, this.HasHeaderImages() && D.createElement(aa.a, {
	rgSources: this.props.rgHeaderImages,
	style: {
		display: "none"
	},
	className: Is.a.ImgSrc,
	onLoad: this.OnHeaderLoad,
	onIncrementalError: this.OnIncrementalError,
	onError: this.props.onError
})), e)