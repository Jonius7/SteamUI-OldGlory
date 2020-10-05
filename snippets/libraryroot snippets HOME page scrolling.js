libraryroot beautified, snippets regarding scrolling on the HOME page

===
SNIPPET OnScroll
===


}, e.prototype.OnScroll = function(e) {
                        console.log("scroll | " + performance.now());
                        var t, i, v;
                        t = this.m_elGrid.current.getBoundingClientRect();
                        v = Math.abs(t.top - this.m_fLastScrollTop);
                        if(v>70) {
                            this.props.maxRows < 2 || (i = Math.abs(t.top - this.m_fLastScrollTop), this.props.childHeight * this.props.scaleGridItems / 8 < i && (this.m_fLastScrollTop = t.top, t.top < window.innerHeight && 0 < t.bottom && this.ComputeLayout()));
                        console.log("scroll2 | " + performance.now());
                        }
                        

===
SNIPPET ComputeLayout
===

}), e.prototype.ComputeLayout = function() {
						console.log("b4 var | " + performance.now());
                        var e = this.fScaledPaddedChildWidth,
                            t = this.fScaledPaddedChildHeight,
                            i = this.m_elGrid.current.getBoundingClientRect(),
                            n = i.width - this.props.paddingLeft - this.props.paddingRight;
                            console.log("gappb | " + performance.now())
                            var r = Math.max(1, Math.min(this.props.childElements.length, Math.floor((n + this.props.gridColumnGap) / e)));
                            console.log("gappaf | " + performance.now())
                            var a = Math.ceil(this.props.childElements.length / r),
                            o = Math.max(0, 0 - i.top),
                            s = Math.max(0, Math.min(this.props.childElements.length, Math.round(o / t * r))),
                            l = Math.max(0, window.innerHeight - i.top),
                            c = Math.max(0, Math.min(this.props.childElements.length, Math.round(l / t * r))),
                            p = Math.max(0, s - r * this.props.renderOutsideRows),
                            d = Math.min(this.props.childElements.length, c + r * this.props.renderOutsideRows - 1),
                            u = Math.floor(p / r),
                            m = Math.floor(d / r);
						console.log("afr var | " + performance.now());
                        (u ? u == this.state.iFirstRenderableRow : a ? a == this.state.iRows : m ? m == this.state.iLastRenderableRow : p ? p == this.state.iFirstRenderableChild : d ? d == this.state.iLastRenderableChild : r ? r == this.state.iItemsPerRow : true) || this.setState({
                            iFirstRenderableRow: u,
                            iRows: a,
                            iLastRenderableRow: m,
                            iFirstRenderableChild: p,
                            iLastRenderableChild: d,
                            iItemsPerRow: r
                        });
                        console.log("afr setstate | " + performance.now());
                        var g = void 0 !== this.props.maxRows ? Math.min(this.props.childElements.length, r * this.props.maxRows) : this.props.childElements.length;
                        g != this.m_nItemsDisplayed && (this.m_nItemsDisplayed = g);
                        console.log("afr childele | " + performance.now());